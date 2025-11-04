# Sensor & Targeting System Documentation

## Overview
The sensor system controls **targeting range** and **accuracy modifiers** in combat. Ships can only target enemies within **2× sensor range**, with accuracy bonuses for close targets and penalties at long range.

---

## Core Mechanics

### Sensor Range
- **Base Range:** Set per ship class (5-10 hexes typically)
- **Equipment Bonus:** Deflector upgrades increase range
- **System Health:** Damage to sensors reduces effective range
- **Maximum Targeting:** Can only engage targets within 2× sensor range

### Accuracy Modifiers
Distance from target determines accuracy:

```
Point Blank:     0-1 hex                 → +50% accuracy
Close Range:     1 to 50% sensor range   → +25% to +50%
Sensor Range:    50% to 100% range       → +10% to +25%
Long Range:      100% to 200% range      → -40% to +10%
Out of Range:    Beyond 2× range         → Cannot target
```

---

## Accuracy Calculation

### Formula

The `get_targeting_accuracy(distance)` method returns an accuracy multiplier:

**Point Blank (0-1 hex):**
```python
accuracy = 1.50  # +50% accuracy
```

**Close Range (within 50% sensor range):**
```python
ratio = distance / (sensor_range × 0.5)
accuracy = 1.50 - (ratio × 0.25)  # Linear from 1.50 → 1.25
```

**Sensor Range (50%-100% sensor range):**
```python
ratio = (distance - sensor_range × 0.5) / (sensor_range × 0.5)
accuracy = 1.25 - (ratio × 0.15)  # Linear from 1.25 → 1.10
```

**Long Range (100%-200% sensor range):**
```python
ratio = (distance - sensor_range) / sensor_range
accuracy = 1.10 - (ratio × 0.50)  # Linear from 1.10 → 0.60
```

**Beyond 2× Sensor Range:**
```python
accuracy = None  # Cannot target
```

---

## Range Bands Detailed

### Point Blank (0-1 hex)
**Accuracy Multiplier:** 1.50× (+50%)

**Tactical Characteristics:**
- Maximum accuracy, devastating volleys
- High risk: enemy also has point blank advantage
- Ideal for finishing crippled enemies
- Boarding action range
- Ramming speed!

**When to Use:**
- Enemy shields down, go for kill
- Your ship has superior close-combat weapons
- Desperate situations requiring maximum damage
- Boarding parties ready

---

### Close Range (2 to 50% sensors)

**Accuracy Multiplier:** 1.25× to 1.50× (+25% to +50%)

**Tactical Characteristics:**
- Optimal engagement range
- High accuracy with manageable risk
- Most battles fought here
- Good shield/hull exchange ratio

**Example (6 hex sensors):**
- 2 hexes: 1.33× (+33% accuracy)
- 3 hexes: 1.25× (+25% accuracy)

**When to Use:**
- Standard combat engagement
- Superior ship with good positioning
- Want reliable hits without excessive risk
- Pursuing damaged enemies

---

### Sensor Range (50%-100% sensors)

**Accuracy Multiplier:** 1.10× to 1.25× (+10% to +25%)

**Tactical Characteristics:**
- Standard combat range
- Still favorable accuracy
- Safest range with good accuracy
- Most strategic combat here

**Example (6 hex sensors):**
- 4 hexes: 1.20× (+20% accuracy)
- 5 hexes: 1.15× (+15% accuracy)
- 6 hexes: 1.10× (+10% accuracy)

**When to Use:**
- Conservative combat approach
- Damaged ship staying at safer distance
- Using superior sensors to advantage
- Torpedo-heavy loadout (high damage, need less accuracy)

---

### Long Range (100%-200% sensors)

**Accuracy Multiplier:** 0.60× to 1.10× (-40% to +10%)

**Tactical Characteristics:**
- Accuracy penalties increase with distance
- Many shots miss entirely
- Only viable for ships with sensor advantage
- Retreat/pursuit combat

**Example (6 hex sensors):**
- 7 hexes: 1.02× (+2% accuracy)
- 8 hexes: 0.93× (-7% accuracy)
- 9 hexes: 0.85× (-15% accuracy)
- 10 hexes: 0.77× (-23% accuracy)
- 11 hexes: 0.68× (-32% accuracy)
- 12 hexes: 0.60× (-40% accuracy)

**When to Use:**
- Retreating while still engaging
- Superior sensors let you shoot, enemy can't return fire
- Harassing enemy during pursuit
- Desperation shots

---

