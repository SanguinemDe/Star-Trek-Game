# Star Trek: Federation Command - Project Structure

## Quick Navigation

### 🚀 Getting Started
- **README.md** - Main documentation, features, and installation
- **QUICKSTART.md** - Quick start guide for new players
- **requirements.txt** - Python dependencies (Pygame)

### 🎮 Running the Game
```powershell
# Install dependencies
pip install -r requirements.txt

# Launch game
python main.py
```

### ⚔️ Combat System Documentation
- **COMBAT_TEST_ARENA_GUIDE.md** - Complete combat mechanics and controls
- **AI_SYSTEM_DOCUMENTATION.md** - AI behavior and personalities

### 🛸 Ship Systems
- **SHIP_SYSTEM.md** - Ship progression and requisition system
- **MARK_SYSTEM_DOCUMENTATION.md** - Mk I-XV equipment system
- **SENSOR_SYSTEM_DOCUMENTATION.md** - Sensor mechanics
- **FIRE_RATE_SYSTEM.md** - Weapon cooldown and fire rates
- **SYSTEMS_DAMAGE.md** - Damage control system

### 👥 Crew & Missions
- **CREW_SYSTEM.md** - Bridge officer recruitment and bonuses
- **MISSION_SYSTEM.md** - Mission types and rewards
- **MISSION_UPDATE.md** - Latest mission features

### 🔧 Development
- **PROJECT_OVERVIEW.md** - Technical overview and architecture
- **CLEANUP_SUMMARY.md** - Recent code organization work
- **CHANGELOG.md** - Version history and updates
- **GUI_README.md** - GUI development notes

---

## Directory Structure

```
Star Trek Game/
│
├── 📄 main.py                      # Main entry point
├── 📄 gui_main.py                  # GUI application controller
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 game/                        # Core game logic
│   ├── 📄 __init__.py
│   ├── 📄 advanced_ship.py        # Ship class with all systems
│   ├── 📄 ship_ai.py              # AI controller for ships
│   ├── 📄 equipment.py            # Mk I-XV equipment system
│   ├── 📄 character.py            # Character creation
│   ├── 📄 galaxy.py               # Galaxy generation
│   ├── 📄 missions.py             # Mission system
│   ├── 📄 crew.py                 # Officer classes
│   ├── 📄 crew_recruitment.py     # Officer recruitment
│   ├── 📄 ship_requisition.py     # Ship purchase system
│   ├── 📄 combat.py               # Combat logic
│   ├── 📄 diplomacy.py            # Faction relations
│   ├── 📄 navigation.py           # Navigation system
│   └── 📁 ships/                  # Ship catalogues
│       ├── 📄 __init__.py
│       └── 📄 federation.py       # 64 Federation ship templates
│
├── 📁 gui/                         # GUI components (LCARS theme)
│   ├── 📄 __init__.py
│   ├── 📄 lcars_theme.py          # LCARS color scheme and constants
│   ├── 📄 components.py           # Reusable UI widgets
│   ├── 📄 hex_grid.py             # Hex grid mathematics
│   ├── 📄 main_menu.py            # Main menu screen
│   ├── 📄 character_creation.py   # Character creation screen
│   ├── 📄 galaxy_map_screen.py    # Galaxy map screen
│   └── 📄 combat_test_screen.py   # Combat arena (1700+ lines!)
│
├── 📁 assets/                      # Game assets
│   └── 📁 Ships/                  # Ship sprites
│       └── 📁 Federation/         # Federation ship sprites
│           └── �️ OdysseyClass.png  # Odyssey-class sprite (1024x1024)
│
├── 📁 _archive/                    # Archived development files
│   ├── 📄 test_*.py               # Test scripts (obsolete)
│   ├── 📄 convert_*.py            # Conversion utilities (used)
│   └── 📄 *_SUMMARY.md            # Historical documentation
│
└── 📁 __pycache__/                 # Python cache (auto-generated)
```

---

## Key Files Explained

### Entry Points

**`main.py`** (54 lines)
- Main game launcher
- Error handling and dependency checking
- Imports and starts `gui_main.py`

**`gui_main.py`** (171 lines)
- Pygame initialization
- Screen management (main menu, character creation, galaxy map, combat)
- Main game loop (60 FPS)
- Event handling coordination

### Combat System

**`gui/combat_test_screen.py`** (1712 lines) ⭐ LARGEST FILE
- Complete tactical combat arena
- 8-phase turn system
- Hex grid with smooth animation
- Multi-targeting system
- Shield arc damage
- AI opponent control
- Tabbed UI panels (STATUS/WEAPONS/POWER/DAMAGE)
- WASD movement controls

**`game/ship_ai.py`** (273 lines)
- AI decision-making for enemy ships
- Movement strategy (range management, arc positioning)
- Firing logic
- 4 personalities: Aggressive, Defensive, Balanced, Sniper

**`gui/hex_grid.py`** (268 lines)
- Hexagonal grid mathematics
- Axial coordinate system
- Pixel ↔ hex conversion
- Distance calculations
- Neighbor finding

