# Mark-Based Equipment System Documentation

## Overview
The Star Trek Game now uses a **Mark (Mk) I-XV equipment system** with **absolute stat values** instead of percentage multipliers. Ships come with starter equipment, and the `upgrade_space` stat represents **available space AFTER starter equipment is already installed**.

---

## Weapon System

### Energy Weapons (Phasers, Disruptors, etc.)

**Formula:** `damage = base_damage + (mark - 1) × 5`

**Fire Rate:** Every turn (cooldown = 0)

**Base Damage by Type:**
- Phaser: 15
- Disruptor: 18
- Plasma: 20
- Polaron: 16
- Tetryon: 14

**Example Progression:**
```
Mk I Phaser:   15 damage (15 + 0×5)
Mk II Phaser:  20 damage (15 + 1×5)
Mk IV Phaser:  30 damage (15 + 3×5)
Mk V Phaser:   35 damage (15 + 4×5)
Mk X Phaser:   60 damage (15 + 9×5)
Mk XII Phaser: 70 damage (15 + 11×5)
Mk XV Phaser:  85 damage (15 + 14×5)
```

### Torpedo Launchers (Photon, Quantum, etc.)

**Formula:** `damage = base_damage + (mark - 1) × 10`

**Fire Rate:** Turn-based cooldown (modified by crew skill and mark)

**Base Cooldown by Type:**
- Photon: 3 turns
- Plasma: 3 turns
- Quantum: 4 turns
- Tricobalt: 5 turns

**Mark Reduction:** -1 turn cooldown at Mk V, X, and XV (minimum 2 turns)

**Crew Skill Modifier:**
- Cadet (0%): No reduction
- Green (5%): Minimal reduction
- Regular (10%): Slight reduction
- Veteran (15%): Moderate reduction
- Elite (20%): 20% faster reload → Photon: 3→2 turns
- Legendary (25%): 25% faster reload → Photon: 3→2 turns

**Base Damage by Type:**
- Photon: 80
- Quantum: 100
- Plasma: 90
- Tricobalt: 120

**Example Progression:**
```
Mk I Photon:   80 damage (80 + 0×10), 3 turn cooldown
Mk III Photon:  100 damage (80 + 2×10), 3 turn cooldown
Mk IV Photon:  110 damage (80 + 3×10), 3 turn cooldown
Mk V Photon:   130 damage (80 + 4×10), 2 turn cooldown (mark bonus)
Mk VIII Photon: 150 damage (80 + 7×10), 2 turn cooldown
Mk X Photon:   170 damage (80 + 9×10), 2 turn cooldown
Mk XII Photon: 190 damage (80 + 11×10), 2 turn cooldown
Mk XIII Photon: 200 damage (80 + 12×10), 2 turn cooldown
Mk XV Photon:  220 damage (80 + 14×10), 2 turn cooldown
```

---

## Fire Rate System (Turn-Based Combat)

The game uses a **turn-based combat system** where weapons have different fire rates:

### Energy Weapons
- **Fire Every Turn** (cooldown = 0)
- Always ready to fire
- No reload time
- Consistent damage output

### Torpedoes
- **Turn-Based Cooldown** (2-5 turns)
- Limited ammunition (must reload at starbases)
- Higher damage but can't fire every turn
- Cooldown modified by:
  - **Torpedo Type:** Photon (3), Quantum (4), Tricobalt (5)
  - **Mark Level:** -1 turn at Mk V, X, XV (minimum 2 turns)
  - **Crew Skill:** Elite/Legendary reduce cooldown further

### Cooldown Examples

**Photon Torpedoes (Base: 3 turns)**
| Mark | Crew Skill | Cooldown |
|------|------------|----------|
| Mk I-IV | Cadet/Green/Regular/Veteran | 3 turns |
| Mk I-IV | Elite/Legendary | 2 turns |
| Mk V-XV | Cadet/Green/Regular/Veteran | 2 turns |
| Mk V-XV | Elite/Legendary | 2 turns |

**Quantum Torpedoes (Base: 4 turns)**
| Mark | Crew Skill | Cooldown |
|------|------------|----------|
| Mk I-IV | Any | 4 turns |
| Mk I-IV | Elite | 3 turns |
| Mk I-IV | Legendary | 3 turns |
| Mk V-XV | Regular/Veteran | 3 turns |
| Mk V-XV | Elite/Legendary | 2 turns |

**Tricobalt Torpedoes (Base: 5 turns)**
| Mark | Crew Skill | Cooldown |
|------|------------|----------|
| Mk I-IV | Any | 5 turns |
| Mk V-XV | Cadet/Green | 4 turns |
| Mk V-XV | Regular/Veteran | 4 turns |
| Mk V-XV | Elite | 3 turns |
| Mk V-XV | Legendary | 3 turns |

