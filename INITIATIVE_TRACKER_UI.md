# Initiative Tracker UI - Implementation Summary

## Overview
Added a visual initiative tracking system at the top of the combat screen that displays all ships in turn order with their sprites, along with a dynamic glow effect around the currently active ship.

## Features Implemented

### 1. Initiative Tracker Bar (Top of Screen)
- **Location**: Centered at top of combat arena (Y=70)
- **Components**:
  - Background panel with LCARS-themed border
  - Ship sprites displayed in initiative order
  - Ship names below each sprite (truncated if too long)
  - Initiative values displayed (if available)
  - Current ship indicator with enhanced visual feedback

### 2. Faction-Based Color Coding
The system uses distinct colors based on ship faction:
- **Friendly (Blue)**: Player-controlled ships
  - Glow: Blue (`LCARS_COLORS['blue']`)
  - Border: Green (`LCARS_COLORS['green']`)
- **Hostile (Red)**: Enemy ships
  - Glow: Red (`LCARS_COLORS['alert_red']`)
  - Border: Red (`LCARS_COLORS['alert_red']`)
- **Neutral (White)**: Neutral ships
  - Glow: White (255, 255, 255)
  - Border: Light Blue (`LCARS_COLORS['light_blue']`)

### 3. Active Ship Glow Effect

#### In Initiative Tracker
- Multi-layered circular glow around active ship's icon
- 5 layers with decreasing alpha (opacity)
- Enhanced border thickness (4px vs 2px for inactive)

#### In Combat Arena
- Animated pulsing glow effect around active ship
- 6 layers of circular glows with decreasing radius
- Pulsing animation: 2-second cycle using sine wave
- Radius oscillates between 60-80 pixels
- Color matches faction (blue/red/white)

### 4. Visual Enhancements
- **Ship Sprites**: Scaled down to 40% for tracker (vs full size in arena)
- **Smooth Scaling**: Uses `pygame.transform.smoothscale()` for quality
- **Sprite Caching**: Leverages existing sprite cache system
- **Fallback Graphics**: Simple circles if sprite fails to load

## Technical Implementation

### New Methods Added

#### `_draw_initiative_tracker()`
**Location**: `gui/combat_test_screen.py` (line ~3153)

Draws the initiative order UI at the top of the screen:
- Calculates positioning for centered display
- Iterates through `self.initiative_order` list
- Renders ship sprites at 0.4x scale
- Applies glow effects to current ship
- Displays ship names and initiative values

**Key Features**:
- Dynamic centering based on number of ships
- Graceful fallback for missing sprites
- Faction-aware color selection
- Initiative value display (if attribute exists)

#### `_draw_ship()` Enhancement
**Location**: `gui/combat_test_screen.py` (line ~3288)

Enhanced to include glow effect for active ship:
- Checks if ship matches `get_current_acting_ship()`
- Determines glow color from ship faction
- Creates pulsing animation using `pygame.time.get_ticks()`
- Renders 6 layers of semi-transparent circles
- Glow drawn before ship sprite (behind ship)

**Animation Parameters**:
```python
pulse = (pygame.time.get_ticks() % 2000) / 2000.0  # 2-second cycle
pulse_size = 10 + int(10 * math.sin(pulse * math.pi * 2))  # 10-20px oscillation
alpha = 200 - (i * 30)  # Decreasing opacity per layer
radius = 60 + pulse_size - (i * 8)  # Decreasing radius per layer
```

### Integration Points

#### Main Draw Loop
**Location**: `gui/combat_test_screen.py` `draw()` method

Updated to call initiative tracker:
```python
def draw(self):
    # ... background and panels ...
    
    # Draw initiative tracker at the top
    self._draw_initiative_tracker()
    
    # ... rest of UI ...
```

#### Ship Faction System
Uses existing faction attributes:
- `ship.faction` attribute (set during ship creation)
- Values: `'friendly'`, `'enemy'`, `'neutral'`
- Defaults to `'neutral'` if attribute missing

## Usage

### Automatic Display
The initiative tracker appears automatically during combat:
1. Ships are added to `self.initiative_order` during initiative phase
2. `self.current_ship_index` tracks which ship is acting
3. `get_current_acting_ship()` returns the active ship
4. Tracker updates every frame to show current state

### Visual Feedback
Players can instantly see:
- **Turn Order**: Left-to-right ship sequence
- **Active Ship**: Pulsing glow in tracker + arena
- **Faction Status**: Color-coded borders and glows
- **Initiative Values**: Numerical display below ship names

## Benefits

1. **Clarity**: Players always know whose turn it is
2. **Tactical Awareness**: See full turn order at a glance
3. **Visual Feedback**: Animated glow draws attention to active ship
4. **Faction Recognition**: Color coding prevents friendly fire confusion
5. **Immersion**: LCARS-themed panel matches Star Trek aesthetic

## Future Enhancements

Potential improvements:
- Display initiative roll results temporarily when rolled
- Highlight ships that have already acted this round
- Show action status (moved/fired/etc.) per ship
- Add ship health bars in tracker
- Animate ship icons when they act
- Add tooltips on hover for detailed ship info

## Testing

To test the new UI:
1. Launch the game: `python gui_main.py`
2. Enter Combat Test Arena
3. Observe initiative tracker at top
4. Watch for pulsing glow around active ship
5. Advance through combat phases to see turn changes

## Dependencies

- `pygame-ce 2.5.6`: Graphics rendering
- `gui/lcars_theme.py`: Color schemes
- `gui/hex_grid.py`: Ship positioning
- `game/ship_ai.py`: AI ship management

## Files Modified

1. **gui/combat_test_screen.py**
   - Added `_draw_initiative_tracker()` method
   - Enhanced `_draw_ship()` with glow effect
   - Updated `draw()` to call tracker
   - ~130 new lines of code

## Configuration

Default settings (can be adjusted in code):
```python
# Initiative Tracker
tracker_y = 70           # Y position
ship_icon_size = 50      # Icon diameter
ship_spacing = 120       # Horizontal spacing
tracker_scale = 0.4      # Sprite scale factor

# Glow Effect
pulse_cycle = 2000       # Milliseconds (2 seconds)
base_radius = 60         # Base glow radius
pulse_range = 10         # Radius variation
glow_layers = 6          # Number of glow circles
base_alpha = 200         # Starting opacity
```

## Notes

- Initiative tracker respects existing ship sprite cache for performance
- Glow effects use alpha blending (SRCALPHA) for smooth appearance
- System works with any number of ships (dynamic centering)
- Compatible with multi-hex ships (uses center position)
- No changes required to ship data structures (uses existing attributes)
