# Power Management System

## Overview

The power management system allows tactical resource allocation between three subsystems: **Engines**, **Shields**, and **Weapons**. Power allocation provides percentage-based bonuses that scale consistently across all ship sizes, preventing power imbalances while rewarding strategic choices.

## Design Philosophy

1. **Percentage-Based Scaling**: All bonuses are percentage increases/decreases, ensuring balance across ship sizes
2. **Strategic Trade-offs**: Boosting one system requires reducing others (zero-sum resource allocation)
3. **Balanced Default**: 100 power in each system = no bonus/penalty (33.3% allocation each)
4. **Conservative Caps**: Maximum bonuses capped to prevent one-shot scenarios and maintain tactical depth

## Power Allocation

### Total Power Pool
```
Total Available Power = warp_core_max_power (default: 300)
Distribution: engines + shields + weapons = 300
```

### Default Balance
- **Engines**: 100 power
- **Shields**: 100 power  
- **Weapons**: 100 power
- **Total**: 300 power (balanced allocation)

### Allocation Strategies

**Offensive Build** (Glass Cannon):
- Engines: 50
- Shields: 50
- Weapons: 200
- Effect: +50% weapon damage, -50% movement, -50% shield regen

**Defensive Build** (Tank):
- Engines: 50
- Shields: 200
- Weapons: 50
- Effect: +100% shield regen, -50% movement, -50% weapon damage

**Speed Build** (Hit & Run):
- Engines: 200
- Shields: 50
- Weapons: 50
- Effect: +50% movement, -50% shield regen, -50% weapon damage

**Balanced Build** (Standard):
- Engines: 100
- Shields: 100
- Weapons: 100
- Effect: No bonuses or penalties

## System Bonuses

### Engine Power → Movement Points

**Formula**: `multiplier = 1.0 + ((power - 100) / 10) * 0.05`

**Scaling**:
- 0 power = 0.5x movement (-50%) - MIN
- 50 power = 0.75x movement (-25%)
- 100 power = 1.0x movement (0%) - BALANCED
- 150 power = 1.25x movement (+25%)
- 200 power = 1.5x movement (+50%) - MAX

**Examples**:
- Miranda (6 base MP):
  - At 200 power: 9 MP
  - At 100 power: 6 MP
  - At 0 power: 3 MP

- Yorktown (5 base MP):
  - At 200 power: 7 MP (actually 7.5, rounded down)
  - At 100 power: 5 MP
  - At 0 power: 2 MP (actually 2.5, rounded down)

### Shield Power → Regeneration Rate

**Formula**: `multiplier = 1.0 + ((power - 100) / 10) * 0.10`

**Scaling**:
- 0 power = 0.0x regen (-100%) - MIN
- 50 power = 0.5x regen (-50%)
- 100 power = 1.0x regen (0%) - BALANCED
- 150 power = 1.5x regen (+50%)
- 200 power = 2.0x regen (+100%) - MAX

**Effect**: 
- Does NOT increase shield capacity
- ONLY affects regeneration rate per turn
- High power = shields recover faster between combat rounds
- Low power = shields recover slowly (vulnerable to sustained combat)

### Weapon Power → Damage Output

**Formula**: `multiplier = 1.0 + ((power - 100) / 10) * 0.05`

**Scaling**:
- 0 power = 0.5x damage (-50%) - MIN
- 50 power = 0.75x damage (-25%)
- 100 power = 1.0x damage (0%) - BALANCED
- 150 power = 1.25x damage (+25%)
- 200 power = 1.5x damage (+50%) - MAX

**Examples**:
- Phaser Array XII (85 base damage):
  - At 200 power: 127 damage
  - At 100 power: 85 damage
  - At 0 power: 42 damage

- Photon Torpedo X (270 base damage):
  - At 200 power: 405 damage
  - At 100 power: 270 damage
  - At 0 power: 135 damage