### Combat Turn Flow

1. **Fire Ready Weapons**
   - Check `weapon.can_fire()` for each weapon
   - Call `weapon.fire(crew_skill_bonus)` to deal damage
   - Torpedoes automatically set cooldown

2. **Take Damage / Apply Effects**
   - Process hits, shield damage, hull damage

3. **End of Turn**
   - Call `ship.advance_all_weapon_cooldowns()`
   - All weapon cooldowns decrease by 1 turn
   - Ready weapons become available next turn

---

## Sensor & Targeting System

The sensor system determines targeting range and accuracy in combat.

### Range Bands

**Point Blank (0-1 hex)**
- **Accuracy:** +50%
- **Tactical Use:** Maximum damage, ideal for finishing blows

**Close Range (2 to 50% sensor range)**
- **Accuracy:** +25% to +50% (linear)
- **Tactical Use:** Optimal combat range, high accuracy

**Sensor Range (50% to 100% sensor range)**
- **Accuracy:** +10% to +25% (linear)
- **Tactical Use:** Good accuracy, standard engagement range

**Long Range (100% to 200% sensor range)**
- **Accuracy:** +10% to -40% (linear penalty)
- **Tactical Use:** Reduced accuracy, risky shots

**Out of Range (Beyond 2× sensor range)**
- **Accuracy:** Cannot target
- **Tactical Use:** Must close distance or improve sensors

### Sensor Range Calculation

**Base Sensor Range:**
- Set per ship class (Miranda: 6 hexes, Galaxy: 10 hexes)

**Deflector Equipment Bonus:**
- +1 hex per 2 marks (Mk I: +0, Mk V: +2, Mk X: +5, Mk XV: +7)

**System Damage Penalty:**
- Sensor system health directly affects range
- 50% health = 50% sensor range
- Minimum 1 hex at critical damage

**Effective Range Formula:**
```
effective_range = (base_range + deflector_bonus) × sensor_health
maximum_targeting = effective_range × 2
```

### Accuracy Examples

**Miranda-class (6 hex sensors)**
| Distance | Range Band | Accuracy | Modifier |
|----------|------------|----------|----------|
| 0-1 hex | Point Blank | 1.50× | +50% |
| 2-3 hex | Close Range | 1.25-1.33× | +25-33% |
| 4-6 hex | Sensor Range | 1.10-1.20× | +10-20% |
| 7-9 hex | Long Range | 0.85-1.02× | -15% to +2% |
| 10-12 hex | Long Range | 0.60-0.77× | -40% to -23% |
| 13+ hex | Out of Range | N/A | Cannot target |

**Galaxy-class with Mk X Deflector (11 hex sensors)**
| Distance | Range Band | Accuracy | Modifier |
|----------|------------|----------|----------|
| 0-1 hex | Point Blank | 1.50× | +50% |
| 2-5 hex | Close Range | 1.25-1.50× | +25-50% |
| 6-11 hex | Sensor Range | 1.10-1.25× | +10-25% |
| 12-16 hex | Long Range | 0.77-1.02× | -23% to +2% |
| 17-22 hex | Long Range | 0.60-0.68× | -40% to -32% |
| 23+ hex | Out of Range | N/A | Cannot target |

### Tactical Implications

**Sensor Superiority:**
- Ships with better sensors can engage from safer distances
- Advanced deflectors extend effective combat range
- High-mark deflectors = strategic advantage

**Close Combat:**
- High accuracy bonuses reward aggressive tactics
- Point blank (+50%) is devastating but risky
- Hull damage and boarding actions more viable

**Long Range Combat:**
- Safer but less accurate
- Good for damaged ships retreating
- Requires multiple volleys to score hits

**Sensor Damage:**
- Prioritize sensor protection
- Damaged sensors = reduced range = combat disadvantage
- Emergency repairs crucial in extended battles

---

## Equipment Types & Bonuses

All bonuses are **absolute values**, not multipliers.

### 1. Shield Arrays
**Upgrade Space Cost:** 8

**Capacity Bonus:**
- Standard/Regenerative: +50 per mark
- Covariant: +75 per mark

**Regeneration Bonus (points per turn):**
- Regenerative: +8 per mark
- Standard: +3 per mark

**Damage Reduction (armor):**
- Resilient: +5 armor per mark
- Others: 0

**Example:** Mk V Covariant Shield = +375 capacity, +15 regen

---

### 2. Impulse Engines
**Upgrade Space Cost:** 6

**Speed Bonus:** +1 hex per mark
**Turn Rate Bonus:** -1 turn cost every 3 marks