### Out of Range (Beyond 2× sensors)

**Accuracy Multiplier:** None (cannot target)

**Tactical Characteristics:**
- Completely beyond targeting capability
- Must close distance or improve sensors
- Enemy may escape
- Time to reposition or retreat

**When to Use:**
- Cannot engage, need tactical decision
- Close distance or let enemy escape
- Repair/regroup opportunity
- Strategic withdrawal

---

## Sensor Range by Ship Class

### Starting Ships (Rank 0-2)

**Miranda-class Frigate:**
- Base Sensors: 6 hexes
- Max Targeting: 12 hexes
- With Mk V Deflector: 8 hex sensors, 16 hex max

**Constitution-class Cruiser:**
- Base Sensors: 7 hexes
- Max Targeting: 14 hexes
- With Mk V Deflector: 9 hex sensors, 18 hex max

### Mid-Tier Ships (Rank 3-5)

**Excelsior-class:**
- Base Sensors: 8 hexes
- Max Targeting: 16 hexes
- With Mk X Deflector: 13 hex sensors, 26 hex max

**Ambassador-class:**
- Base Sensors: 9 hexes
- Max Targeting: 18 hexes
- With Mk X Deflector: 14 hex sensors, 28 hex max

### Advanced Ships (Rank 6-8)

**Galaxy-class Heavy Cruiser:**
- Base Sensors: 10 hexes
- Max Targeting: 20 hexes
- With Mk XV Deflector: 17 hex sensors, 34 hex max

**Sovereign-class:**
- Base Sensors: 11 hexes
- Max Targeting: 22 hexes
- With Mk XV Deflector: 18 hex sensors, 36 hex max

---

## Deflector Equipment Impact

### Sensor Range Bonus

**Formula:** `+1 hex per 2 marks`

| Mark | Bonus | Example (6 base) | Max Targeting |
|------|-------|------------------|---------------|
| Mk I | +0 hex | 6 hexes | 12 hexes |
| Mk II | +1 hex | 7 hexes | 14 hexes |
| Mk III | +1 hex | 7 hexes | 14 hexes |
| Mk IV | +2 hex | 8 hexes | 16 hexes |
| Mk V | +2 hex | 8 hexes | 16 hexes |
| Mk VI | +3 hex | 9 hexes | 18 hexes |
| Mk VII | +3 hex | 9 hexes | 18 hexes |
| Mk VIII | +4 hex | 10 hexes | 20 hexes |
| Mk IX | +4 hex | 10 hexes | 20 hexes |
| Mk X | +5 hex | 11 hexes | 22 hexes |
| Mk XI | +5 hex | 11 hexes | 22 hexes |
| Mk XII | +6 hex | 12 hexes | 24 hexes |
| Mk XIII | +6 hex | 12 hexes | 24 hexes |
| Mk XIV | +7 hex | 13 hexes | 26 hexes |
| Mk XV | +7 hex | 13 hexes | 26 hexes |

### Strategic Value

**Early Game (Mk I-IV):**
- Modest sensor improvements
- Focus on weapon/shield upgrades
- Sensor upgrades nice-to-have

**Mid Game (Mk V-X):**
- Significant range extensions
- Enables long-range tactics
- Competitive advantage in combat

**Late Game (Mk XI-XV):**
- Superior sensor range
- Dominate sensor warfare
- Shoot enemies before they can return fire
- Essential for elite combat

---

## System Damage Effects

### Sensor Health Impact

**Formula:** `effective_range = (base + bonus) × (sensor_health / 100)`

**Minimum:** 1 hex (sensors never completely fail)

| Sensor Health | Effective Range | Impact |
|---------------|-----------------|--------|
| 100% | Full range | Normal operations |
| 75% | 75% range | Noticeable reduction |
| 50% | 50% range | Severe handicap |
| 25% | 25% range | Critical, nearly blind |
| 10% | Minimum (1 hex) | Point blank only |

### Tactical Implications

**Sensor Priority:**
- Protect sensors in combat
- Target enemy sensors to gain advantage
- Emergency repairs critical
- Retreat if sensors critically damaged

**Combat Examples:**

**Galaxy-class with 50% sensor damage:**
- Base: 10 hexes
- Deflector Mk X: +5 hexes
- Total potential: 15 hexes
- At 50% health: 7.5 → **7 hexes effective**
- Max targeting: **14 hexes** (vs 30 at full health)

**Miranda-class with 25% sensor damage:**
- Base: 6 hexes
- No deflector
- At 25% health: 1.5 → **1 hex effective**
- Max targeting: **2 hexes** (basically blind)

