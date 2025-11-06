# Collision Detection and AI Movement Refactor

## Date: November 6, 2025

## Problem Statement

1. **Ad-hoc Collision Detection**: Collision checking was scattered throughout `combat_test_screen.py` rather than being part of the ship's architecture
2. **AI Under-utilization of Movement Points**: AI ships with 7 movement points were only using 1-5 moves due to:
   - Random gates blocking movement generation
   - Early returns from `decide_movement()` function
   - No loop to ensure all MP are used

## Solutions Implemented

### 1. Ship-Based Collision Detection Architecture

**File**: `game/advanced_ship.py`

Added two new methods to `AdvancedShip` class:

```python
def would_collide_at(self, new_q, new_r, all_ships):
    """
    Check if moving to new position would cause collision with any ship
    
    Args:
        new_q, new_r: Target hex coordinates (center hex for multi-hex ships)
        all_ships: List of all ships in combat (including self)
        
    Returns:
        (would_collide: bool, blocking_ship: Ship or None, colliding_hexes: list)
    """
    
def can_move_to(self, new_q, new_r, all_ships):
    """
    Simplified collision check - returns True if move is legal
    
    Args:
        new_q, new_r: Target hex coordinates
        all_ships: List of all ships in combat
        
    Returns:
        bool: True if can move to position without collision
    """
```

**Benefits**:
- Collision detection logic lives with the ship itself
- Multi-hex ships (Very Large/Huge with 7 hexes) automatically check ALL occupied hexes
- Reusable across any combat system
- Single source of truth for collision rules
- Can be extended for future features (terrain, asteroids, etc.)

### 2. Aggressive AI Movement Logic

**File**: `game/ship_ai.py`

Replaced the randomized, gated movement logic in `decide_movement()` Priority 5 section:

**OLD LOGIC** (Lines 391-434):
- Multiple `if/elif` with random checks
- Only triggered movement if random roll succeeded
- Often left 3-6 movement points unused
- Early returns prevented using remaining MP

**NEW LOGIC**:
- **`while remaining_mp > 0` loop** ensures ALL movement points are used
- Prioritizes evasive turns (harder to hit: +5% defense per hex moved)
- Aggressive personalities make tactical advances
- Final MP used for positioning or weapon arc adjustment
- No random gates blocking movement generation

**Combat Behavior Changes**:
- Small ships now stay highly mobile (key tactical advantage vs large ships)
- AI uses 6-7 moves consistently instead of 1-4
- Evasive maneuvers make AI harder to hit
- More dynamic, unpredictable movement patterns

### 3. Combat Screen Integration

**File**: `gui/combat_test_screen.py`

**Updated Methods**:
- `move_forward()`: Now calls `ship.would_collide_at()` instead of local method
- `move_backward()`: Now calls `ship.would_collide_at()` instead of local method
- `would_collide_multi_hex()`: Marked as DEPRECATED, kept for backward compatibility

**Changes**:
```python
# OLD
would_collide, blocking_ship, colliding_hexes = self.would_collide_multi_hex(ship, new_q, new_r)

# NEW
would_collide, blocking_ship, colliding_hexes = ship.would_collide_at(new_q, new_r, self.all_ships)
```

## Testing Notes

Test the following scenarios:

1. **Multi-hex Collision**: 
   - Very Large/Huge ships should block all 7 hexes
   - AI should not be able to move through any occupied hex
   - Player ship should be blocked from moving into any occupied hex

2. **AI Movement Aggressiveness**:
   - Check `combat_log.txt` for AI decision logging
   - AI should use 6-7 movement points per turn (not 1-4)
   - Look for messages: "Evasive maneuver", "Aggressive tactical move", "Final positioning"
   - Small ships should be highly mobile and hard to pin down

3. **Combat Balance**:
   - AI should be more challenging (harder to hit, more tactical)
   - Small ships vs large ships = mobility advantage working as intended
   - Balanced AI personality should use aggressive=True behavior

## Expected Combat Log Output

```
DEBUG: Asking AI to decide movement with 7 MP
DEBUG: AI settings - preferred_range:6, aggressive:True, evasion:0.5
DEBUG: Distance to target: 7, Target in arc: fore
Excelsior2-1: Closing to optimal range (currently 7, want 6)
Excelsior2-1: Evasive maneuver (4 MP left)
Excelsior2-1: Aggressive tactical move (2 MP left)
Excelsior2-1: Final positioning (1 MP left)
DEBUG: AI decided on 7 moves: ['forward', 'forward', 'turn_right', 'forward', 'turn_left', 'forward']
```

## Architecture Improvements

### Before:
```
Combat Screen
    └─ would_collide_multi_hex()  ← Ad-hoc collision logic
    └─ move_forward()             ← Calls local collision method
    └─ move_backward()            ← Calls local collision method
```

### After:
```
AdvancedShip
    └─ would_collide_at()    ← Authoritative collision detection
    └─ can_move_to()         ← Simplified boolean check
    └─ get_occupied_hexes()  ← Already existed, now used by above

Combat Screen
    └─ move_forward()        ← Calls ship.would_collide_at()
    └─ move_backward()       ← Calls ship.would_collide_at()
```

## Future Enhancements

Now that collision detection is in the ship class:

1. **Terrain/Hazards**: Extend `would_collide_at()` to check nebulas, asteroids, etc.
2. **Formation Movement**: Ships can query each other for formation positioning
3. **Pathfinding**: AI can use `can_move_to()` for A* pathfinding around obstacles
4. **Tactical Assessment**: AI can evaluate "safe" hexes without actually moving
5. **Collision Prediction**: Show player where they CAN'T move with red overlay

## Code Quality Notes

- **Single Responsibility**: Each method has one clear purpose
- **Encapsulation**: Ship knows its own collision rules
- **Testability**: Collision logic can be unit tested independently
- **Maintainability**: Future collision rules added in one place
- **Logging Preserved**: All debug logging kept as requested by user