**Example:** Mk VI Impulse = +6 speed, -2 turn cost

---

### 3. Warp Cores
**Upgrade Space Cost:** 10

**Power Bonus:**
- Overcharged: +20 power per mark
- Standard: +15 power per mark

**Efficiency Bonus (reduces power costs):**
- Efficient: -2% per mark
- Others: 0%

**Example:** Mk X Overcharged Core = +200 power

---

### 4. Deflector Dishes
**Upgrade Space Cost:** 7

**Sensor Range:** +1 hex every 2 marks (critical for targeting accuracy)
**Auxiliary Power:** +5 power per mark

**Sensor Impact:**
- Better sensors = longer targeting range
- Accuracy bonus within sensor range
- Can only target up to 2× sensor range

**Example:** Mk VIII Deflector = +4 hexes sensor range, +40 aux power

**Tactical Value:**
- Mk I-II: 6-7 hex range (12-14 max targeting)
- Mk V: 8 hex range (16 max targeting)
- Mk X: 11 hex range (22 max targeting)
- Mk XV: 13 hex range (26 max targeting)

---

### 5. Warp Engines
**Upgrade Space Cost:** 8

**Warp Speed:** +0.1 warp factor per mark
**Sector Speed:** +5% per mark

**Example:** Mk XII Warp Engine = +1.2 warp factor, +60% sector speed

---

### 6. Armor Plating
**Upgrade Space Cost:** 6

**Armor Bonus:**
- Neutronium: +4 armor per mark
- Ablative: +3 armor per mark
- Polarized: +2 armor per mark (special bonuses vs energy weapons)

**Hull Bonus:**
- Neutronium: +100 hull per mark
- Standard: +50 hull per mark

**Example:** Mk XV Neutronium = +60 armor, +1500 hull

---

## Ship Classes & Starter Equipment

### Miranda-class Frigate (Rank 1)
**Upgrade Space Available:** 80

**Starter Equipment:**
- 3× Mk IV Phaser Arrays (30 damage each)
- 1× Mk IV Photon Torpedoes (110 damage)
- Mk II Shields
- Mk II Impulse Engines
- Mk II Warp Core

**Upgrade Example:**
- Player can install Mk V phasers, using 5 upgrade space per weapon
- Upgrading all 3 phasers: 3×5 = 15 upgrade space used
- Remaining: 80-15 = 65 upgrade space

---

### Galaxy-class Heavy Cruiser (Rank 8)
**Upgrade Space Available:** 200

**Starter Equipment:**
- 4× Mk XII Phaser Arrays (70 damage, one Mk X = 60 damage)
- 2× Mk XII Photon Torpedoes (190 damage)
- Mk X Shields
- Mk X Impulse Engines
- Mk XII Warp Core

**Upgrade Example:**
- Player can upgrade to Mk XV phasers for maximum damage (85 dmg)
- Or install quantum torpedoes (higher base damage)
- Large upgrade space allows extensive customization

---

## Code Usage

### Creating Ships with Mark-Based Weapons

```python
from game.advanced_ship import AdvancedShip, WeaponArray, TorpedoBay

ship = AdvancedShip("USS Example", "NCC-1701", "Constitution", "Cruiser", 2270)

# Add Mk IV phasers
ship.weapon_arrays = [
    WeaponArray('phaser', mark=4, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
    WeaponArray('phaser', mark=4, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5)
]

# Add Mk III photon torpedoes
ship.torpedo_bays = [
    TorpedoBay('photon', mark=3, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
]

# Check damage
damage = ship.weapon_arrays[0].get_damage()  # Returns 30
```

### Creating Equipment Upgrades

```python
from game.equipment import (
    create_phaser_array,
    create_shield_array,
    create_impulse_engine,
    create_warp_core
)

# Create Mk V phaser upgrade
phaser_mk5 = create_phaser_array(5)
print(phaser_mk5.get_damage())  # 35 damage
print(phaser_mk5.upgrade_space_cost)  # 5

# Create Mk VIII covariant shield
shield_mk8 = create_shield_array(8, 'covariant')
print(shield_mk8.get_capacity_bonus())  # +600 capacity
print(shield_mk8.get_regeneration_bonus())  # +24 regen per turn
```

### Installing Equipment on Ships

```python
from game.ships import create_starting_ship
from game.equipment import create_phaser_array

# Get starter ship (Miranda with Mk IV weapons)
ship = create_starting_ship()

# Create Mk VI phaser upgrade
new_phaser = create_phaser_array(6)

# Install equipment
success = ship.install_equipment(new_phaser)
if success:
    print(f"Installed! Using {ship.upgrade_space_used}/{ship.upgrade_space} space")
else:
    print("Not enough upgrade space!")

# Get total stats including equipment bonuses
total_stats = ship.get_total_stats()
print(total_stats['hull'])  # Hull + armor bonuses
print(total_stats['shields'])  # Shields + capacity bonuses
```