---

## Code Usage

### Check Targeting Range

```python
from game.ships import create_starting_ship

ship = create_starting_ship()

# Get effective sensor range
sensor_range = ship.get_effective_sensor_range()
print(f"Sensor range: {sensor_range} hexes")
print(f"Max targeting: {sensor_range * 2} hexes")

# Check if target is in range
enemy_distance = 8
if ship.can_target(enemy_distance):
    print("Enemy in range!")
else:
    print("Enemy too far!")
```

### Calculate Accuracy

```python
# Get accuracy modifier for distance
distance = 5
accuracy = ship.get_targeting_accuracy(distance)

if accuracy is None:
    print("Cannot target")
else:
    # Apply to damage calculation
    base_damage = 100
    actual_damage = base_damage * accuracy
    print(f"Damage at {distance} hexes: {actual_damage}")
```

### Get Range Description

```python
# Get human-readable range info
for distance in range(0, 15):
    description = ship.get_range_description(distance)
    print(f"{distance} hexes: {description}")
```

### Combat Integration

```python
# Full combat accuracy calculation
def calculate_hit_chance(ship, target_distance, base_hit_chance=0.70):
    """
    Calculate final hit chance with sensor accuracy
    
    Args:
        ship: Firing ship
        target_distance: Distance to target in hexes
        base_hit_chance: Base weapon accuracy (0.0-1.0)
    
    Returns:
        Final hit chance (0.0-1.0)
    """
    # Check if in range
    if not ship.can_target(target_distance):
        return 0.0  # Cannot hit
    
    # Get accuracy modifier
    accuracy_mod = ship.get_targeting_accuracy(target_distance)
    
    # Apply to base hit chance
    final_chance = base_hit_chance * accuracy_mod
    
    # Clamp to 0.0-1.0
    return max(0.0, min(1.0, final_chance))

# Example usage
ship = create_starting_ship()

print("Hit chances at various ranges:")
for dist in [1, 3, 6, 9, 12]:
    chance = calculate_hit_chance(ship, dist)
    print(f"  {dist} hexes: {chance*100:.1f}% hit chance")
```

---

## Tactical Strategies

### Sensor Superiority

**Advantages:**
- Engage enemies before they can return fire
- Choose optimal engagement range
- Retreat while maintaining fire
- Control the battlefield

**How to Achieve:**
- High-mark deflector equipment
- Protect sensor systems
- Prioritize sensor upgrades
- Advanced ship classes

**Example:**
- Your ship: 15 hex sensors (30 max)
- Enemy ship: 6 hex sensors (12 max)
- Engage at 15-20 hexes
- You can shoot them (-10% to -23% accuracy)
- They cannot shoot you (out of range)

### Close Combat Specialist

**Advantages:**
- Maximum damage output
- Quick decisive battles
- Less reliant on sensors

**Disadvantages:**
- High risk, high reward
- Takes more damage
- Vulnerable to sensor-superior enemies

**Loadout:**
- Heavy weapons (torpedoes, heavy phasers)
- Strong shields and armor
- Fast impulse engines
- Adequate but not maxed sensors

### Balanced Approach

**Advantages:**
- Flexible tactical options
- Handle various enemies
- No critical weaknesses

**Loadout:**
- Mid-tier deflector (Mk V-X)
- Balanced weapons (energy + torpedoes)
- Good shields
- Standard engagement: sensor range (50%-100%)

---

## Future Enhancements

### Planned Features

1. **Sensor Jamming**
   - Equipment that reduces enemy sensor range
   - ECM/ECCM warfare

2. **Active Sensors**
   - Power allocation affects sensor range
   - Trade power for detection

3. **Passive Detection**
   - Detect enemies beyond sensor range
   - Cannot target, but aware of presence

4. **Sensor Scan Actions**
   - Spend turn scanning for tactical data
   - Reveals enemy stats, weak points

5. **Terrain Effects**
   - Nebulae reduce sensor range
   - Asteroid fields block sensors
   - Planetary interference

---

## Conclusion

The sensor system adds **tactical depth and strategic planning** to combat:

- **Range matters:** Close combat vs long-range engagements
- **Equipment choices:** Deflector upgrades provide real advantages
- **System management:** Protect sensors or suffer penalties
- **Ship design:** Sensor-heavy scouts vs brawlers
- **Combat tactics:** Positioning and range control crucial

Players must **balance offense, defense, and sensors** for optimal combat effectiveness!
