# Star Trek Game - System Infrastructure

This document describes the core infrastructure systems available for use in the game.

## 📁 File Overview

All infrastructure files are located in `game/` directory:

- `combat_phase.py` - Combat phase enumerations
- `rng.py` - Central random number generator
- `logger.py` - Logging system
- `state_machine.py` - Game state management
- `save_system.py` - Save/load with dataclasses
- `delta_time.py` - Frame-rate independent timing

---

## 🎲 RNG System (`game/rng.py`)

### Purpose
Centralized random number generation with seed control for:
- **Reproducible bugs** - Save seed, reproduce exact combat scenario
- **Testing** - Unit tests with fixed seeds
- **Balance tuning** - Analyze combat with multiple seed runs

### Basic Usage
```python
from game.rng import GameRNG

# Create RNG (auto-generates seed)
rng = GameRNG()

# Or use specific seed for replay
rng = GameRNG(seed=12345)

# Combat rolls
hit = rng.roll_hit(0.85)  # 85% accuracy
damage = rng.roll_damage(10, 50)  # 10-50 damage
crit = rng.roll_critical(0.15)  # 15% crit chance

# Save seed for replay
seed = rng.get_seed()
print(f"Combat seed: {seed}")
```

### When to Use
- **NOW**: Replace `random.randint()` in combat code
- Replace all `random.random()` for hit/miss rolls
- Use for loot drops, encounter generation

### Global Instance
```python
from game.rng import game_rng  # Pre-created instance

if game_rng.roll_hit(accuracy):
    # Fire weapon
```

---

## 📊 Logging System (`game/logger.py`)

### Purpose
- Track bugs with timestamps
- Performance profiling
- Combat debugging
- User support (send logs)

### Setup (in main.py)
```python
from game.logger import setup_logging, get_logger

# Initialize at game start
setup_logging()  # Creates logs/latest.log

# Get logger for each module
logger = get_logger(__name__)
```

### Usage Examples
```python
# Different log levels
logger.debug("Detailed debug info")
logger.info("Game saved successfully")
logger.warning("Shield strength low")
logger.error("Failed to load texture")

# Combat logging
logger.info(f"{attacker.name} fires at {target.name}")
logger.info(f"Hit for {damage} damage")

# Exception logging
try:
    load_ship_data()
except Exception as e:
    logger.exception(f"Failed to load ship: {e}")
```

### When to Use
- **NOW**: Add `setup_logging()` to main.py startup
- Add info logs for major events (combat start, phase changes)
- Add error logs for failures
- Add debug logs for tricky bugs

### Log Locations
- `logs/latest.log` - Current session
- `logs/game_20250104_153045.log` - Archived previous sessions

---

## 🎭 Combat Phase Enums (`game/combat_phase.py`)

### Purpose
Replace magic strings with type-safe enums:
```python
# Before (error-prone)
if self.combat_phase == "fireing":  # TYPO BUG!
    
# After (safe)
if self.combat_phase == CombatPhase.FIRING:  # Autocomplete, no typos
```

### Usage
```python
from game.combat_phase import CombatPhase

# Set phase
self.combat_phase = CombatPhase.FIRING

# Check phase
if self.combat_phase == CombatPhase.MOVEMENT:
    # Handle movement

# Get phase order
for phase in CombatPhase.get_order():
    print(phase)

# Advance phase
next_phase = CombatPhase.next_phase(current_phase)
```

### When to Use
- **NEXT REFACTOR**: Replace all `"firing"`, `"targeting"` strings
- Add to combat_test_screen.py gradually
- Will prevent 90% of phase-related bugs

---

## 🎮 State Machine (`game/state_machine.py`)

### Purpose
Manage high-level game screens and transitions.

### Game States
```python
from game.state_machine import GameState, StateManager

# Available states
GameState.STARTUP
GameState.MAIN_MENU
GameState.COMBAT
GameState.GALAXY_MAP
# ... and more
```

### Basic Usage
```python
# Create state manager
state_mgr = StateManager(initial_state=GameState.STARTUP)

# Transition to new state
state_mgr.transition_to(GameState.MAIN_MENU)

# Check current state
if state_mgr.is_state(GameState.COMBAT):
    # In combat

# Go back to previous state
state_mgr.go_back()
```

### Screen Management
```python
from game.state_machine import ScreenManager, Screen

# Register screens
screen_mgr = ScreenManager()
screen_mgr.register(GameState.COMBAT, CombatScreen())
screen_mgr.register(GameState.MAIN_MENU, MainMenuScreen())

# Switch screens
screen_mgr.set_active(GameState.COMBAT)

# In game loop
screen_mgr.update(dt)
screen_mgr.render(screen)
screen_mgr.handle_events(events)
```

