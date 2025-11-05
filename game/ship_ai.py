"""
Basic AI controller for computer-controlled ships in combat.
Provides simple but effective tactical decision-making.
"""

import random


class ShipAI:
    """Basic AI controller for ships in combat"""
    
    def __init__(self, ship, hex_grid):
        """
        Initialize AI controller
        
        Args:
            ship: The AdvancedShip this AI controls
            hex_grid: HexGrid instance for navigation
        """
        self.ship = ship
        self.hex_grid = hex_grid
        self.target = None
        self.preferred_range = 6  # Medium range - balanced
        self.aggressive = True  # Will close to optimal range
        self.all_ships = []  # Will be set by combat screen
        
    def set_target(self, target_ship):
        """Set the target ship to engage"""
        self.target = target_ship
    
    def select_best_target(self, all_ships):
        """
        Intelligently select the best target from available enemy ships
        
        Args:
            all_ships: List of all ships in combat
            
        Returns:
            Ship object or None
        """
        self.all_ships = all_ships
        
        # Get this ship's faction
        my_faction = getattr(self.ship, 'faction', 'neutral')
        
        # Find all valid enemy targets (different faction, still alive)
        valid_targets = []
        for ship in all_ships:
            if ship == self.ship:
                continue
            
            # Check if ship is alive
            if ship.hull <= 0:
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
            return None
        
        # Select target based on distance and threat level
        best_target = None
        best_score = -999999
        
        for target in valid_targets:
            # Calculate distance
            distance = self.hex_grid.distance(
                self.ship.hex_q, self.ship.hex_r,
                target.hex_q, target.hex_r
            )
            
            # Score based on:
            # - Distance (prefer closer targets)
            # - Damage potential (prefer weaker targets)
            # - Threat level (prefer armed targets)
            
            distance_score = -distance  # Negative because closer is better
            
            # Hull percentage (prefer damaged targets)
            hull_percent = target.hull / target.max_hull
            damage_score = (1.0 - hull_percent) * 50  # Up to +50 for nearly dead
            
            # Weapon count (prefer armed targets)
            weapon_count = len(target.weapon_arrays) + len(target.torpedo_bays)
            threat_score = weapon_count * 10
            
            total_score = distance_score + damage_score + threat_score
            
            if total_score > best_score:
                best_score = total_score
                best_target = target
        
        return best_target
    
    def update_target(self, all_ships):
        """
        Re-evaluate target selection if current target is invalid
        
        Args:
            all_ships: List of all ships in combat
        """
        # If no target or target is dead, select new target
        if not self.target or self.target.hull <= 0:
            self.target = self.select_best_target(all_ships)
            return
        
        # Check if current target is still a valid enemy
        my_faction = getattr(self.ship, 'faction', 'neutral')
        target_faction = getattr(self.target, 'faction', 'neutral')
        
        # If targeting friendly ship, switch targets immediately
        if my_faction == target_faction:
            self.target = self.select_best_target(all_ships)
            return
        
    def decide_movement(self, movement_points):
        """
        Decide how to move this turn with sophisticated tactical AI
        
        Returns:
            list: List of movement commands ['forward', 'turn_left', etc.]
        """
        if not self.target:
            return []
        
        moves = []
        remaining_mp = movement_points
        
        # Calculate current distance to target
        distance = self.hex_grid.distance(
            self.ship.hex_q, self.ship.hex_r,
            self.target.hex_q, self.target.hex_r
        )
        
        # Get target arc
        target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
        
        # Determine strategy based on situation
        hull_percent = self.ship.hull / self.ship.max_hull
        retreat_threshold = getattr(self, 'retreat_threshold', 0.3)
        
        # Check shield status
        shield_percent = 0
        if hasattr(self.ship, 'shields') and hasattr(self.ship, 'max_shields'):
            total_shields = sum(self.ship.shields.values())
            max_total_shields = sum(self.ship.max_shields.values())
            if max_total_shields > 0:
                shield_percent = total_shields / max_total_shields
        
        # If badly damaged and shields down, try to evade
        if hull_percent < retreat_threshold or (hull_percent < 0.5 and shield_percent < 0.2):
            self.aggressive = False
            # Try to back away while keeping weapons on target
            if remaining_mp >= 1:
                # Check if weapons still in arc
                weapons_in_arc = self._check_weapons_in_arc(target_arc)
                if weapons_in_arc:
                    # Back away while maintaining firing solution
                    moves.append('backward')
                    remaining_mp -= 1
                return moves
        
        # Check if target is in arc for any weapons
        weapons_in_arc = self._check_weapons_in_arc(target_arc)
        best_weapon_arcs = self._get_best_weapon_arcs()
        
        # Check if we should rotate shields (PRIORITY CHECK)
        should_rotate, rotate_direction, rotate_reason = self._should_rotate_shields(target_arc)
        
        # Priority 0: Shield rotation if shields are critically weak and we have strong shields available
        if should_rotate and rotate_direction and remaining_mp >= 2:
            # Check if we can afford to rotate (have weapons in arc or will after rotation)
            arc_shields = self._get_shield_strength_by_arc()
            current_shield_percent = arc_shields.get(target_arc, 0) / max(self.ship.max_shields.get(self._arc_to_shield_facing(target_arc), 1), 1)
            
            # Only rotate if shields are critically weak (<30%) or if we're maintaining weapons on target
            if current_shield_percent < 0.3 or weapons_in_arc:
                # Perform shield rotation maneuver
                moves.append('forward')
                remaining_mp -= 1
                moves.append(rotate_direction)
                remaining_mp -= 1
                
                # Log reason for tactical awareness
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"{self.ship.name}: {rotate_reason}")
                
                return moves
        
        # Priority 1: Get weapons on target if not in arc
        if not weapons_in_arc and remaining_mp >= 2:
            # Determine which way to turn to face target
            turn_direction = self._determine_turn_direction()
            
            if turn_direction:
                # Move forward first (required for turning in most systems)
                moves.append('forward')
                remaining_mp -= 1
                
                # Then turn toward target
                moves.append(turn_direction)
                remaining_mp -= 1
                
                # If still have MP and need more turning, keep maneuvering
                if remaining_mp >= 2:
                    # Check if we need another turn (target more than 60° off)
                    import math
                    dx = self.target.position[0] - self.ship.position[0]
                    dy = self.target.position[1] - self.ship.position[1]
                    angle_to_target = math.degrees(math.atan2(dy, dx))
                    if angle_to_target < 0:
                        angle_to_target += 360
                    
                    # Predict facing after one turn
                    new_facing = (self.ship.facing + (1 if turn_direction == 'turn_right' else -1)) % 6
                    new_angle = 90 + (new_facing * 60)
                    new_angle = new_angle % 360
                    
                    diff = angle_to_target - new_angle
                    if diff > 180:
                        diff -= 360
                    elif diff < -180:
                        diff += 360
                    
                    # If still significantly off, do another turn
                    if abs(diff) > 45:
                        moves.append('forward')
                        remaining_mp -= 1
                        moves.append(turn_direction)
                        remaining_mp -= 1
        
        # Priority 2: Optimal range management
        elif distance > self.preferred_range + 3 and self.aggressive:
            # Too far, close in aggressively
            moves_to_make = min(remaining_mp, distance - self.preferred_range)
            for _ in range(moves_to_make):
                if remaining_mp >= 1:
                    moves.append('forward')
                    remaining_mp -= 1
                    
        elif distance < self.preferred_range - 3:
            # Too close, back off while maintaining weapons on target
            moves_to_make = min(remaining_mp, self.preferred_range - distance)
            for _ in range(moves_to_make):
                if remaining_mp >= 1:
                    moves.append('backward')
                    remaining_mp -= 1
                    
        elif distance > self.preferred_range + 1 and self.aggressive:
            # Slightly far, close in a bit
            if remaining_mp >= 1:
                moves.append('forward')
                remaining_mp -= 1
                
        elif distance < self.preferred_range - 1:
            # Slightly close, back off a bit
            if remaining_mp >= 1:
                moves.append('backward')
                remaining_mp -= 1
        
        # Priority 3: Tactical maneuvering at optimal range
        else:
            # At good range, perform tactical maneuvers
            if remaining_mp >= 2:
                # Check shield status - if weak, consider rotating even with weapons on target
                arc_shields = self._get_shield_strength_by_arc()
                current_shield = arc_shields.get(target_arc, 0)
                max_shield = self.ship.max_shields.get(self._arc_to_shield_facing(target_arc), 1) if hasattr(self.ship, 'max_shields') else 1
                current_shield_percent = current_shield / max(max_shield, 1)
                
                # If shields are getting weak (<50%) and we have stronger shields, rotate
                if current_shield_percent < 0.5 and should_rotate and rotate_direction:
                    if random.random() < 0.5:  # 50% chance to prioritize shields over pure offense
                        moves.append('forward')
                        remaining_mp -= 1
                        moves.append(rotate_direction)
                        remaining_mp -= 1
                        return moves
                
                # Check if we should reposition to bring more weapons to bear
                if 'fore' in best_weapon_arcs and target_arc != 'fore':
                    # Try to turn to bring forward weapons to bear
                    turn_direction = self._determine_turn_direction()
                    if turn_direction and random.random() < 0.6:  # 60% chance
                        moves.append('forward')
                        remaining_mp -= 1
                        moves.append(turn_direction)
                        remaining_mp -= 1
                elif remaining_mp >= 2 and random.random() < 0.4:  # 40% chance for evasive maneuvers
                    # Evasive action - move and turn for unpredictability
                    moves.append('forward')
                    remaining_mp -= 1
                    
                    # Turn in semi-random direction (weighted toward target)
                    if random.random() < 0.7:
                        # Turn toward target
                        turn_direction = self._determine_turn_direction()
                        if turn_direction:
                            moves.append(turn_direction)
                    else:
                        # Turn away (evasive)
                        if random.random() < 0.5:
                            moves.append('turn_left')
                        else:
                            moves.append('turn_right')
                    remaining_mp -= 1
        
        return moves
    
    def _check_weapons_in_arc(self, target_arc):
        """Check if any weapons can fire at target arc"""
        for weapon in self.ship.weapon_arrays:
            if target_arc in weapon.firing_arcs:
                return True
        for torpedo in self.ship.torpedo_bays:
            if target_arc in torpedo.firing_arcs:
                return True
        return False
    
    def _get_best_weapon_arcs(self):
        """Get arcs where we have the most/best weapons"""
        arc_scores = {}
        
        for weapon in self.ship.weapon_arrays:
            for arc in weapon.firing_arcs:
                if arc not in arc_scores:
                    arc_scores[arc] = 0
                arc_scores[arc] += weapon.get_damage()
        
        for torpedo in self.ship.torpedo_bays:
            for arc in torpedo.firing_arcs:
                if arc not in arc_scores:
                    arc_scores[arc] = 0
                arc_scores[arc] += torpedo.get_damage() * 0.8  # Torpedoes weighted slightly less
        
        # Return arcs sorted by firepower
        return sorted(arc_scores.keys(), key=lambda a: arc_scores[a], reverse=True)
    
    def _get_shield_strength_by_arc(self):
        """
        Get current shield strength for each arc
        
        Returns:
            dict: {arc: shield_value}
        """
        if not hasattr(self.ship, 'shields'):
            return {}
        
        shields = self.ship.shields
        
        # Map shield facings to hex arcs
        # Fore shield covers fore arc
        # Aft shield covers aft arc
        # Port shield covers port-fore and port-aft
        # Starboard shield covers starboard-fore and starboard-aft
        
        arc_shields = {
            'fore': shields.get('fore', 0),
            'aft': shields.get('aft', 0),
            'port-fore': shields.get('port', 0),
            'port-aft': shields.get('port', 0),
            'starboard-fore': shields.get('starboard', 0),
            'starboard-aft': shields.get('starboard', 0)
        }
        
        return arc_shields
    
    def _should_rotate_shields(self, target_arc):
        """
        Determine if we should rotate to present stronger shields
        
        Args:
            target_arc: Arc where the target is located
            
        Returns:
            tuple: (should_rotate: bool, direction: str or None, reason: str)
        """
        if not hasattr(self.ship, 'shields') or not hasattr(self.ship, 'max_shields'):
            return (False, None, "No shields")
        
        arc_shields = self._get_shield_strength_by_arc()
        current_shield = arc_shields.get(target_arc, 0)
        max_shield_this_arc = self.ship.max_shields.get(self._arc_to_shield_facing(target_arc), 1)
        
        if max_shield_this_arc <= 0:
            return (False, None, "No max shield")
        
        current_percent = current_shield / max_shield_this_arc
        
        # If current shield facing is strong (>60%), don't rotate
        if current_percent > 0.6:
            return (False, None, "Current shields strong")
        
        # If current shield is weak (<40%), consider rotating
        if current_percent < 0.4:
            # Find the strongest shield
            strongest_facing = None
            strongest_value = 0
            strongest_percent = 0
            
            for facing, value in self.ship.shields.items():
                max_val = self.ship.max_shields.get(facing, 1)
                if max_val > 0:
                    percent = value / max_val
                    if value > strongest_value and percent > strongest_percent:
                        strongest_facing = facing
                        strongest_value = value
                        strongest_percent = percent
            
            # If we found a much stronger shield (20%+ better), rotate to it
            if strongest_facing and strongest_percent > current_percent + 0.2:
                # Determine which way to turn to present that shield to target
                target_facing = self._shield_facing_to_arc(strongest_facing)
                
                if target_facing:
                    # Calculate turn direction needed
                    turn_dir = self._calculate_turn_to_present_arc(target_arc, target_facing)
                    if turn_dir:
                        return (True, turn_dir, f"Rotate {strongest_facing} shield ({int(strongest_percent*100)}%) to threat")
        
        return (False, None, "No rotation needed")
    
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
    
    def _shield_facing_to_arc(self, facing):
        """Convert shield facing to best arc to present"""
        facing_map = {
            'fore': 'fore',
            'aft': 'aft',
            'port': 'port-fore',
            'starboard': 'starboard-fore'
        }
        return facing_map.get(facing, 'fore')
    
    def _calculate_turn_to_present_arc(self, current_target_arc, desired_arc):
        """
        Calculate which direction to turn to present desired arc to target
        
        Args:
            current_target_arc: Where target currently is
            desired_arc: Which arc we want to present to target
            
        Returns:
            str: 'turn_left' or 'turn_right' or None
        """
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
            return None  # Already presenting correct arc
        elif diff <= 3:
            return 'turn_right'  # Turn clockwise
        else:
            return 'turn_left'  # Turn counter-clockwise
    
    def _determine_turn_direction(self):
        """
        Determine which direction to turn to face target
        
        Returns:
            str: 'turn_left' or 'turn_right' or None
        """
        if not self.target:
            return None
        
        # Calculate angle to target
        import math
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
        # Positive diff = target is clockwise = turn right
        # Negative diff = target is counter-clockwise = turn left
        if abs(diff) < 30:  # Already facing roughly correct direction
            return None
        elif diff > 0:
            return 'turn_right'
        else:
            return 'turn_left'
    
    def should_fire(self):
        """
        Decide whether to fire weapons this turn
        
        Returns:
            bool: True if should fire, False otherwise
        """
        if not self.target:
            return False
        
        # Calculate distance
        distance = self.hex_grid.distance(
            self.ship.hex_q, self.ship.hex_r,
            self.target.hex_q, self.target.hex_r
        )
        
        # Get target arc
        target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
        
        # Check if any weapons are ready and in arc
        for weapon in self.ship.weapon_arrays:
            if weapon.can_fire() and target_arc in weapon.firing_arcs:
                # Check range (phasers max 12 hexes)
                if distance <= 12:
                    return True
        
        for torpedo in self.ship.torpedo_bays:
            if torpedo.can_fire() and target_arc in torpedo.firing_arcs:
                # Check range (torpedoes max 15 hexes)
                if distance <= 15:
                    return True
        
        return False
    
    def get_combat_report(self):
        """
        Generate a brief status report for debugging
        
        Returns:
            str: Status report
        """
        if not self.target:
            return "AI: No target"
        
        distance = self.hex_grid.distance(
            self.ship.hex_q, self.ship.hex_r,
            self.target.hex_q, self.target.hex_r
        )
        
        target_arc = self.ship.get_target_arc(self.target.hex_q, self.target.hex_r)
        
        hull_percent = int((self.ship.hull / self.ship.max_hull) * 100)
        
        return f"AI: Dist={distance} Arc={target_arc} Hull={hull_percent}% Aggr={self.aggressive}"


class AIPersonality:
    """Different AI personality types for variety"""
    
    AGGRESSIVE = {
        'preferred_range': 4,  # Close range
        'aggressive': True,
        'retreat_threshold': 0.2,  # Only retreat at 20% hull
    }
    
    DEFENSIVE = {
        'preferred_range': 8,  # Long range
        'aggressive': False,
        'retreat_threshold': 0.5,  # Retreat at 50% hull
    }
    
    BALANCED = {
        'preferred_range': 6,  # Medium range
        'aggressive': True,
        'retreat_threshold': 0.3,  # Retreat at 30% hull
    }
    
    SNIPER = {
        'preferred_range': 10,  # Very long range
        'aggressive': False,
        'retreat_threshold': 0.4,  # Retreat at 40% hull
    }
    
    @staticmethod
    def apply_to_ai(ai, personality_name):
        """
        Apply a personality to an AI instance
        
        Args:
            ai: ShipAI instance
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
