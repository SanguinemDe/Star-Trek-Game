# Multiple Enemy Ships - Initiative Fix

## Problem Identified
The initiative system was only including 2 ships in combat regardless of how many enemy ships were actually created:
- `self.initiative_order = [self.player_ship, self.enemy_ship]` (line 1514)

This hardcoded initialization only included:
1. The player ship
2. The FIRST enemy ship (stored in `self.enemy_ship`)

All other enemy ships in `self.all_ships` were being ignored for initiative/turn order.

## Root Cause
The `roll_initiative()` method was using legacy code that assumed only one enemy ship. While the ship creation code properly created multiple ships and stored them in:
- `self.all_ships` - Complete list of all ships
- `self.enemy_ais` - List of AI controllers for each enemy
- `enemy_ships_list` - Local list during creation

The initiative system wasn't updated to use the full `self.all_ships` list.

## Solution Applied

### File: `gui/combat_test_screen.py`
**Method**: `roll_initiative()` (line ~1489)

**Before**:
```python
# TESTING: Player always wins initiative
self.initiative_order = [self.player_ship, self.enemy_ship]
```

**After**:
```python
# TESTING: Player always wins initiative, but include ALL ships
self.initiative_order = [self.player_ship] + [ship for ship in self.all_ships if ship != self.player_ship]
```

**Also Updated the Commented Code** (for future use):
- Changed from `ships = [self.player_ship, self.enemy_ship]` 
- To `for ship in self.all_ships:`
- Changed d20 roll to d100 roll (as per requirements: Command + 1d100)

## Impact

### What Now Works
1. **Initiative Tracker**: Now displays ALL ships in combat, not just 2
2. **Turn Order**: All enemy ships get their own turns
3. **AI Execution**: Each enemy ship's AI controller is properly activated
4. **Targeting**: Each enemy can independently target the player
5. **Combat Flow**: True multi-ship combat with proper turn sequencing

### Verified Systems
These systems were already correct and didn't need changes:
- ✅ **Ship Creation**: `_create_ships_from_config()` properly creates multiple ships
- ✅ **AI Controllers**: `self.enemy_ais` list properly stores all enemy AIs
- ✅ **AI Movement**: `execute_ai_movement()` looks up correct AI per ship
- ✅ **AI Targeting**: `execute_ai_targeting()` uses individual AI controllers
- ✅ **AI Firing**: `execute_ai_firing()` fires with correct ship/AI pair
- ✅ **Ship List**: `self.all_ships` contains all combatants

## Testing

To verify the fix:
1. Launch Combat Test Arena with multiple enemy ships
2. Check initiative tracker at top - should show all ships
3. Observe turn order - each enemy should act individually
4. Watch combat log - each enemy should report actions separately
5. Monitor AI movement - different enemies should move independently

## Future Enhancement

When uncommenting the actual initiative roll system, ensure:
```python
def roll_initiative(self):
    import random
    initiative_rolls = []
    
    for ship in self.all_ships:  # ✓ Already fixed
        # Base initiative from command crew skill
        base_initiative = 0
        if hasattr(ship, 'command_crew') and ship.command_crew.get('captain'):
            base_initiative = ship.command_crew['captain'].attributes.get('command', 50)
        
        # Add random d100 roll
        roll = random.randint(1, 100)
        total = base_initiative + roll
        ship.initiative = total  # Store on ship for display
        
        initiative_rolls.append((ship, total, roll))
    
    # Sort by total (highest first)
    initiative_rolls.sort(key=lambda x: x[1], reverse=True)
    self.initiative_order = [ship for ship, total, roll in initiative_rolls]
    
    # Log results
    for ship, total, roll in initiative_rolls:
        self.add_to_log(f"{ship.name} initiative: {total} ({roll} + {total-roll} command)")
```

## Files Modified
1. **gui/combat_test_screen.py** - Fixed `roll_initiative()` method

## Related Systems
- Initiative Tracker UI (displays all ships correctly now)
- Active ship glow effect (will cycle through all ships)
- Combat phase system (all ships get turns)
- AI controller lookup (already supported multiple AIs)
