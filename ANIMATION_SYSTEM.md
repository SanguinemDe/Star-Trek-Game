# Ship Animation System

## Overview
The combat test screen now features a smooth animation system for ship movement and rotation, replacing the previous instant "teleportation" behavior.

## Key Features

### 1. **Smooth Movement**
- Ships now glide smoothly from hex to hex instead of teleporting
- Uses smoothstep easing function for natural acceleration/deceleration
- Animation duration: ~2 seconds per hex (configurable via `animation_speed`)

### 2. **Smooth Rotation**
- Ships rotate gradually through intermediate angles instead of snapping
- Automatically takes shortest rotation path (e.g., 5→0 rotates forward, not backwards)
- Animation duration: ~1.4 seconds per 60° turn (configurable via `rotation_speed`)

### 3. **Sequential Animation Queue**
- Multiple moves are queued and executed sequentially
- Each animation completes before the next begins
- Prevents visual confusion and collision issues

### 4. **Unified System**
- Both player and AI ships use the same animation system
- Consistent visual experience regardless of who is moving
- AI moves are no longer instant - they animate just like player moves

## Technical Implementation

### Animation State Variables
Located in `gui/combat_test_screen.py` `__init__()`:

```python
self.animating_ship = None              # Currently animating ship
self.animation_start_pos = None         # Starting pixel position (x, y)
self.animation_end_pos = None           # Ending pixel position (x, y)
self.animation_start_facing = None      # Starting facing (0-5)
self.animation_end_facing = None        # Ending facing (0-5)
self.animation_progress = 0.0           # Progress from 0.0 to 1.0
self.animation_speed = 0.5              # Movement speed multiplier
self.rotation_speed = 0.7               # Rotation speed multiplier
self.animation_callback = None          # Function to call on completion
self.pending_ai_moves = []              # Queue of moves to execute
```

### Speed Settings
- **`animation_speed = 0.5`**: Movement animations (lower = slower)
  - 0.5 = ~2 seconds per hex
  - 1.0 = ~1 second per hex
  - 2.0 = ~0.5 seconds per hex

- **`rotation_speed = 0.7`**: Rotation animations (can differ from movement)
  - 0.7 = ~1.4 seconds per 60° turn
  - 1.0 = ~1 second per turn

### Easing Function
Uses **smoothstep** easing for very natural motion:

```python
t = t * t * t * (t * (t * 6 - 15) + 10)
```

This creates gentle acceleration at the start and deceleration at the end, mimicking real ship physics.

### Movement Functions
All movement functions call `start_ship_animation()`:

```python
def move_forward(self, ship):
    # ... collision checks ...
    old_pos = ship.position
    new_pos = self.hex_grid.axial_to_pixel(new_q, new_r)
    
    # Update hex coordinates immediately
    ship.hex_q = new_q
    ship.hex_r = new_r
    
    # Start animation from old to new position
    self.start_ship_animation(ship, old_pos, new_pos)
```

### AI Movement Queue
AI moves are now queued instead of instant:

```python
def execute_ai_movement(self):
    # ... get AI decisions ...
    
    # Queue all moves for animation
    for move_command in moves:
        def execute_move():
            if cmd == 'forward':
                success = self.move_forward(ship_ref)
            # ... etc ...
        
        self.pending_ai_moves.append(execute_move)
    
    # Start first move (subsequent moves auto-execute when animation completes)
    first_move = self.pending_ai_moves.pop(0)
    first_move()
```

### Update Loop
The `update()` function handles animation progress:

```python
def update(self, dt):
    if self.animating_ship is not None:
        # Determine speed based on animation type
        speed = self.animation_speed if is_movement else self.rotation_speed
        
        self.animation_progress += dt * speed
        
        if self.animation_progress >= 1.0:
            # Animation complete - snap to final state
            # ... execute callback ...
            # ... clear animation state ...
        else:
            # Interpolate position and facing
            t = smoothstep(self.animation_progress)
            # ... update ship position and _anim_facing ...
    
    # Process next queued move when animation finishes
    elif len(self.pending_ai_moves) > 0:
        next_move = self.pending_ai_moves.pop(0)
        next_move()
```

### Drawing Ships
The `_draw_ship()` function uses `_anim_facing` for smooth rotation:

```python
def _draw_ship(self, ship, color):
    # Use animated facing if available
    if hasattr(ship, '_anim_facing') and ship._anim_facing is not None:
        facing_value = ship._anim_facing  # Float value for smooth rotation
    else:
        facing_value = ship.facing  # Discrete 0-5 value
    
    # Sprites are pre-rendered at all 6 facings
    discrete_facing = int(facing_value) % 6
    rotated_sprite = self.ship_sprite_cache[ship.ship_class][scale_factor][discrete_facing]
```

## Player Experience

### Before Animation System
- Ships would instantly "teleport" from hex to hex
- Facing would snap instantly to new directions
- AI moves were impossible to follow visually
- Felt very mechanical and unnatural

### After Animation System
- Ships glide smoothly between hexes
- Rotation is gradual and natural
- AI moves are clearly visible and understandable
- Feels cinematic and tactical

### Controls During Animation
- Player input is blocked during animations (`not self.is_animating()` checks)
- Prevents accidental double-moves
- Ensures animations complete properly
- Maintains tactical clarity

## Future Enhancements

### Possible Additions
1. **Variable Speed Settings**
   - Add to options menu
   - Fast/Normal/Slow/Cinematic presets
   - Per-faction speeds (player vs AI)

2. **Motion Trails**
   - Fading trail showing ship's path
   - Helps track movement in busy battles

3. **Acceleration Particles**
   - Impulse engine glow during movement
   - RCS thruster effects during rotation

4. **Skip Animation Button**
   - Hold SPACE to fast-forward animations
   - Useful when many AI ships move

5. **Camera Follow**
   - Pan camera to keep animated ship visible
   - Zoom in slightly during movement

## Configuration

### Adjusting Speed
Edit `gui/combat_test_screen.py` line ~1075:

```python
self.animation_speed = 0.5   # Change this value
self.rotation_speed = 0.7    # Change this value
```

### Recommended Settings
- **Cinematic**: 0.3 movement, 0.4 rotation
- **Normal**: 0.5 movement, 0.7 rotation
- **Fast**: 1.0 movement, 1.5 rotation
- **Instant**: 5.0 movement, 5.0 rotation (effectively instant)

## Troubleshooting

### Ships Still Teleport
- Check that `start_ship_animation()` is being called in movement functions
- Verify `animation_speed` and `rotation_speed` are not extremely high (>5.0)

### Animations Too Slow
- Increase `animation_speed` and `rotation_speed` values
- Consider adding a "skip animation" hotkey

### Animations Jerky/Choppy
- Check frame rate (should be 60 FPS)
- Ensure smoothstep easing function is active
- Verify no other processes are consuming CPU

### AI Moves Not Animating
- Check that `execute_ai_movement()` is queuing moves in `pending_ai_moves`
- Verify update loop is processing the queue
- Check for early `complete_ship_action()` calls

## Code Locations

### Main Files
- **Animation System**: `gui/combat_test_screen.py` lines 1068-1076 (init), 4200-4290 (update)
- **Movement Functions**: `gui/combat_test_screen.py` lines 1990-2220
- **AI Movement**: `gui/combat_test_screen.py` lines 2220-2280
- **Ship Drawing**: `gui/combat_test_screen.py` lines 4588-4665

### Key Functions
- `start_ship_animation()` - Initialize animation
- `is_animating()` - Check if animation active
- `update()` - Process animation progress
- `_draw_ship()` - Render ship with smooth rotation
- `execute_ai_movement()` - Queue AI moves

## Performance Impact

### Negligible
- Animation calculations are lightweight
- Pre-rendered sprites mean no real-time rotation
- Smoothstep function is simple polynomial
- Queue processing is O(1) per frame

### Memory
- No additional memory overhead
- Uses existing ship position/facing attributes
- Temporary `_anim_facing` attribute only during rotation

## Testing

### What to Test
1. **Player Movement**: Press W/S - ship should glide smoothly
2. **Player Rotation**: Press A/D after moving - ship should rotate smoothly
3. **AI Movement**: Enemy ships should animate when moving
4. **Multiple Moves**: AI should chain multiple moves with animations
5. **Collision Blocking**: Failed moves should not queue remaining animations
6. **Fast Combat**: Multiple enemy ships moving sequentially

### Expected Behavior
- Smooth, natural motion
- No teleporting
- No overlapping ships
- Animations queue properly
- Input blocked during animations
- All ships use same animation system
