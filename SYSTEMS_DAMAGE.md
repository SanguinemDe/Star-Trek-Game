# Systems Damage and Crew Casualties System

## Overview
Implemented a comprehensive systems damage and crew casualties system that realistically simulates combat damage, system degradation, and crew loss with Medical officer mitigation.

## Key Features Implemented

### 1. Systems Damage
**Location:** `game/ship.py` - `_process_hull_damage()` method

- **Shield-Dependent Damage Rates:**
  - Shields UP: 15% chance per system, 2-8 damage per hit
  - Shields DOWN: 40% chance per system, 5-15 damage per hit

- **Hull Integrity Modifiers:**
  - Hull < 50%: 1.5x damage multiplier
  - Hull < 25%: 2.0x damage multiplier

- **Systems Tracked:**
  - Weapons (affects damage output and accuracy)
  - Shields (affects recharge rate)
  - Sensors (affects scan range and targeting)
  - Engines (affects warp speed and evasion)
  - Life Support (kills crew if damaged)
  - Transporter (no direct combat effect)

### 2. Crew Casualties
**Location:** `game/ship.py` - `_process_casualties()` method

- **Base Casualty Rates:**
  - Shields UP: 0.5 deaths per 10 hull damage
  - Shields DOWN: 2.0 deaths per 10 hull damage

- **Medical Officer Mitigation:**
  - Reduces casualties by up to 50% at max skill (100)
  - Formula: `1.0 - (medical_skill / 200.0)`

- **Effects:**
  - Reduces current crew count
  - Tracks `casualties_this_combat` for reporting
  - Lowers crew morale with each death

### 3. Crew Regeneration
**Location:** `game/ship.py` - `regenerate_crew()` method

- **Recovery Rate:**
  - Base: 1 crew per stardate
  - Medical Officer Bonus: +2 crew per stardate at max skill
  - Formula: `1 + (medical_skill / 50.0)` crew per stardate

- **Effects:**
  - Slowly replenishes crew during travel
  - Improves morale as crew recovers
  - Cannot exceed max_crew capacity

### 4. Life Support Failure
**Location:** `game/ship.py` - `process_life_support_damage()` method

- **Death Rate:**
  - Scales with life support damage (0-100%)
  - Up to 2 crew deaths per day at 0% life support
  - Medical officer provides up to 33% mitigation

- **Effects:**
  - Continuous crew loss during travel if damaged
  - Morale loss with each death
  - Critical warning messages displayed

### 5. System Performance Penalties
**Location:** `game/ship.py` - `get_system_penalties()` method

Returns multipliers (0.0-1.0) for:
- **Weapons Damage:** Directly affected by weapons system status
- **Weapons Accuracy:** Affected by weapons and sensors
- **Warp Speed:** Directly affected by engines
- **Shield Recharge:** Directly affected by shields system
- **Sensor Range:** Directly affected by sensors
- **Evasion:** Affected by engines (min 50%)

All penalties also affected by crew effectiveness.

### 6. Crew Effectiveness
**Location:** `game/ship.py` - `get_crew_effectiveness()` method

- **Calculation:**
  - Crew percent: `crew_count / max_crew`
  - Morale multiplier: `0.5 + (morale / 200.0)`
  - Combined: `crew_percent * morale_multiplier`
  - Range: 0.5-1.0 (50%-100%)

- **Effects:**
  - Multiplies ALL system performance penalties
  - Affects combat, exploration, and diplomacy
  - Creates death spiral if crew losses mount

## Integration Points

### Combat System (`game/combat.py`)
- Weapon attacks apply system penalties to damage and accuracy
- Combat aftermath displays:
  - Total casualties
  - Damaged systems
  - Performance warnings

### Navigation System (`game/navigation.py`)
- During travel:
  - Crew regenerates based on travel time
  - Life support damage causes casualties
  - Warning messages for critical damage

### UI System (`game/ui.py`)
- Ship status display shows:
  - System status with indicators (●◐○)
  - Crew effectiveness percentage
  - Active performance penalties

### Station Repairs (`game/exploration.py`)
- Full repairs restore:
  - Hull and armor
  - All systems to 100%
  - Shields recharged
- Costs calculated per point

## Combat Example

```
=== Scenario: Torpedo hits with shields down ===

Before:
- Hull: 60/60
- Shields: 0/40
- Crew: 200/200
- All systems: 100%

After 200 damage torpedo:
- Hull: 0/60 (DESTROYED)
- Crew: 119/200 (81 casualties)
- Weapons: 81%
- Shields: 81%
- Sensors: 81%
- Engines: 100%
- Life_Support: 81%
- Crew Effectiveness: 50.6%
- Weapons Damage: 33.2%
- Warp Speed: 41.0%
```

## Balancing Notes

### Medical Officer Impact
- Rank 2 (Lieutenant) with ~40 skill: 20% casualty reduction
- Rank 4 (Commander) with ~80 skill: 40% casualty reduction
- Max theoretical (100 skill): 50% casualty reduction

### Life Support Critical Thresholds
- 100-75%: Safe, no casualties
- 75-50%: Occasional casualties (<1% per day)
- 50-25%: Moderate casualties (~1% per day)
- 25-0%: Heavy casualties (~2% per day)

### System Damage Recovery
- Station repairs: Instant, expensive (dilithium cost)
- Crew regeneration: Slow, automatic during travel
- No field repairs for systems (requires station)

## Testing Results

Test script: `test_systems.py`

✅ Systems damage scales correctly with shield status
✅ Hull integrity modifiers work as expected
✅ Casualties increase dramatically without shields
✅ Medical officer reduces casualties appropriately
✅ System penalties affect ship performance
✅ Crew regeneration works during travel
✅ Life support damage kills crew over time
✅ Crew effectiveness impacts all systems

## Future Enhancements (Optional)

1. **Field Repairs:** Engineering officer attempts during downtime
2. **Critical Hits:** Rare chance to instantly destroy a system
3. **System Redundancy:** Backup systems reduce penalty severity
4. **Crew Training:** Experienced crew reduces casualty rates
5. **Triage:** Medical officer prioritizes critical patients during combat
6. **Battle Damage Assessment:** Detailed report after combat
7. **Repair Priority:** Choose which systems to repair first at stations
8. **Emergency Repairs:** Temporary fixes during combat (high risk)

## Code Quality

- ✅ All methods fully commented
- ✅ Clear variable names
- ✅ Modular design
- ✅ No circular dependencies
- ✅ Consistent with existing codebase
- ✅ Compiles without errors
- ✅ Tested and verified
