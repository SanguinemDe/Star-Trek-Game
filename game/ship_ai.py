"""
Advanced AI Controller for Computer-Controlled Ships in Combat

This module provides intelligent AI behavior for ships in tactical combat,
including movement, targeting, firing decisions, and shield management.

Features:
- Robust error handling with detailed logging
- Multiple AI personalities (Aggressive, Defensive, Balanced, Sniper)
- Intelligent target selection based on threat assessment
- Tactical movement with range management
- Shield rotation to protect weak facings
- Weapon firing decisions based on arc and range
- Multi-enemy support

Author: Rewritten for robustness and clarity
Date: November 5, 2025
"""

import random
import math
from game.logger import get_logger

logger = get_logger(__name__)


class ShipAI:
    """
    Advanced AI controller for ships in tactical combat
    
    This AI makes intelligent decisions about movement, targeting, and firing
    while handling edge cases and errors gracefully.
    """
    
    def __init__(self, ship, hex_grid):
        """
        Initialize AI controller with required components
        
        Args:
            ship: The AdvancedShip instance this AI controls
            hex_grid: HexGrid instance for navigation calculations
            
        Raises:
            ValueError: If ship or hex_grid is invalid
        """
        # Validate inputs
        if not ship:
            logger.error("ShipAI: Cannot initialize with None ship")
            raise ValueError("ShipAI requires a valid ship object")
        if not hex_grid:
            logger.error("ShipAI: Cannot initialize with None hex_grid")
            raise ValueError("ShipAI requires a valid hex_grid object")
        
        # Store references
        self.ship = ship
        self.hex_grid = hex_grid
        self.target = None
        self.all_ships = []  # List of all ships in combat
        
        # AI Personality Settings (can be modified by AIPersonality.apply_to_ai)
        self.preferred_range = 6  # Optimal range to maintain (hexes)
        self.aggressive = True  # Will close to optimal range
        self.retreat_threshold = 0.3  # Retreat when hull drops below this %
        self.evasion_priority = 0.5  # How much to prioritize evasive movement (0.0-1.0)
        
        # Tactical state
        self.last_target_arc = None
        self.turns_at_optimal_range = 0
        self.retreat_mode = False
        
        logger.info(f"AI initialized for {ship.name} ({ship.ship_class}-class)")
        
        # Verify ship has required hex coordinates
        if not hasattr(ship, 'hex_q'):
            logger.warning(f"{ship.name}: Missing hex_q, setting to 0")
            ship.hex_q = 0
        if not hasattr(ship, 'hex_r'):
            logger.warning(f"{ship.name}: Missing hex_r, setting to 0")
            ship.hex_r = 0
    
    # ═══════════════════════════════════════════════════════════════════
    # TARGET SELECTION
    # ═══════════════════════════════════════════════════════════════════
    
    def set_target(self, target_ship):
        """
        Manually set the target ship to engage
        
        Args:
            target_ship: Ship to target, or None to clear target
        """
        if target_ship:
            logger.info(f"{self.ship.name}: Target set to {target_ship.name}")
        else:
            logger.info(f"{self.ship.name}: Target cleared")
        self.target = target_ship
    
    def select_best_target(self, all_ships):
        """
        Intelligently select the best enemy target from available ships
        
        Uses threat assessment based on:
        - Distance (prefer closer targets)
        - Hull integrity (prefer damaged targets)
        - Firepower (prefer armed threats)
        - Faction (must be enemy)
        
        Args:
            all_ships: List of all ships in combat
            
        Returns:
            Ship object or None if no valid targets
        """
        try:
            if not all_ships:
                logger.warning(f"{self.ship.name}: No ships list provided for targeting")
                return None
            
            self.all_ships = all_ships
            
            # Get this ship's faction
            my_faction = getattr(self.ship, 'faction', 'neutral')
            
            # Find all valid enemy targets
            valid_targets = []
            for ship in all_ships:
                # Skip self
                if ship == self.ship:
                    continue
                
                # Skip dead ships
                if not hasattr(ship, 'hull') or ship.hull <= 0:
                    continue
                
                # Check faction
                ship_faction = getattr(ship, 'faction', 'neutral')
                
                # Don't attack ships of same faction
                if ship_faction == my_faction:
                    continue
                
                # Don't attack neutral unless we're hostile
                if ship_faction == 'neutral' and my_faction != 'hostile':
                    continue
                
                valid_targets.append(ship)
            
            if not valid_targets:
                logger.debug(f"{self.ship.name}: No valid enemy targets found")
                return None
            
            # Score each target
            best_target = None
            best_score = -999999
            
            for target in valid_targets:
                score = self._calculate_target_priority(target)
                
                if score > best_score:
                    best_score = score
                    best_target = target
            
            if best_target:
                logger.info(f"{self.ship.name}: Selected target {best_target.name} (score: {best_score:.1f})")
            
            return best_target
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error selecting target: {e}")
            return None
    
    def _calculate_target_priority(self, target):
        """
        Calculate priority score for a potential target
        
        Args:
            target: Ship to evaluate
            
        Returns:
            float: Priority score (higher = better target)
        """
        try:
            score = 0.0
            
            # Verify both ships have coordinates
            if not all(hasattr(self.ship, attr) for attr in ['hex_q', 'hex_r']):
                logger.warning(f"{self.ship.name}: Missing hex coordinates for distance calc")
                return score
            
            if not all(hasattr(target, attr) for attr in ['hex_q', 'hex_r']):
                logger.warning(f"{target.name}: Missing hex coordinates for distance calc")
                return score
            
            # 1. Distance scoring (closer is better)
            distance = self.hex_grid.distance(
                self.ship.hex_q, self.ship.hex_r,
                target.hex_q, target.hex_r
            )
            # Score: 0 to -30 based on distance (0 = same hex, -30 = 30+ hexes away)
            distance_score = -min(distance, 30)
            score += distance_score
            
            # 2. Damage potential (prefer weakened targets)
            if hasattr(target, 'hull') and hasattr(target, 'max_hull') and target.max_hull > 0:
                hull_percent = target.hull / target.max_hull
                # Score: 0 to +50 based on damage (50 = nearly dead, 0 = full health)
                damage_score = (1.0 - hull_percent) * 50
                score += damage_score
            
            # 3. Threat level (prefer armed targets)
            weapon_count = 0
            if hasattr(target, 'weapon_arrays'):
                weapon_count += len(target.weapon_arrays)
            if hasattr(target, 'torpedo_bays'):
                weapon_count += len(target.torpedo_bays)
            # Score: 0 to +20 based on weapons (more weapons = higher priority)
            threat_score = min(weapon_count * 5, 20)
            score += threat_score
            
            # 4. Current target bonus (prefer to keep current target)
            if target == self.target:
                score += 25
            
            return score
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error calculating target priority: {e}")
            return 0.0
    
    def update_target(self, all_ships):
        """
        Re-evaluate target selection if current target is invalid or dead
        
        This is called at the start of each phase to ensure the AI has a valid target.
        
        Args:
            all_ships: List of all ships in combat
        """
        try:
            self.all_ships = all_ships
            
            # Check if current target is valid
            target_valid = (
                self.target is not None
                and hasattr(self.target, 'hull')
                and self.target.hull > 0
            )
            
            # Check if current target is still an enemy
            if target_valid:
                my_faction = getattr(self.ship, 'faction', 'neutral')
                target_faction = getattr(self.target, 'faction', 'neutral')
                
                if my_faction == target_faction:
                    logger.info(f"{self.ship.name}: Current target {self.target.name} is now friendly")
                    target_valid = False
            
            # Select new target if needed
            if not target_valid:
                old_target = self.target.name if self.target else "None"
                self.target = self.select_best_target(all_ships)
                if self.target:
                    logger.info(f"{self.ship.name}: Target changed from {old_target} to {self.target.name}")
                else:
                    logger.warning(f"{self.ship.name}: No valid targets available")
                    
        except Exception as e:
            logger.error(f"{self.ship.name}: Error updating target: {e}")
            self.target = None
    
    # ═══════════════════════════════════════════════════════════════════
    # MOVEMENT AI
    # ═══════════════════════════════════════════════════════════════════
    
    def decide_movement(self, movement_points):
        """
        Decide movement actions for this turn based on tactical situation
        
        Movement priorities:
        1. Retreat if hull is critical
        2. Rotate shields if current facing is weak
        3. Turn to bring weapons on target
        4. Maneuver to optimal range
        5. Tactical positioning at optimal range
        
        Args:
            movement_points: Number of movement points available this turn
            
        Returns:
            list: List of movement commands ['forward', 'backward', 'turn_left', 'turn_right']
        """
        try:
            # Validate inputs
            if movement_points is None or movement_points <= 0:
                logger.debug(f"{self.ship.name}: No movement points available")
                return []
            
            if not self.target:
                logger.debug(f"{self.ship.name}: No target for movement decision")
                return []
            
            # Verify required attributes exist
            required_attrs = ['hex_q', 'hex_r', 'facing', 'hull', 'max_hull']
            for attr in required_attrs:
                if not hasattr(self.ship, attr):
                    logger.error(f"{self.ship.name}: Missing required attribute '{attr}'")
                    return []
            
            # Verify target has coordinates
            if not hasattr(self.target, 'hex_q') or not hasattr(self.target, 'hex_r'):
                logger.error(f"{self.ship.name}: Target {self.target.name} missing hex coordinates")
                return []
            
            logger.info(f"{self.ship.name}: Deciding movement ({movement_points} MP available)")
            
            # Calculate current tactical situation
            distance = self.hex_grid.distance(
                self.ship.hex_q, self.ship.hex_r,
                self.target.hex_q, self.target.hex_r
            )
            
            target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
            hull_percent = self.ship.hull / max(self.ship.max_hull, 1)
            
            logger.info(f"  Distance: {distance}, Arc: {target_arc}, Hull: {hull_percent:.1%}")
            
            # Determine retreat status
            if hull_percent < self.retreat_threshold:
                self.retreat_mode = True
            elif hull_percent > (self.retreat_threshold + 0.2):  # Hysteresis
                self.retreat_mode = False
            
            # Execute movement strategy
            moves = []
            remaining_mp = movement_points
            
            # PRIORITY 1: Retreat if critically damaged
            if self.retreat_mode:
                logger.info(f"{self.ship.name}: RETREAT MODE (hull {hull_percent:.1%})")
                moves = self._plan_retreat_movement(remaining_mp, target_arc)
                return moves
            
            # PRIORITY 2: Shield rotation if shields are weak
            shield_rotation = self._should_rotate_shields(target_arc)
            if shield_rotation['should_rotate'] and remaining_mp >= 2:
                logger.info(f"{self.ship.name}: {shield_rotation['reason']}")
                moves.append('forward')
                moves.append(shield_rotation['direction'])
                remaining_mp -= 2
                
                # Return after shield rotation to avoid overcomplicating
                if remaining_mp == 0:
                    return moves
            
            # PRIORITY 3: Range management (check BEFORE weapon arcs)
            # This ensures ships don't turn uselessly when they should be backing away
            range_diff = distance - self.preferred_range
            
            # Get weapons on target if not in arc (but only if range is OK)
            weapons_in_arc = self._check_weapons_in_arc(target_arc)
            if not weapons_in_arc and remaining_mp >= 2 and abs(range_diff) <= 2:
                # Only turn to bring weapons to bear if we're at reasonable range
                logger.info(f"{self.ship.name}: Turning to bring weapons on target")
                turn_dir = self._determine_turn_direction()
                if turn_dir:
                    moves.append('forward')
                    moves.append(turn_dir)
                    remaining_mp -= 2
            
            # PRIORITY 4: Range management
            # Always try to maintain optimal range
            if range_diff > 1 and self.aggressive:
                # Too far, close in (only if aggressive)
                logger.info(f"{self.ship.name}: Closing to optimal range (currently {distance}, want {self.preferred_range})")
                steps = min(remaining_mp, max(1, abs(range_diff)))
                for _ in range(steps):
                    moves.append('forward')
                    remaining_mp -= 1
            elif range_diff < -1:
                # Too close, back off (always back off if too close)
                logger.info(f"{self.ship.name}: Backing to optimal range (currently {distance}, want {self.preferred_range})")
                steps = min(remaining_mp, max(1, abs(range_diff)))
                for _ in range(steps):
                    moves.append('backward')
                    remaining_mp -= 1
            
            # PRIORITY 5: Use ALL remaining movement points for tactical maneuvering
            # Small/fast ships MUST stay mobile to survive
            # TURNING RULES: Must move before turning, can only turn once per hex moved
            # Valid pattern: forward, turn, forward, turn, forward...
            
            while remaining_mp > 0:
                if remaining_mp >= 2 and self.evasion_priority > 0.3:
                    # Evasive maneuver: move + turn (legal sequence)
                    logger.info(f"{self.ship.name}: Evasive maneuver ({remaining_mp} MP left)")
                    moves.append('forward')
                    turn_choice = random.choice(['turn_left', 'turn_right'])
                    moves.append(turn_choice)
                    remaining_mp -= 2
                elif remaining_mp >= 2 and self.aggressive and random.random() < 0.6:
                    # Aggressive tactical: move + turn (legal sequence)
                    logger.info(f"{self.ship.name}: Aggressive advance with turn ({remaining_mp} MP left)")
                    moves.append('forward')
                    turn_choice = random.choice(['turn_left', 'turn_right'])
                    moves.append(turn_choice)
                    remaining_mp -= 2
                elif remaining_mp >= 1:
                    # Just move forward
                    logger.info(f"{self.ship.name}: Straight advance ({remaining_mp} MP left)")
                    moves.append('forward')
                    remaining_mp -= 1
                else:
                    break
            
            logger.info(f"{self.ship.name}: Planned moves: {moves}")
            return moves
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error in decide_movement: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _plan_retreat_movement(self, movement_points, target_arc):
        """
        Plan movement for retreat (backing away while keeping weapons on target)
        
        Args:
            movement_points: Available movement points
            target_arc: Current arc where target is located
            
        Returns:
            list: Movement commands
        """
        moves = []
        remaining = movement_points
        
        # Try to keep weapons on target while retreating
        weapons_in_arc = self._check_weapons_in_arc(target_arc)
        
        if weapons_in_arc and remaining >= 1:
            # Back away while maintaining firing solution
            steps = min(remaining, 2)
            for _ in range(steps):
                moves.append('backward')
                remaining -= 1
        elif remaining >= 2:
            # Turn to bring weapons to bear, then retreat
            turn_dir = self._determine_turn_direction()
            if turn_dir:
                moves.append('forward')
                moves.append(turn_dir)
                remaining -= 2
        
        return moves
    
    def _check_weapons_in_arc(self, target_arc):
        """
        Check if any weapons can fire at the target arc
        
        Args:
            target_arc: Arc to check ('fore', 'aft', 'port-fore', etc.)
            
        Returns:
            bool: True if at least one weapon can fire at this arc
        """
        try:
            if not target_arc:
                return False
            
            # Check energy weapons
            if hasattr(self.ship, 'weapon_arrays'):
                for weapon in self.ship.weapon_arrays:
                    if hasattr(weapon, 'firing_arcs') and target_arc in weapon.firing_arcs:
                        return True
            
            # Check torpedo bays
            if hasattr(self.ship, 'torpedo_bays'):
                for torpedo in self.ship.torpedo_bays:
                    if hasattr(torpedo, 'firing_arcs') and target_arc in torpedo.firing_arcs:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error checking weapons in arc: {e}")
            return False
    
    def _determine_turn_direction(self):
        """
        Determine which direction to turn to face target
        
        Returns:
            str: 'turn_left' or 'turn_right' or None
        """
        try:
            if not self.target:
                return None
            
            # Calculate angle to target
            dx = self.target.position[0] - self.ship.position[0]
            dy = self.target.position[1] - self.ship.position[1]
            angle_to_target = math.degrees(math.atan2(dy, dx))
            
            # Normalize to 0-360
            if angle_to_target < 0:
                angle_to_target += 360
            
            # Current facing angle (facing 0 = 90°, each facing is 60° clockwise)
            current_angle = 90 + (self.ship.facing * 60)
            current_angle = current_angle % 360
            
            # Calculate angular difference
            diff = angle_to_target - current_angle
            
            # Normalize to -180 to 180
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360
            
            # Determine turn direction
            if abs(diff) < 30:  # Already facing roughly correct direction
                return None
            elif diff > 0:
                return 'turn_right'  # Target is clockwise
            else:
                return 'turn_left'  # Target is counter-clockwise
                
        except Exception as e:
            logger.error(f"{self.ship.name}: Error determining turn direction: {e}")
            return None
    
    def _should_rotate_shields(self, target_arc):
        """
        Determine if we should rotate to present stronger shields
        
        Args:
            target_arc: Arc where the target is located
            
        Returns:
            dict: {'should_rotate': bool, 'direction': str or None, 'reason': str}
        """
        try:
            result = {'should_rotate': False, 'direction': None, 'reason': ''}
            
            if not hasattr(self.ship, 'shields') or not hasattr(self.ship, 'max_shields'):
                result['reason'] = "No shield system"
                return result
            
            # Get shield strength for current facing
            shield_facing = self._arc_to_shield_facing(target_arc)
            current_shield = self.ship.shields.get(shield_facing, 0)
            max_shield = self.ship.max_shields.get(shield_facing, 1)
            
            if max_shield <= 0:
                result['reason'] = "No max shield"
                return result
            
            current_percent = current_shield / max_shield
            
            # If current shield is strong (>60%), don't rotate
            if current_percent > 0.6:
                result['reason'] = f"Current {shield_facing} shields strong ({current_percent:.1%})"
                return result
            
            # If current shield is weak (<40%), consider rotating
            if current_percent < 0.4:
                # Find the strongest shield
                strongest_facing = None
                strongest_percent = 0
                
                for facing, value in self.ship.shields.items():
                    max_val = self.ship.max_shields.get(facing, 1)
                    if max_val > 0:
                        percent = value / max_val
                        if percent > strongest_percent:
                            strongest_facing = facing
                            strongest_percent = percent
                
                # If we found a much stronger shield (20%+ better), rotate to it
                if strongest_facing and strongest_percent > (current_percent + 0.2):
                    # Determine which way to turn to present that shield to target
                    turn_dir = self._calculate_turn_to_present_shield(target_arc, strongest_facing)
                    
                    result['should_rotate'] = True
                    result['direction'] = turn_dir
                    result['reason'] = f"Rotating {strongest_facing} shield ({strongest_percent:.1%}) to threat"
                    return result
            
            result['reason'] = "No shield rotation needed"
            return result
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error checking shield rotation: {e}")
            return {'should_rotate': False, 'direction': None, 'reason': 'Error'}
    
    def _arc_to_shield_facing(self, arc):
        """Convert target arc to shield facing"""
        arc_map = {
            'fore': 'fore',
            'starboard-fore': 'starboard',
            'starboard-aft': 'starboard',
            'aft': 'aft',
            'port-aft': 'port',
            'port-fore': 'port'
        }
        return arc_map.get(arc, 'fore')
    
    def _calculate_turn_to_present_shield(self, current_target_arc, desired_shield_facing):
        """
        Calculate which direction to turn to present desired shield to target
        
        Args:
            current_target_arc: Where target currently is
            desired_shield_facing: Which shield we want to present ('fore', 'aft', 'port', 'starboard')
            
        Returns:
            str: 'turn_left' or 'turn_right' or None
        """
        # Map shield facing to arc
        facing_to_arc = {
            'fore': 'fore',
            'aft': 'aft',
            'port': 'port-fore',
            'starboard': 'starboard-fore'
        }
        
        desired_arc = facing_to_arc.get(desired_shield_facing, 'fore')
        
        # Arc positions (clockwise from fore)
        arc_positions = {
            'fore': 0,
            'starboard-fore': 1,
            'starboard-aft': 2,
            'aft': 3,
            'port-aft': 4,
            'port-fore': 5
        }
        
        current_pos = arc_positions.get(current_target_arc, 0)
        desired_pos = arc_positions.get(desired_arc, 0)
        
        # Calculate shortest turn direction
        diff = (desired_pos - current_pos) % 6
        
        if diff == 0:
            return None  # Already presenting correct shield
        elif diff <= 3:
            return 'turn_right'  # Turn clockwise
        else:
            return 'turn_left'  # Turn counter-clockwise
    
    # ═══════════════════════════════════════════════════════════════════
    # FIRING AI
    # ═══════════════════════════════════════════════════════════════════
    
    def should_fire(self):
        """
        Decide whether to fire weapons this turn
        
        Returns:
            bool: True if should fire, False otherwise
        """
        try:
            if not self.target:
                return False
            
            if not hasattr(self.target, 'hull') or self.target.hull <= 0:
                return False
            
            # Verify we have coordinates
            if not all(hasattr(self.ship, attr) for attr in ['hex_q', 'hex_r']):
                return False
            if not all(hasattr(self.target, attr) for attr in ['hex_q', 'hex_r']):
                return False
            
            # Calculate distance
            distance = self.hex_grid.distance(
                self.ship.hex_q, self.ship.hex_r,
                self.target.hex_q, self.target.hex_r
            )
            
            # Get target arc
            target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
            
            # Check if any weapons are ready and in arc
            can_fire = False
            
            # Check energy weapons (phasers, etc.)
            if hasattr(self.ship, 'weapon_arrays'):
                for weapon in self.ship.weapon_arrays:
                    if hasattr(weapon, 'can_fire') and weapon.can_fire():
                        if hasattr(weapon, 'firing_arcs') and target_arc in weapon.firing_arcs:
                            if distance <= 12:  # Max phaser range
                                can_fire = True
                                break
            
            # Check torpedoes
            if not can_fire and hasattr(self.ship, 'torpedo_bays'):
                for torpedo in self.ship.torpedo_bays:
                    if hasattr(torpedo, 'can_fire') and torpedo.can_fire():
                        if hasattr(torpedo, 'firing_arcs') and target_arc in torpedo.firing_arcs:
                            if distance <= 15:  # Max torpedo range
                                can_fire = True
                                break
            
            if can_fire:
                logger.info(f"{self.ship.name}: Can fire at {self.target.name} (dist: {distance}, arc: {target_arc})")
            
            return can_fire
            
        except Exception as e:
            logger.error(f"{self.ship.name}: Error in should_fire: {e}")
            return False
    
    def get_combat_report(self):
        """
        Generate a brief status report for debugging
        
        Returns:
            str: Status report
        """
        try:
            if not self.target:
                return f"{self.ship.name}: No target"
            
            distance = self.hex_grid.distance(
                self.ship.hex_q, self.ship.hex_r,
                self.target.hex_q, self.target.hex_r
            )
            
            target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
            hull_percent = int((self.ship.hull / self.ship.max_hull) * 100)
            
            return f"{self.ship.name}: Target={self.target.name} Dist={distance} Arc={target_arc} Hull={hull_percent}%"
            
        except Exception as e:
            return f"{self.ship.name}: Error generating report: {e}"