### Ship Systems

**`game/advanced_ship.py`** (1509 lines) ⭐ SECOND LARGEST
- Complete ship class with all systems
- Equipment slots (Mk I-XV)
- Weapon arrays and torpedo bays
- Shield arc management
- Crew and power systems
- Sensor calculations
- Combat methods

**`game/ships/federation.py`** (2642 lines) ⭐ THIRD LARGEST
- 64 Federation ship templates
- Factory functions for each ship class
- Equipment loadouts
- Ship statistics and requirements

**`game/equipment.py`** (306 lines)
- Mk I-XV equipment progression
- Weapon damage formulas
- Shield capacity calculations
- Engine bonuses
- Deflector sensor bonuses

### UI Components

**`gui/components.py`** (470 lines)
- Button widget (LCARS-style with rounded corners)
- Panel widget (bordered rectangles)
- TextInput widget (text entry fields)
- Dropdown widget (selection lists)
- TabbedPanel widget (multi-tab containers) ⭐ NEW

**`gui/lcars_theme.py`** (~100 lines)
- LCARS color palette (orange, blue, purple, etc.)
- Screen dimensions and constants
- Button styling parameters

---

## Code Statistics

### Total Lines of Code
- **Combat System:** ~2,200 lines (combat_test_screen.py + ship_ai.py + hex_grid.py)
- **Ship Systems:** ~4,500 lines (advanced_ship.py + federation.py + equipment.py)
- **GUI Components:** ~800 lines (components.py + other GUI files)
- **Core Game Logic:** ~3,000 lines (character, galaxy, missions, crew, etc.)
- **Total Active Code:** ~10,500 lines

### File Sizes (Top 5)
1. `game/ships/federation.py` - 2,642 lines (ship templates)
2. `gui/combat_test_screen.py` - 1,712 lines (combat arena)
3. `game/advanced_ship.py` - 1,509 lines (ship class)
4. `gui/components.py` - 470 lines (UI widgets)
5. `game/equipment.py` - 306 lines (equipment system)

### Documentation
- Active markdown files: 14
- Archived markdown files: 8
- Total documentation: ~5,000 lines

---

## Development Workflow

### Adding New Features
1. **Core Logic:** Add to `game/` directory
2. **UI Elements:** Add to `gui/` directory
3. **Ship Templates:** Add to `game/ships/federation.py`
4. **Equipment:** Update `game/equipment.py` formulas

### Testing
- **Combat:** Use "COMBAT TEST" from main menu
- **Full Game:** Use "NEW GAME" from main menu
- **Quick Test:** Modify ship loadouts in `federation.py`

### Documentation
- **User Docs:** Update README.md
- **Developer Docs:** Update PROJECT_OVERVIEW.md
- **System Docs:** Update specific *_DOCUMENTATION.md files

---

## Recent Changes (Nov 4, 2025)

### ✅ Completed
- Tabbed panel UI system (STATUS/WEAPONS/POWER/DAMAGE tabs)
- Comprehensive code cleanup and organization
- Added docstrings to all major files
- Archived 19 obsolete files
- Updated README.md with combat features
- Created CLEANUP_SUMMARY.md

### 🚀 Combat Arena Features
- 8-phase combat system
- Hex-based tactical movement
- Multi-target support (3 targets max)
- Shield arc damage system
- AI opponents with personalities
- Smooth animation system
- Tabbed status panels

---

## Quick Reference

### Controls (Combat Arena)
- **W** - Move forward
- **S** - Move backward
- **A** - Turn left (60°)
- **D** - Turn right (60°)
- **Mouse** - Click to target ships
- **1/2/3** - Cycle target priority
- **SPACE** - Fire weapons
- **ENTER** - End turn/advance phase
- **R** - Reset arena
- **ESC** - Return to menu

### Important Classes
- `AdvancedShip` - Main ship class
- `WeaponArray` - Energy weapons
- `TorpedoBay` - Torpedo launchers
- `HexGrid` - Hex mathematics
- `ShipAI` - AI controller
- `TabbedPanel` - Multi-tab UI

### Key Constants
- Hex size: 40 pixels
- Animation speed: 1.5 (lower = smoother)
- Max targets: 3 (primary/secondary/tertiary)
- Shield facings: 4 (fore/aft/port/starboard)
- Combat phases: 8
- Mark levels: 15 (Mk I - Mk XV)

---

## Support & Resources

### Documentation Files
- **README.md** - Start here!
- **COMBAT_TEST_ARENA_GUIDE.md** - Combat mechanics
- **PROJECT_OVERVIEW.md** - Technical architecture
- **CLEANUP_SUMMARY.md** - Recent code organization

### Getting Help
1. Check relevant .md documentation file
2. Review code comments and docstrings
3. Test in Combat Arena
4. Check `_archive/` for historical context

---

**Last Updated:** November 4, 2025  
**Status:** ✅ Active Development  
**Code Quality:** 🟢 Well Documented
