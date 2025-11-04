# Theme System Update - UI Color Adaptation

## Overview
Updated the entire UI to be fully theme-aware, with proper color adaptation between LCARS V1 (classic warm) and LCARS V2 (modern cool) styles.

## Changes Made

### 1. Font System Enhancement
**File:** `gui/lcars_theme.py`

Added sci-fi font management system:
- `get_font(size, bold=False)` - Returns appropriate sci-fi themed fonts
- Searches for custom fonts in `assets/fonts/` directory
- Falls back to system fonts with sci-fi feel (Consolas, Courier New, Arial Narrow, Impact)
- Supports both regular and bold variants

**Font Priority:**
1. Antonio-Bold.ttf / Antonio-Regular.ttf (custom)
2. Orbitron-Bold.ttf / Orbitron-Regular.ttf (custom)
3. Consolas (system - monospace, clean)
4. Courier New (system - monospace, readable)
5. Arial Narrow (system - condensed, modern)
6. Impact (system - bold, geometric)
7. Arial (system - clean fallback)
8. Default pygame font (ultimate fallback)

### 2. Theme-Aware Color Functions
**File:** `gui/lcars_theme.py`

Added helper functions for dynamic color selection:

```python
get_accent_color()    # Primary highlight color
                      # V1: Warm orange (255, 153, 0)
                      # V2: Cool cyan (102, 204, 255)

get_warning_color()   # Medium alert/warning color
                      # V1: Orange (255, 153, 0)
                      # V2: Purple (120, 100, 220)
```

These functions replace hardcoded orange colors throughout the UI.

### 3. Combat Test Screen Updates
**File:** `gui/combat_test_screen.py`

Updated all color references:
- **Title**: Now uses `get_accent_color()`
- **Phase indicators**: Uses `get_accent_color()`
- **Section headers**: All use `get_accent_color()` (Weapons, Power, Damage, etc.)
- **Hull warnings**: Changed from orange to `get_warning_color()`
- **Shield warnings**: Changed from orange to `get_warning_color()`
- **Targeting lines**: Secondary targets use `get_warning_color()`
- **Combat log title**: Uses `get_accent_color()`
- **Fonts**: Now uses `get_font()` with bold variants

### 4. Menu Screens Updates
**Files:** `gui/main_menu.py`, `gui/options_screen.py`

- Updated font initialization to use `get_font()`
- All screens now use sci-fi themed fonts with proper bold styling

### 5. UI Components Updates
**File:** `gui/components.py`

**TabbedPanel:**
- Active tab color: Uses `get_accent_color()` instead of hardcoded orange
- Tab borders: Uses `get_accent_color()`
- Content borders: Uses `get_accent_color()`

**Button:**
- Already uses dynamic corner radius based on theme
- V1: 25px radius (rounded)
- V2: 5px radius (angular)

## Visual Changes by Theme

### LCARS V1 (Classic)
- **Accent Color**: Warm orange (#FF9900)
- **Warning Color**: Orange (#FF9900)
- **Font Style**: Bold, geometric (Consolas/Impact preferred)
- **Corner Radius**: 25px (rounded)
- **Overall Feel**: Warm, classic TNG era

### LCARS V2 (Modern)
- **Accent Color**: Bright cyan (#66CCFF)
- **Warning Color**: Deep purple (#7864DC)
- **Font Style**: Bold, condensed (Consolas/Arial Narrow preferred)
- **Corner Radius**: 5px (angular)
- **Overall Feel**: Cool, modern Discovery/Picard era

## Color Mapping Changes

| UI Element | Old Color | V1 Color | V2 Color |
|------------|-----------|----------|----------|
| Titles | Orange | Orange | Cyan |
| Headers | Orange | Orange | Cyan |
| Phase indicators | Orange | Orange | Cyan |
| Hull warning (50-75%) | Orange | Orange | Purple |
| Shield warning (25-50%) | Orange | Orange | Purple |
| Tab highlights | Orange | Orange | Cyan |
| Borders | Orange | Orange | Cyan |
| Secondary targets | Orange | Orange | Purple |

## Files Modified

1. `gui/lcars_theme.py` - Added font system and color helper functions
2. `gui/combat_test_screen.py` - Updated all colors and fonts
3. `gui/main_menu.py` - Updated fonts
4. `gui/options_screen.py` - Updated fonts
5. `gui/components.py` - Made TabbedPanel theme-aware

## Installation Notes

### Optional: Custom Fonts
To use custom sci-fi fonts, place font files in `assets/fonts/`:
- `Antonio-Bold.ttf`
- `Antonio-Regular.ttf`
- `Orbitron-Bold.ttf`
- `Orbitron-Regular.ttf`

The system will automatically detect and use them. If not present, it falls back to system fonts.

### Font Sources
- **Antonio**: https://fonts.google.com/specimen/Antonio
  - Geometric sans-serif, excellent for sci-fi displays
  - Free under Open Font License
- **Orbitron**: https://fonts.google.com/specimen/Orbitron
  - Futuristic geometric sans-serif
  - Free under Open Font License

## Testing

All UI screens now properly adapt to theme changes:
1. Main Menu - Uses theme fonts and colors
2. Options Menu - Allows theme switching, uses theme fonts
3. Combat Test Arena - All panels, tabs, and text adapt to theme
4. Status panels - Tabs and content use theme colors
5. Combat log - Uses theme accent colors

## Benefits

1. **Consistency**: All UI elements now respect the active theme
2. **Readability**: Sci-fi fonts maintain readability while adding style
3. **Visual Coherence**: V2 theme now properly uses cool colors throughout
4. **Maintainability**: Centralized color functions make future changes easier
5. **Performance**: No impact, colors calculated once per frame

## Future Enhancements

Potential additions:
- Theme-specific animation speeds
- Theme-specific sound effects
- Additional font options (Michroma, Quantico, etc.)
- Per-element font size scaling for different themes
- Theme preview images in options menu

---

**Last Updated:** November 4, 2025  
**Version:** 1.1.0