### Weapon Fire Rates (Turn-Based Combat)

```python
from game.ships import create_starting_ship

ship = create_starting_ship()

# Get crew skill bonus (Regular = 10%)
crew_bonus = ship.get_crew_bonus()  # 0.10

# === TURN 1: Fire Weapons ===
# Energy weapons fire every turn
phaser_damage = ship.weapon_arrays[0].fire(crew_bonus)
print(f"Phaser: {phaser_damage} damage")  # 30 damage

# Torpedoes have cooldown
if ship.torpedo_bays[0].can_fire():
    torpedo_damage = ship.torpedo_bays[0].fire(crew_bonus)
    print(f"Torpedo: {torpedo_damage} damage")  # 110 damage
    print(f"Cooldown: {ship.torpedo_bays[0].cooldown_remaining} turns")  # 3 turns

# === END OF TURN: Advance Cooldowns ===
ship.advance_all_weapon_cooldowns()

# === TURN 2: Phasers Ready, Torpedoes on Cooldown ===
print(f"Phaser ready: {ship.weapon_arrays[0].can_fire()}")  # True
print(f"Torpedo ready: {ship.torpedo_bays[0].can_fire()}")  # False
print(f"Cooldown remaining: {ship.torpedo_bays[0].cooldown_remaining}")  # 2 turns

# Get all ready weapons
ready_weapons = ship.get_ready_weapons()
for weapon_type, index, weapon in ready_weapons:
    if weapon_type == 'array':
        print(f"Phaser array {index} ready")
    elif weapon_type == 'torpedo':
        print(f"Torpedo bay {index} ready")

# Get weapon status display
status = ship.get_weapon_status()
for weapon_info in status['energy_weapons']:
    print(f"Mk {weapon_info['mark']} {weapon_info['type']}: {weapon_info['damage']} dmg")
    
for torp_info in status['torpedoes']:
    print(f"Mk {torp_info['mark']} {torp_info['type']}: {torp_info['damage']} dmg")
    print(f"  Torpedoes: {torp_info['torpedoes']}/{torp_info['max_torpedoes']}")
    print(f"  Ready: {torp_info['ready']}, Cooldown: {torp_info['cooldown']} turns")
```

---

## Upgrade Space Management

**Key Concept:** `upgrade_space` is the space **available** after starter equipment.

**Example:** Miranda-class
- Has 80 upgrade space available
- Starter equipment (3 phasers + 1 torpedo) is already installed
- These don't count toward the 80 available space
- Player can add up to 80 points worth of upgrades

**Upgrade Space Costs:**
- Energy Weapons: 5 per weapon
- Torpedo Launchers: 10 per launcher
- Shield Arrays: 8
- Warp Cores: 10
- Warp Engines: 8
- Deflectors: 7
- Impulse Engines: 6
- Armor: 6

---

## Mark Requirements by Rank

Equipment marks are gated by player rank to prevent power gaming:

```
Mk I-II:   Rank 0 (Lieutenant Commander)
Mk III-IV: Rank 1 (Commander)
Mk V-VI:   Rank 2 (Captain)
Mk VII-VIII: Rank 3 (Fleet Captain)
Mk IX-X:   Rank 4 (Commodore)
Mk XI:     Rank 5 (Rear Admiral)
Mk XII:    Rank 6 (Vice Admiral)
Mk XIII-XIV: Rank 7 (Admiral)
Mk XV:     Rank 8 (Fleet Admiral)
```

---

## Benefits of This System

1. **Clear Progression:** Each mark provides predictable stat increases
2. **Strategic Choice:** Limited upgrade space forces meaningful decisions
3. **No Stacking Issues:** Absolute values prevent exponential power scaling
4. **Easy Balance:** Simple to tune damage/stats by adjusting mark bonuses
5. **Player-Friendly:** Obvious what upgrading provides (Mk IV→V = +5 damage)
6. **Starter Equipment:** Ships come battle-ready, upgrades enhance capabilities

---

## Future Expansion

The system is designed to support:
- **Other Factions:** Klingon disruptors, Romulan plasma, Borg cutting beams
- **Special Weapons:** Chroniton torpedoes, transphasic torpedoes
- **Set Bonuses:** Equipping full Mk XII sets provides extra bonuses
- **Experimental Tech:** Prototype Mk XVI+ equipment for endgame
- **Crafting:** Break down old equipment to build new gear
