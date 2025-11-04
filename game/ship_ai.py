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
        
    def set_target(self, target_ship):
        """Set the target ship to engage"""
        self.target = target_ship
        
    def decide_movement(self, movement_points):
        """
        Decide how to move this turn
        
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
        
        # If badly damaged, try to retreat (not implemented yet, just hold position)
        if hull_percent < 0.3:
            self.aggressive = False
            # For now, just skip movement
            return []
        
        # Check if target is in arc
        weapons_in_arc = False
        for weapon in self.ship.weapon_arrays:
            if target_arc in weapon.firing_arcs:
                weapons_in_arc = True
                break
        
        if not weapons_in_arc:
            for torpedo in self.ship.torpedo_bays:
                if target_arc in torpedo.firing_arcs:
                    weapons_in_arc = True
                    break
        
        # Priority 1: If weapons not in arc, try to turn to face target
        if not weapons_in_arc and remaining_mp >= 2:  # Need MP to move then turn
            # Move forward first (required for turning)
            moves.append('forward')
            remaining_mp -= 1
            
            # Determine which way to turn to face target
            turn_direction = self._determine_turn_direction()
            if turn_direction and remaining_mp >= 1:
                moves.append(turn_direction)
                remaining_mp -= 1
        
        # Priority 2: Adjust range
        elif distance > self.preferred_range + 2 and self.aggressive:
            # Too far, close in
            while remaining_mp >= 1 and distance > self.preferred_range:
                moves.append('forward')
                remaining_mp -= 1
                distance -= 1  # Approximate
                
        elif distance < self.preferred_range - 2:
            # Too close, back off
            while remaining_mp >= 1 and distance < self.preferred_range:
                moves.append('backward')
                remaining_mp -= 1
                distance += 1  # Approximate
                
        else:
            # Good range, maybe do some maneuvering
            if remaining_mp >= 2 and random.random() < 0.3:  # 30% chance
                moves.append('forward')
                remaining_mp -= 1
                
                # Random turn for unpredictability
                if random.random() < 0.5:
                    moves.append('turn_left')
                else:
                    moves.append('turn_right')
                remaining_mp -= 1
        
        return moves
    
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