**Why Only +50% Max?**
Capping weapon bonus at +50% prevents:
- One-shot kills (Yorktown with 200 weapon power still can't instantly destroy smaller ships)
- Power gaming (forced to make tactical trade-offs)
- Invalidating other stats (system efficiency, crew bonuses still matter)

## Tactical Considerations

### When to Increase Engine Power
- **Closing distance** to slow-moving enemies
- **Flanking maneuvers** requiring extra hexes
- **Retreat scenarios** needing maximum escape speed
- **Evasive tactics** to avoid enemy firing arcs

### When to Increase Shield Power
- **Sustained combat** with multiple enemies
- **Tank role** drawing fire for allies
- **Low hull** situations needing shield buffer
- **Recovery phase** after taking heavy damage

### When to Increase Weapon Power
- **Alpha strike** opening salvo
- **Target weak shields** to maximize damage
- **Finishing move** on low-hull enemy
- **Outnumbered** scenarios (end fights quickly)

### When to Keep Balanced
- **Uncertain situations** maintaining flexibility
- **Exploration** general-purpose allocation
- **New encounters** before assessing threat
- **Learning opponents** during first engagement

## Implementation Details

### Code Structure

```python
# AdvancedShip methods:
ship.get_engine_power_bonus()      # Returns 0.5 to 1.5
ship.get_shield_power_bonus()      # Returns 0.0 to 2.0  
ship.get_weapon_power_bonus()      # Returns 0.5 to 1.5
ship.get_current_movement_points() # Returns base MP * engine bonus
```

### Calculation Flow

**Movement Phase Start**:
```python
base_mp = ship.impulse_speed
power_multiplier = ship.get_engine_power_bonus()
actual_mp = int(base_mp * power_multiplier)
```

**Weapon Firing**:
```python
base_damage = weapon.base_damage
power_multiplier = ship.get_weapon_power_bonus()
damage = base_damage * system_efficiency * power_multiplier * (crew_bonuses)
```

**Shield Regeneration**:
```python
base_regen = amount_per_arc
power_multiplier = ship.get_shield_power_bonus()
regen = base_regen * system_efficiency * power_multiplier
```

## Balance Philosophy

### Why Percentage-Based?
- **Size-Agnostic**: Works identically for Miranda (small) and Yorktown (huge)
- **Fair Scaling**: +50% is +50% regardless of base stats
- **Predictable**: Players can mentally calculate effects
- **Future-Proof**: New ships auto-balance

### Why Conservative Caps?
- **+50% weapons** prevents instant kills while still feeling impactful
- **+50% movement** provides significant tactical advantage without breaking positioning
- **+100% shields** allows defensive builds but doesn't make ships invincible
- **-50% minimums** force meaningful trade-offs (can't ignore systems entirely)

### Design Goals Achieved
✅ Small ships remain viable (percentage bonuses scale equally)
✅ Large ships can't one-shot everything (damage cap at +50%)
✅ Strategic depth (must choose between mobility, defense, offense)
✅ Dynamic gameplay (can change allocation between rounds)
✅ Clear feedback (UI shows power levels and resulting bonuses)

## UI Integration

### Power Triangle (GUI)
- Drag point within triangle to allocate power
- Visual representation of three-way trade-off
- Real-time preview of bonuses
- Cannot exceed total available power

### In-Combat Display
```
MOVEMENT: 7/7 (base 5 × 1.50)  ← Shows power bonus
Engines: 200  Shields: 50  Weapons: 50
```

### Combat Log
```
Enterprise: 7 movement points (base 5 × 1.50)
PHASER → PRIMARY: 127 damage (base 85 × 1.50)
```

## Future Enhancements

### Possible Additions
1. **Overload Mode**: Temporarily exceed 300 total (risk system damage)
2. **Preset Configurations**: Save/load power profiles
3. **Dynamic Power**: Auto-adjust based on AI combat state
4. **System Damage**: Power distribution affected by damaged systems
5. **Warp Core Upgrades**: Increase total power pool (400, 500, etc.)

### Already Implemented
✅ Percentage-based scaling across all ship sizes
✅ Conservative damage caps (+50% max)
✅ Strategic trade-offs (zero-sum allocation)
✅ Real-time movement point calculation
✅ Weapon damage scaling with power
✅ Shield regeneration scaling with power
✅ UI feedback showing power effects