class AIPersonality:
    """
    Predefined AI personality types for variety in combat
    
    Each personality modifies the AI's behavior by adjusting:
    - preferred_range: Optimal combat distance
    - aggressive: Whether to close or maintain distance
    - retreat_threshold: Hull % at which to retreat
    """
    
    AGGRESSIVE = {
        'preferred_range': 4,  # Close range combat
        'aggressive': True,
        'retreat_threshold': 0.2,  # Only retreat at 20% hull
        'evasion_priority': 0.3,  # Low evasion (prefer direct assault)
    }
    
    DEFENSIVE = {
        'preferred_range': 8,  # Long range combat
        'aggressive': False,
        'retreat_threshold': 0.5,  # Retreat at 50% hull
        'evasion_priority': 0.8,  # High evasion (stay mobile for defense)
    }
    
    BALANCED = {
        'preferred_range': 6,  # Medium range combat
        'aggressive': True,
        'retreat_threshold': 0.3,  # Retreat at 30% hull
        'evasion_priority': 0.5,  # Moderate evasion
    }
    
    SNIPER = {
        'preferred_range': 10,  # Very long range combat
        'aggressive': False,
        'retreat_threshold': 0.4,  # Retreat at 40% hull
        'evasion_priority': 0.6,  # Moderate-high evasion (kiting)
    }
    
    @staticmethod
    def apply_to_ai(ai, personality_name):
        """
        Apply a personality to an AI instance
        
        Args:
            ai: ShipAI instance to modify
            personality_name: str ('aggressive', 'defensive', 'balanced', 'sniper')
        """
        personalities = {
            'aggressive': AIPersonality.AGGRESSIVE,
            'defensive': AIPersonality.DEFENSIVE,
            'balanced': AIPersonality.BALANCED,
            'sniper': AIPersonality.SNIPER,
        }
        
        personality = personalities.get(personality_name.lower(), AIPersonality.BALANCED)
        
        ai.preferred_range = personality['preferred_range']
        ai.aggressive = personality['aggressive']
        ai.retreat_threshold = personality['retreat_threshold']
        ai.evasion_priority = personality['evasion_priority']
        
        logger.info(f"Applied {personality_name.upper()} personality to {ai.ship.name}")
