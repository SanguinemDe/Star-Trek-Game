# LCARS Theme System Documentation

## Overview

The game now supports multiple LCARS (Library Computer Access/Retrieval System) interface themes that can be switched in the Options menu.

## Available Themes

### LCARS V1 - Classic (TNG Era)
The original LCARS interface style from Star Trek: The Next Generation era.

**Visual Characteristics:**
- Warm color palette with classic LCARS orange
- Rounded corners (25px radius) on all UI elements
- Softer, more pastel tones
- Dark gray-blue backgrounds
- Traditional LCARS aesthetic

**Color Scheme:**
- Primary: Warm orange (255, 153, 0)
- Accents: Classic LCARS blue, purple, peach
- Backgrounds: Dark gray-blue tones
- Text: Soft white and gray

### LCARS V2 - Modern (Discovery/Picard Era)
A modernized LCARS interface inspired by Star Trek: Discovery and Picard.

**Visual Characteristics:**
- Cool color palette with cyan and blue tones
- More angular elements (5px corner radius)
- Sharper, more saturated colors
- Darker blue-black backgrounds
- Contemporary sci-fi aesthetic

**Color Scheme:**
- Primary: Bright amber-orange (255, 138, 51)
- Accents: Vivid cyan-blue, cornflower blue, deep purple
- Backgrounds: Very dark blue-black tones
- Text: Bright blue-white for contrast

## How to Use

### In-Game
1. Launch the game
2. Click "OPTIONS" from the main menu
3. Select your preferred interface style:
   - "INTERFACE: LCARS_V1" for classic theme
   - "INTERFACE: LCARS_V2" for modern theme
4. Theme changes take effect immediately
5. Press "< BACK" to return to main menu

### Technical Implementation

The theme is saved to `settings/options.json` and automatically loaded on game startup.

```json
{
  "theme": "lcars_v2"
}
```

## Developer Notes

### Adding New Themes

To add a new theme variant:

1. **Define color palette** in `gui/lcars_theme.py`:
```python
LCARS_V3_COLORS = {
    'orange': (R, G, B),
    'blue': (R, G, B),
    # ... etc
}
```

2. **Add to available themes**:
```python
AVAILABLE_THEMES = ['lcars_v1', 'lcars_v2', 'lcars_v3']
```

3. **Update set_theme() function**:
```python
elif theme_name == 'lcars_v3':
    LCARS_COLORS.update(LCARS_V3_COLORS)
```

4. **Update UI style** in `gui/components.py` if needed:
```python
def get_corner_radius():
    theme = get_current_theme()
    if theme == 'lcars_v3':
        return 15  # Custom corner radius
    # ... etc
```

### Theme-Aware Components

UI components automatically adapt to the active theme:

- **Buttons**: Corner radius adjusts based on theme (rounded for V1, angular for V2)
- **Panels**: Border styles adapt to theme aesthetic
- **Colors**: All components use LCARS_COLORS dictionary which updates on theme change

### Files Modified

- `gui/lcars_theme.py` - Theme definitions and management functions
- `gui/components.py` - Theme-aware corner radius system
- `gui/options_screen.py` - New options menu with theme selection
- `gui/main_menu.py` - Connected OPTIONS button to options screen
- `gui_main.py` - Loads theme preference on startup, registers options screen

## Theme Comparison

| Feature | LCARS V1 | LCARS V2 |
|---------|----------|----------|
| Era | TNG (2360s) | Discovery/Picard (2250s/2380s) |
| Corner Radius | 25px (rounded) | 5px (angular) |
| Color Tone | Warm | Cool |
| Background | Gray-blue | Blue-black |
| Saturation | Medium | High |
| Inspiration | Classic Trek | Modern Trek |

## Performance

Theme switching is instantaneous with no performance impact. The theme preference is:
- Loaded once at startup
- Saved immediately when changed
- Applied globally across all UI components

## Future Enhancements

Potential additions:
- Voyager-era theme (gold and purple tones)
- Enterprise NX-01 theme (blue and orange)
- Klingon interface theme (red and black)
- Romulan interface theme (green and gray)
- Custom color picker for user-defined themes
- Animation style variants (smooth vs. instant transitions)
- Sound effect themes

## Accessibility

Both themes maintain:
- High contrast ratios for readability
- Color-blind friendly palettes
- Clear visual hierarchy
- Consistent interaction patterns

---

**Last Updated:** November 4, 2025  
**Version:** 1.0.0