### When to Use
- **WHEN REFACTORING**: Formalize existing screen switching
- Use when adding new screens (starbase, galaxy map)
- Helps with save/load (save current state)

---

## 💾 Save System (`game/save_system.py`)

### Purpose
- Clean JSON serialization
- Version migrations
- Type-safe save data

### Define Save Data
```python
from game.save_system import GameSaveData, PlayerData, ShipData

# Create save
player = PlayerData(
    name="Captain Picard",
    rank="Captain",
    credits=50000
)

ship = ShipData(
    name="USS Enterprise",
    ship_class="Galaxy",
    hull=5000,
    max_hull=5000
)

save_data = GameSaveData(
    player=player,
    player_ship=ship
)
```

### Save/Load
```python
from game.save_system import SaveManager

save_mgr = SaveManager()  # Uses 'saves/' directory

# Save game
save_mgr.save_game(save_data, "slot_1")

# Load game
loaded = save_mgr.load_game("slot_1")
if loaded:
    print(f"Playing as {loaded.player.name}")

# List all saves
for save in save_mgr.list_saves():
    print(f"{save['name']} - {save['timestamp']}")
```

### When to Use
- **WHEN IMPLEMENTING SAVES**: Use these dataclasses as the foundation
- Extend `GameSaveData` with new fields as needed
- Version field allows future migrations

---

## ⏱️ Delta Time System (`game/delta_time.py`)

### Purpose
Frame-rate independent game logic.

### DeltaTimer
```python
from game.delta_time import DeltaTimer

timer = DeltaTimer()

# Game loop
while running:
    dt = timer.tick(target_fps=60)  # Returns delta time in seconds
    
    # Update with delta time
    update_game(dt)
    
    # Check FPS
    print(f"FPS: {timer.get_fps():.1f}")
```

### Cooldown Timers
```python
from game.delta_time import Cooldown

weapon_cooldown = Cooldown(2.0)  # 2 second cooldown

if weapon_cooldown.is_ready():
    fire_weapon()
    weapon_cooldown.start()

# In update loop
weapon_cooldown.update(dt)

# UI: Show cooldown bar
progress = weapon_cooldown.get_progress()  # 0.0 to 1.0
```

### Animation Helpers
```python
from game.delta_time import Animation, lerp, smooth_step

# Create animation
move_anim = Animation(duration=1.5, loop=False)
move_anim.start()

# Update
move_anim.update(dt)

# Get progress and interpolate
t = move_anim.get_progress()  # 0.0 to 1.0
t = smooth_step(t)  # Apply easing
position = lerp(start_pos, end_pos, t)
```

### When to Use
- **ALREADY USING**: Your code uses `dt` in update()
- **NOW**: Replace weapon cooldown counters with `Cooldown` class
- Use `Animation` for smooth movements instead of frame counting

---

## 🚀 Integration Roadmap

### Phase 1: Quick Wins (This Week)
1. **Add logging** - `setup_logging()` in main.py
2. **Use RNG** - Replace combat random calls
3. **Combat phase enums** - Gradual replacement

### Phase 2: Refactoring (When Adding Features)
4. **State machine** - When adding new screens
5. **Save system** - When implementing saves

### Phase 3: Already Done ✓
6. **Delta time** - Already using `dt` in animations

---

## 🧪 Testing Systems

All systems have test code at the bottom. Run individually:

```bash
# Test RNG
python game/rng.py

# Test logging
python game/logger.py

# Test combat phases
python game/combat_phase.py

# Test state machine
python game/state_machine.py

# Test save system
python game/save_system.py

# Test delta time
python game/delta_time.py
```

---

## 📝 Notes

- All systems are **non-breaking** - they don't interfere with existing code
- Use them **gradually** - no need to refactor everything at once
- **Logging first** - Will help find bugs in other systems
- **RNG second** - Makes combat reproducible for testing

---

## 🆘 Quick Reference

```python
# Logging
from game.logger import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)
logger.info("Message")

# RNG
from game.rng import game_rng
if game_rng.roll_hit(0.85):
    damage = game_rng.roll_damage(10, 50)

# Combat Phases
from game.combat_phase import CombatPhase
if phase == CombatPhase.FIRING:
    fire_weapons()

# Cooldowns
from game.delta_time import Cooldown
cd = Cooldown(2.0)
cd.update(dt)
if cd.is_ready():
    cd.start()

# State Management
from game.state_machine import GameState, StateManager
state_mgr.transition_to(GameState.COMBAT)

# Saves
from game.save_system import SaveManager, GameSaveData
save_mgr.save_game(save_data, "slot_1")
```

---

Ready to use! Start with logging and RNG, then integrate the rest as you build new features. 🖖
