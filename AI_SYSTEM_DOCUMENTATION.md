# Ship AI System Documentation

## Overview

Basic AI system for computer-controlled ships in tactical combat. The AI makes decisions about movement and weapons firing based on tactical situation.

**NEW:** Ships now animate smoothly between hexes instead of jumping instantly!

## Features

### Movement AI

The AI considers:
- **Distance to target**: Tries to maintain optimal weapon range
- **Weapon arcs**: Maneuvers to get weapons in firing arc
- **Hull damage**: Becomes defensive when badly damaged

### Firing AI

The AI will fire when:
- Weapons are ready (not on cooldown)
- Target is in weapon arc
- Target is within weapon range
- Uses all available weapons each turn

### AI Personalities

Four distinct AI personalities are available:

1. **AGGRESSIVE**
   - Preferred range: 4 hexes (close)
   - Always advances
   - Only retreats at 20% hull

2. **DEFENSIVE**
   - Preferred range: 8 hexes (long)
   - Maintains distance
   - Retreats at 50% hull

3. **BALANCED** (default)
   - Preferred range: 6 hexes (medium)
   - Aggressive but tactical
   - Retreats at 30% hull

4. **SNIPER**
   - Preferred range: 10 hexes (very long)
   - Stays at maximum range
   - Retreats at 40% hull

## Implementation

### File Structure

- `game/ship_ai.py` - Core AI logic
- `gui/combat_test_screen.py` - AI integration into combat

### Key Classes

#### ShipAI
Main AI controller class

**Methods:**
- `decide_movement(movement_points)` - Returns list of movement commands
- `should_fire()` - Determines if AI should fire this turn
- `_determine_turn_direction()` - Calculates optimal turn direction

#### AIPersonality
Personality presets for different AI behaviors

**Usage:**
```python
ai = ShipAI(ship, hex_grid)
ai.set_target(target_ship)
AIPersonality.apply_to_ai(ai, 'aggressive')
```

## Movement Decision Logic

1. **Check if badly damaged** - If hull < 30%, become defensive
2. **Priority 1: Get weapons in arc**
   - If weapons not in arc, move forward then turn toward target
3. **Priority 2: Adjust range**
   - If too far from preferred range, move closer
   - If too close, back away
4. **Priority 3: Maneuver**
   - Random evasive maneuvers (30% chance)

## Firing Decision Logic

1. Check if target exists
2. Calculate distance to target
3. For each weapon:
   - Check if ready to fire
   - Check if target in arc
   - Check if target in range
4. Fire if any weapon meets all conditions

## Future Enhancements

Planned improvements:

1. **Tactical Positioning**
   - Utilize terrain/obstacles
   - Protect damaged shield arcs
   - Flanking maneuvers

2. **Target Priority**
   - Focus on weakest target
   - Switch targets based on threat

3. **Special Abilities**
   - Use attack patterns
   - Activate defensive maneuvers
   - Emergency power management

4. **Formation Flying**
   - Coordinate with other AI ships
   - Wingman tactics
   - Cover fire

5. **Difficulty Levels**
   - Easy: Predictable, poor targeting
   - Normal: Current AI
   - Hard: Advanced tactics, perfect accuracy
   - Expert: Optimal play, predictive positioning

## Testing the AI

### In Combat Test Arena

1. Launch game and click "COMBAT TEST"
2. During movement phase:
   - Player moves first (initiative disabled for testing)
   - After player ends movement (ENTER), AI will move automatically
   - Watch enemy ship maneuver toward optimal range
3. During firing phase:
   - Player fires first (SPACE)
   - After player fires, AI will auto-fire after 0.5s delay
   - Combat log shows AI weapon fire

### Changing AI Personality

In `gui/combat_test_screen.py`, line ~137:
```python
AIPersonality.apply_to_ai(self.enemy_ai, 'balanced')
```

Change `'balanced'` to:
- `'aggressive'` - Close range brawler
- `'defensive'` - Long range sniper
- `'sniper'` - Maximum range engagement

### Debug Info

AI status can be checked with:
```python
status = self.enemy_ai.get_combat_report()
```

Returns: `"AI: Dist=12 Arc=fore Hull=85% Aggr=True"`

## Known Limitations

Current AI limitations:

1. **No obstacle avoidance** - AI doesn't navigate around terrain
2. **No shield management** - Doesn't protect weak shield arcs
3. **Simple range logic** - Just moves forward/backward
4. **No power management** - Doesn't adjust power distribution
5. **No retreat** - Retreat logic present but not fully implemented
6. **Single target only** - Can only engage one target at a time

## Performance Notes

- AI decisions are made instantly
- Artificial delays added for visual clarity:
  - Movement completion: 0.5s delay after all moves
  - Firing: 0.5s delay
- No performance impact on combat calculations

## Animation System

### Smooth Movement

Ships now smoothly glide between hexes with animation:

**Features:**
- **Ease-in-out interpolation** - Smooth acceleration/deceleration
- **Configurable speed** - Default 3.0x speed multiplier
- **Queue system** - AI moves execute sequentially with animation
- **Input blocking** - Player can't move during animations

**Technical Details:**
- Animation uses cubic ease-in-out: `t = t * t * (3.0 - 2.0 * t)`
- Updates at 60 FPS via `update(dt)` method
- Hex coordinates updated immediately, visual position interpolated
- Both player and AI ships use same animation system

**Configuration:**
In `combat_test_screen.py` __init__:
```python
self.animation_speed = 3.0  # Higher = faster (default: 3.0)
```

### How It Works

1. **Movement Command** - Player presses WASD or AI decides to move
2. **Position Calculation** - New hex coordinates calculated
3. **Animation Start** - `start_ship_animation()` begins interpolation
4. **Update Loop** - `update(dt)` smoothly moves ship each frame
5. **Completion** - Ship snaps to final position, callback executed

### AI Move Queue

AI moves are queued and executed one at a time:
```python
self.pending_ai_moves = [
    lambda: move_forward(ship),
    lambda: turn_left(ship),
    lambda: move_forward(ship),
]
```

Each move completes its animation before next move starts.
