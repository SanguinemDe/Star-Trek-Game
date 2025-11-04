# Star Trek Game - GUI Installation Guide

## Pygame Installation Issue

**Problem:** Pygame doesn't have pre-built wheels for Python 3.14 yet (released November 2024).

**Solutions:**

### Option 1: Use Python 3.11 or 3.12 (Recommended)
1. Install Python 3.12 from python.org
2. Run: `python -m pip install pygame`
3. Run the GUI: `python gui_main.py`

### Option 2: Wait for Pygame to Support 3.14
Pygame typically releases new builds a few months after Python releases.
Check: https://pypi.org/project/pygame/

### Option 3: Use Tkinter (Built-in Alternative)
Tkinter comes with Python and works with all versions.
**Note:** I've created the Pygame version for better graphics and LCARS styling.
If you need immediate GUI support, I can create a Tkinter version instead.

## What's Been Created

### GUI Package Structure
```
gui/
├── __init__.py
├── lcars_theme.py        - LCARS color scheme and constants
├── components.py         - Reusable UI widgets (Button, Panel, TextInput, etc.)
├── main_menu.py          - Main menu screen with LCARS styling
└── character_creation.py - Full character creation interface
```

### Features Implemented

**Main Menu:**
- ✅ LCARS-styled interface with Federation colors
- ✅ Mouse-driven buttons (New Game, Load Game, Options, Quit)
- ✅ Animated panels and real-time stardate display
- ✅ Professional Star Trek aesthetic

**Character Creation:**
- ✅ Name input field with cursor
- ✅ Species dropdown (9 Federation species)
- ✅ Attribute sliders (Tactical, Science, Engineering, Diplomacy, Command)
- ✅ Real-time preview panel
- ✅ Visual attribute bars
- ✅ Species descriptions
- ✅ Point allocation system
- ✅ Back and Create buttons

**UI Components:**
- ✅ Button (with hover and press states)
- ✅ Panel (rounded rectangles with borders)
- ✅ TextInput (with cursor and placeholder)
- ✅ Slider (for numeric values)
- ✅ DropdownMenu (with expansion animation)

## Testing Once Pygame is Installed

```bash
python gui_main.py
```

This will launch the graphical interface!

## Next Steps (After Pygame Works)

1. **LCARS Main Game Screen** - Galaxy map, ship status, navigation
2. **Hex-Based Star Map** - Visual navigation with mouse controls
3. **Ship Status Panel** - Graphical hull/shields/systems display
4. **Combat Visualization** - Animated combat sequences
5. **Space Station Interface** - Docking and services
6. **Crew Management** - Visual crew roster

## Alternative: Tkinter Version

Would you like me to create a Tkinter version that will work immediately with Python 3.14?
It won't have the same smooth LCARS styling, but it will be functional.

Let me know which approach you prefer!
