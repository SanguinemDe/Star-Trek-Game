# Ship AI - Quick Reference Guide

## Basic Usage

### Initialize AI for a Ship
```python
from game.ship_ai import ShipAI, AIPersonality

# Create AI controller
ai = ShipAI(ship, hex_grid)

# Set initial target
ai.set_target(enemy_ship)

# Apply personality
AIPersonality.apply_to_ai(ai, 'balanced')
```

### In Combat Loop

```python
# TARGETING PHASE
ai.update_target(all_ships)  # Refresh target if invalid
target = ai.target

# MOVEMENT PHASE
moves = ai.decide_movement(movement_points)
for move in moves:
    if move == 'forward':
        move_forward(ship)
    elif move == 'backward':
        move_backward(ship)
    elif move == 'turn_left':
        turn_left(ship)
    elif move == 'turn_right':
        turn_right(ship)

# FIRING PHASE
if ai.should_fire():
    fire_weapons(ship, ai.target)
```

## Personalities

### Aggressive
```python
AIPersonality.apply_to_ai(ai, 'aggressive')
```
- **Range:** 4 hexes (close combat)
- **Behavior:** Charges at enemies
- **Retreat:** Only at 20% hull

### Defensive
```python
AIPersonality.apply_to_ai(ai, 'defensive')
```
- **Range:** 8 hexes (long range)
- **Behavior:** Maintains distance
- **Retreat:** At 50% hull

### Balanced (Default)
```python
AIPersonality.apply_to_ai(ai, 'balanced')
```
- **Range:** 6 hexes (medium range)
- **Behavior:** Standard tactics
- **Retreat:** At 30% hull

### Sniper
```python
AIPersonality.apply_to_ai(ai, 'sniper')
```
- **Range:** 10 hexes (very long range)
- **Behavior:** Kites enemies
- **Retreat:** At 40% hull

## Movement Commands

The AI returns a list of movement commands:

- `'forward'` - Move 1 hex forward
- `'backward'` - Move 1 hex backward
- `'turn_left'` - Rotate 60° counter-clockwise
- `'turn_right'` - Rotate 60° clockwise

**Example:**
```python
moves = ai.decide_movement(5)
# Returns: ['forward', 'turn_right', 'forward', 'forward']
```

## Combat Report

Get status summary:
```python
report = ai.get_combat_report()
print(report)
# Output: "USS Miranda-1: Target=Enterprise Dist=8 Arc=fore Hull=85%"
```

## Required Ship Attributes

Ships must have:
```python
ship.hex_q           # Hex Q coordinate (int)
ship.hex_r           # Hex R coordinate (int)
ship.facing          # Facing direction 0-5 (int)
ship.hull            # Current hull points (float)
ship.max_hull        # Maximum hull points (float)
ship.position        # (x, y) pixel position (tuple)
ship.shields         # Shield values by facing (dict)
ship.max_shields     # Max shield values (dict)
ship.weapon_arrays   # List of WeaponArray objects
ship.torpedo_bays    # List of TorpedoBay objects
ship.faction         # Faction identifier (string)
```

Ships must have methods:
```python
ship.get_target_arc(q, r)  # Returns arc where target is ('fore', 'aft', etc.)
```

Weapons must have:
```python
weapon.can_fire()      # Returns True if ready to fire
weapon.firing_arcs     # List of arcs weapon can fire in
```

## Debugging

### Enable Logging
```python
from game.logger import get_logger
logger = get_logger(__name__)

# Logs are automatically written to logs/game.log
```

### Check AI State
```python
print(f"Target: {ai.target}")
print(f"Preferred Range: {ai.preferred_range}")
print(f"Aggressive: {ai.aggressive}")
print(f"Retreat Mode: {ai.retreat_mode}")
print(f"Retreat Threshold: {ai.retreat_threshold}")
```

### Validate Ship Setup
```python
def validate_ship_for_ai(ship):
    """Check if ship has all required attributes"""
    required = ['hex_q', 'hex_r', 'facing', 'hull', 'max_hull', 
                'position', 'shields', 'max_shields', 'weapon_arrays', 
                'torpedo_bays', 'faction']
    
    for attr in required:
        if not hasattr(ship, attr):
            print(f"ERROR: Ship missing {attr}")
            return False
    
    print("Ship is valid for AI control")
    return True
```

## Common Issues

### AI Not Moving
**Problem:** `decide_movement()` returns empty list  
**Solution:** Check ship has hex_q, hex_r, and valid target

### AI Not Firing
**Problem:** `should_fire()` returns False  
**Solution:** Check weapon range, arc, and cooldown

### AI Attacking Friendlies
**Problem:** Ships same faction attacking each other  
**Solution:** Ensure ships have different `faction` attributes

### AI Selecting No Target
**Problem:** `select_best_target()` returns None  
**Solution:** Verify enemy ships are alive, different faction

## Performance Tips

1. **Reuse AI instances** - Don't create new AI every turn
2. **Cache target selection** - Only call `update_target()` when needed
3. **Limit AI ships** - More than 10 AIs may impact FPS
4. **Disable debug logging** - In production, set log level to WARNING

## Example: Full Combat Setup

```python
from game.ship_ai import ShipAI, AIPersonality

# Initialize combat
player_ship = create_player_ship()
enemy_ships = [create_enemy_ship() for _ in range(3)]
all_ships = [player_ship] + enemy_ships

# Create AIs for enemies
enemy_ais = []
for enemy in enemy_ships:
    ai = ShipAI(enemy, hex_grid)
    ai.set_target(player_ship)
    AIPersonality.apply_to_ai(ai, 'balanced')
    enemy_ais.append(ai)

# Combat loop
while combat_active:
    for ship in all_ships:
        # Skip player ship (human controlled)
        if ship == player_ship:
            continue
        
        # Find AI for this ship
        ship_ai = None
        for ai in enemy_ais:
            if ai.ship == ship:
                ship_ai = ai
                break
        
        if not ship_ai:
            continue
        
        # Update target
        ship_ai.update_target(all_ships)
        
        # Execute AI turn
        moves = ship_ai.decide_movement(ship.impulse_speed)
        execute_moves(ship, moves)
        
        if ship_ai.should_fire():
            fire_weapons(ship, ship_ai.target)
```

## API Reference

### ShipAI Class

#### Constructor
```python
ShipAI(ship, hex_grid)
```

#### Methods
```python
set_target(target_ship)                    # Manually set target
select_best_target(all_ships)              # Choose best enemy
update_target(all_ships)                   # Refresh target validity
decide_movement(movement_points)           # Get movement commands
should_fire()                              # Check if should fire
get_combat_report()                        # Get status string
```

### AIPersonality Class

#### Static Method
```python
AIPersonality.apply_to_ai(ai, personality_name)
```

#### Personalities
- `'aggressive'` - Close range fighter
- `'defensive'` - Long range kiter
- `'balanced'` - Medium range tactician
- `'sniper'` - Very long range attacker

---

**Quick Start:** Copy the "Full Combat Setup" example and modify for your needs!
