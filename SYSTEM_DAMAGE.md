# Internal Systems Damage System

## Overview
Ships in combat can sustain damage to internal systems as they take hull damage. The more damaged a ship's hull becomes, the higher the chance and severity of system failures.

## Hull vs Destruction

### Hull Reaches 0%
- **Ship is DISABLED but NOT destroyed**
- Can still be salvaged and repaired at a starbase
- Crew survives (unless warp core breach occurs)
- Ship is "dead in space" - no offensive capability

### Warp Core Reaches 0%
- **CATASTROPHIC WARP CORE BREACH**
- 💥 Ship is COMPLETELY DESTROYED
- Massive explosion (damages nearby ships in future implementation)
- Very low crew/player survival chance (10% base)
- Engineer skill can improve survival odds slightly (up to 30% max)
- No salvage possible

## System Damage Mechanics

### Damage Probability Based on Hull Integrity

| Hull Integrity | Base Chance | Damage Severity |
|---------------|-------------|-----------------|
| 75-100% | 15% × damage_ratio | 5-10% per system |
| 50-75% | 30% × damage_ratio | 8-15% per system |
| 25-50% | 50% × damage_ratio | 12-25% per system |
| 0-25% | 75% × damage_ratio | 20-40% per system |

**damage_ratio** = (hull damage from hit) / (maximum hull)

### System Vulnerability

Different systems have different vulnerabilities to damage:

| System | Vulnerability | Notes |
|--------|--------------|-------|
| Shields | 1.2× | Shield emitters exposed on hull |
| Sensors | 1.1× | Sensor arrays exposed |
| Weapons | 1.0× | Standard vulnerability |
| Auxiliary | 1.0× | Standard vulnerability |
| Sick Bay | 0.9× | Interior but accessible |
| Impulse Engines | 0.8× | Somewhat protected |
| Engineering | 0.7× | Deep interior systems |
| Warp Drive | 0.6× | Well protected core systems |
| Life Support | 0.5× | Redundant, protected systems |
| **Warp Core** | **0.4×** | **Most protected, but CRITICAL if damaged** |

## System Failure Consequences

### Warp Core (0%)
- ⚠️ **WARP CORE BREACH IMMINENT**
- Ship will explode at end of turn
- Emergency protocols: evacuate crew (10% base survival, +20% with skilled engineer)
- **BIG BOOM** - total loss

### Life Support (0%)
- ⚠️ **LIFE SUPPORT FAILURE**
- Crew casualties increase rapidly over time
- Crew efficiency severely reduced
- Affects weapons, sensors, and engineering efficiency (cascade effect)

### Impulse Engines (0%)
- ⚠️ **IMPULSE DRIVE OFFLINE**
- Ship mobility compromised
- Cannot maneuver or change speed
- Evasion reduced to 0

### Warp Drive (0%)
- ⚠️ **WARP DRIVE OFFLINE**
- Cannot achieve warp speed
- Stranded if not at starbase

### Shields (0%)
- ⚠️ **SHIELD GENERATORS DESTROYED**
- No shield regeneration possible
- Existing shields remain but won't recharge
- Must repair at starbase

### Weapons (0%)
- ⚠️ **WEAPON SYSTEMS DESTROYED**
- Cannot fire any weapons
- Ship is defenseless
- Manual targeting completely offline

### Sensors (0%)
- ⚠️ **SENSORS DESTROYED**
- Targeting severely degraded
- Accuracy penalties on all weapons
- Cannot detect cloaked ships
- Sensor range reduced to minimum

## Damage Cascades

Damage to critical systems affects other systems:

### Warp Core Damage
- **Affects:** ALL systems
- Warp core efficiency multiplies all other system efficiencies
- Example: Warp core at 50% → all systems operate at 50% of their current efficiency

### Life Support Damage
- **Affects:** Weapons, Sensors, Engineering
- Life support efficiency multiplies these specific systems
- Example: Life support at 60% → weapons damage reduced by 40%

### Sensor Damage
- **Affects:** Weapon accuracy
- Damaged sensors reduce targeting accuracy
- Example: Sensors at 40% → weapon accuracy reduced significantly

## Combat Log Messages

### System Damage
```
⚠ Enterprise: shields critical (28%)
⚠ Defiant: WARP_CORE DESTROYED!
```

### Warp Core Breach
```
💥 WARP CORE BREACH! Crew evacuated!
💥💥💥 CATASTROPHIC WARP CORE BREACH! Defiant DESTROYED! 💥💥💥
```

### Hull Failure
```
*** Enterprise DISABLED - Hull integrity failure! ***
```

## Strategic Implications

1. **Target Priority**: Targeting already-damaged ships increases chance of catastrophic system failures

2. **Risk Management**: As your hull drops below 50%, risk of critical system damage escalates rapidly

3. **Warp Core Protection**: Losing your warp core = game over. Consider retreating before hull drops below 25%

4. **Engineer Importance**: A skilled engineer officer can:
   - Improve system repair rates
   - Increase warp core breach survival chances
   - Reduce damage cascade effects

5. **Medical Officer Value**: Reduces crew casualties, maintains crew efficiency longer

6. **Tactical Retreat**: Disabled ships can be repaired at starbase. Destroyed ships (warp core breach) are TOTAL LOSS.

## Repair Options

### Field Repairs
- Limited to 25% or 50% depending on damage severity
- Engineering efficiency affects repair speed
- Engineer officer provides bonus

### Starbase Repairs
- Full repair to 100% for all systems
- Hull can be restored
- Warp core can be replaced
- No restrictions

## Future Enhancements

1. **Proximity Damage**: Warp core breaches damage nearby ships
2. **System Targeting**: Ability to target specific enemy systems
3. **Critical Hits**: Random chance for extra damage to specific system
4. **Damage Control Teams**: Crew assignments to reduce system damage
5. **Emergency Power**: Reroute power from damaged systems to functional ones
