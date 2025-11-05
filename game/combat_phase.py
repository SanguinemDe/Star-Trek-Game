"""
Combat Phase Enumeration
Replaces magic strings with type-safe enums for combat phases
"""
from enum import Enum, auto


class CombatPhase(Enum):
    """
    Phases of combat in sequential order.
    Each phase represents a distinct stage of the combat turn.
    """
    INITIATIVE = "initiative"      # Roll initiative to determine turn order
    MOVEMENT = "movement"          # Ships move on the hex grid
    TARGETING = "targeting"        # Ships select targets and firing arcs
    FIRING = "firing"              # Ships fire weapons at targets
    DAMAGE = "damage"              # Apply damage, system effects, casualties
    HOUSEKEEPING = "housekeeping"  # End of turn cleanup, cooldowns, regeneration
    
    def __str__(self):
        """Return the phase name in title case"""
        return self.value.title()
    
    @classmethod
    def get_order(cls):
        """
        Returns the phases in their sequential turn order.
        Use this to iterate through combat phases.
        """
        return [
            cls.INITIATIVE,
            cls.MOVEMENT,
            cls.TARGETING,
            cls.FIRING,
            cls.DAMAGE,
            cls.HOUSEKEEPING
        ]
    
    @classmethod
    def next_phase(cls, current_phase):
        """
        Get the next phase in sequence.
        Returns None if current_phase is the last phase (turn ends).
        
        Args:
            current_phase: Current CombatPhase enum value
            
        Returns:
            Next CombatPhase or None if end of turn
        """
        order = cls.get_order()
        try:
            current_index = order.index(current_phase)
            if current_index < len(order) - 1:
                return order[current_index + 1]
            return None  # End of turn
        except ValueError:
            return None


class CombatState(Enum):
    """Overall combat state machine"""
    SETUP = auto()           # Setting up combat
    IN_PROGRESS = auto()     # Combat ongoing
    PLAYER_VICTORY = auto()  # Player won
    ENEMY_VICTORY = auto()   # Enemy won
    RETREAT = auto()         # Player retreated
    DRAW = auto()            # Both sides retreat/destroyed


# Example usage (for documentation):
if __name__ == "__main__":
    print("Combat Phase Order:")
    for i, phase in enumerate(CombatPhase.get_order(), 1):
        print(f"  {i}. {phase}")
    
    print("\nPhase Progression:")
    current = CombatPhase.INITIATIVE
    while current:
        next_phase = CombatPhase.next_phase(current)
        print(f"  {current} -> {next_phase if next_phase else 'END OF TURN'}")
        current = next_phase
