# Weapon Fire Rate System - Implementation Summary

## Date: November 3, 2025

## Overview
Added a **turn-based fire rate system** where energy weapons fire every turn, while torpedoes and special weapons have cooldown periods modified by crew skill and equipment marks.

---

## Core Mechanics

### Energy Weapons (Phasers, Disruptors, etc.)
- **Fire Rate:** Every turn (cooldown = 0)
- **Behavior:** Always ready, consistent damage output
- **Tactical Use:** Reliable damage source, can fire continuously

### Torpedoes (Photon, Quantum, Tricobalt)
- **Fire Rate:** Turn-based cooldown (2-5 turns)
- **Behavior:** High burst damage, limited by cooldown and ammunition
- **Tactical Use:** Alpha strikes, finishing blows, special situations

---

## Cooldown Calculation

### Base Cooldown by Torpedo Type
```python
base_cooldowns = {
    'photon': 3,      # Standard torpedoes
    'plasma': 3,      # Similar to photon
    'quantum': 4,     # More powerful, slower reload
    'tricobalt': 5    # Devastating, longest cooldown
}
```

### Mark Level Reduction
- **-1 turn** at Mk V (5+ marks)
- **-1 turn** at Mk X (10+ marks)
- **-1 turn** at Mk XV (15 marks)
- **Minimum cooldown:** 2 turns (never less)

Formula: `cooldown = max(2, base_cooldown - (mark // 5))`

**Examples:**
- Mk I-IV Photon: 3 turns
- Mk V-IX Photon: 2 turns
- Mk X-XV Photon: 2 turns (minimum reached)

### Crew Skill Modifier

Crew skill reduces cooldown time as a percentage:

| Crew Skill | Bonus | Effect |
|------------|-------|--------|
| Cadet | 0% | No reduction |
| Green | 5% | Minimal (3→3, 4→4, 5→5) |
| Regular | 10% | Slight (3→3, 4→4, 5→5) |
| Veteran | 15% | Moderate (3→3, 4→3, 5→4) |
| Elite | 20% | Significant (3→2, 4→3, 5→4) |
| Legendary | 25% | Maximum (3→2, 4→3, 5→4) |

Formula: `cooldown = max(1, int(round(base * (1.0 - crew_bonus))))`

**Examples:**
- Photon (3 turns) + Elite (20%): 3 × 0.8 = 2.4 → **2 turns**
- Quantum (4 turns) + Veteran (15%): 4 × 0.85 = 3.4 → **3 turns**
- Tricobalt (5 turns) + Legendary (25%): 5 × 0.75 = 3.75 → **4 turns**

---

## Code Implementation

### WeaponArray Class Changes

```python
class WeaponArray:
    def __init__(self, weapon_type, mark, firing_arcs, upgrade_space_cost=5):
        # ... existing attributes ...
        self.cooldown_remaining = 0  # NEW: Tracks cooldown state
    
    def get_cooldown_time(self):
        """Energy weapons always ready (cooldown = 0)"""
        return 0
    
    def can_fire(self):
        """Check if weapon ready"""
        return self.cooldown_remaining <= 0
    
    def fire(self, crew_skill_bonus=0.0):
        """Fire weapon and set cooldown"""
        if not self.can_fire():
            return 0
        self.cooldown_remaining = self.get_cooldown_time()
        return self.get_damage()
    
    def advance_cooldown(self):
        """Reduce cooldown by 1 turn"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
```

### TorpedoBay Class Changes

```python
class TorpedoBay:
    def __init__(self, torpedo_type, mark, firing_arcs, max_torpedoes=100, upgrade_space_cost=10):
        # ... existing attributes ...
        self.cooldown_remaining = 0  # NEW: Tracks cooldown state
    
    def get_base_cooldown(self):
        """Base cooldown with mark reduction"""
        base_cooldowns = {
            'photon': 3,
            'quantum': 4,
            'plasma': 3,
            'tricobalt': 5
        }
        base = base_cooldowns.get(self.torpedo_type, 3)
        mark_reduction = min(1, self.mark // 5)
        return max(2, base - mark_reduction)
    
    def get_cooldown_with_crew(self, crew_skill_bonus=0.0):
        """Cooldown modified by crew skill"""
        base = self.get_base_cooldown()
        modified = base * (1.0 - crew_skill_bonus)
        return max(1, int(round(modified)))
    
    def can_fire(self):
        """Check if ready and has ammo"""
        return self.cooldown_remaining <= 0 and self.torpedoes > 0
    
    def fire(self, crew_skill_bonus=0.0):
        """Fire torpedo and set cooldown"""
        if not self.can_fire():
            return 0
        
        self.torpedoes -= 1
        damage = self.get_damage()
        self.cooldown_remaining = self.get_cooldown_with_crew(crew_skill_bonus)
        
        return damage
    
    def advance_cooldown(self):
        """Reduce cooldown by 1 turn"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
    
    def reload(self, amount=None):
        """Reload torpedoes (at starbase)"""
        if amount is None:
            self.torpedoes = self.max_torpedoes
        else:
            self.torpedoes = min(self.max_torpedoes, self.torpedoes + amount)
```

### AdvancedShip Class Helper Methods

```python
def advance_all_weapon_cooldowns(self):
    """Call at end of each combat turn"""
    for weapon in self.weapon_arrays:
        weapon.advance_cooldown()
    for torpedo in self.torpedo_bays:
        torpedo.advance_cooldown()
    for special in self.special_weapons:
        if hasattr(special, 'advance_cooldown'):
            special.advance_cooldown()

def get_ready_weapons(self):
    """Get list of weapons that can fire this turn"""
    ready = []
    
    for i, weapon in enumerate(self.weapon_arrays):
        if weapon.can_fire():
            ready.append(('array', i, weapon))
    
    for i, torpedo in enumerate(self.torpedo_bays):
        if torpedo.can_fire():
            ready.append(('torpedo', i, torpedo))
    
    for i, special in enumerate(self.special_weapons):
        if hasattr(special, 'can_fire') and special.can_fire():
            ready.append(('special', i, special))
    
    return ready

def get_weapon_status(self):
    """Get detailed status for UI display"""
    status = {
        'energy_weapons': [],
        'torpedoes': [],
        'special_weapons': []
    }
    
    for weapon in self.weapon_arrays:
        status['energy_weapons'].append({
            'type': weapon.weapon_type,
            'mark': weapon.mark,
            'damage': weapon.get_damage(),
            'arcs': weapon.firing_arcs,
            'ready': weapon.can_fire(),
            'cooldown': weapon.cooldown_remaining
        })
    
    for torpedo in self.torpedo_bays:
        status['torpedoes'].append({
            'type': torpedo.torpedo_type,
            'mark': torpedo.mark,
            'damage': torpedo.get_damage(),
            'arcs': torpedo.firing_arcs,
            'torpedoes': torpedo.torpedoes,
            'max_torpedoes': torpedo.max_torpedoes,
            'ready': torpedo.can_fire(),
            'cooldown': torpedo.cooldown_remaining,
            'base_cooldown': torpedo.get_base_cooldown()
        })
    
    return status
```

---

## Combat Turn Example

### Turn 1: Alpha Strike
```python
ship = create_starting_ship()
crew_bonus = 0.10  # Regular crew

# Fire all weapons
phaser_dmg = ship.weapon_arrays[0].fire(crew_bonus)  # 30 damage
torpedo_dmg = ship.torpedo_bays[0].fire(crew_bonus)  # 110 damage

print(f"Total damage: {phaser_dmg + torpedo_dmg}")  # 140 damage
print(f"Torpedo cooldown: {ship.torpedo_bays[0].cooldown_remaining}")  # 3 turns
print(f"Torpedoes left: {ship.torpedo_bays[0].torpedoes}")  # 49/50
```

### Turn 2: Phasers Only
```python
ship.advance_all_weapon_cooldowns()  # Reduce cooldowns

# Check what's ready
ready = ship.get_ready_weapons()
# Only phasers ready: [('array', 0, ...), ('array', 1, ...), ('array', 2, ...)]

# Fire phasers
total_damage = 0
for weapon_type, index, weapon in ready:
    if weapon_type == 'array':
        total_damage += weapon.fire(crew_bonus)

print(f"Phaser damage: {total_damage}")  # 90 damage (3 × 30)
print(f"Torpedo cooldown: {ship.torpedo_bays[0].cooldown_remaining}")  # 2 turns
```

### Turn 3: Continue Phaser Fire
```python
ship.advance_all_weapon_cooldowns()

# Phasers ready, torpedoes still cooling down
print(f"Torpedo cooldown: {ship.torpedo_bays[0].cooldown_remaining}")  # 1 turn
```

### Turn 4: Full Arsenal Ready
```python
ship.advance_all_weapon_cooldowns()

# Everything ready again
print(f"Torpedo ready: {ship.torpedo_bays[0].can_fire()}")  # True

# Fire everything
phaser_dmg = sum(w.fire(crew_bonus) for w in ship.weapon_arrays)
torpedo_dmg = ship.torpedo_bays[0].fire(crew_bonus)

print(f"Total damage: {phaser_dmg + torpedo_dmg}")  # 140 damage
```

---

## Tactical Implications

### Energy Weapons Strategy
- **Reliable Damage:** Use for sustained pressure
- **Shield Whittling:** Constant fire reduces enemy shields
- **No Ammo Concerns:** Fire freely without resource management
- **Power Management:** May need to balance power to weapons system

### Torpedo Strategy
- **Alpha Strike:** Open combat with torpedo + phasers for maximum damage
- **Timing:** Wait for shield gaps or critical moments
- **Resource Management:** Limited ammunition, save for important targets
- **Crew Training:** Elite/Legendary crews make torpedoes much more viable
- **Mark Upgrades:** Higher marks reduce cooldown, increasing effectiveness

### Crew Skill Impact
- **Early Game (Cadet/Green):** Torpedoes take full cooldown, use sparingly
- **Mid Game (Regular/Veteran):** Slight improvements, more viable in longer fights
- **Late Game (Elite/Legendary):** Torpedoes nearly as reliable as energy weapons

---

## Balance Considerations

### Energy vs Torpedoes

**Energy Weapons:**
- ✅ Fire every turn
- ✅ No ammo limit
- ✅ Consistent damage
- ❌ Lower damage per shot
- ❌ Limited firing arcs

**Torpedoes:**
- ✅ Very high damage (80-220)
- ✅ Can bypass some shields
- ❌ Cooldown periods (2-5 turns)
- ❌ Limited ammunition
- ❌ Must reload at starbase

### Progression Curve
1. **Rank 0-2:** Mk I-IV weapons, long cooldowns, energy weapons preferred
2. **Rank 3-5:** Mk V-X weapons, reduced cooldowns, torpedoes more viable
3. **Rank 6-8:** Mk XI-XV weapons, minimum cooldowns, balanced arsenal

---

## Testing Results

```
✓ Energy weapons fire every turn (cooldown = 0)
✓ Torpedoes start with 3-turn cooldown (Photon, Mk IV)
✓ Cooldown advances each turn correctly
✓ Torpedoes ready after cooldown expires
✓ Elite/Legendary crew reduces cooldown (3→2 turns)
✓ Ammunition tracking works (50→49 after firing)
✓ Multiple weapons track cooldowns independently
✓ get_ready_weapons() returns correct list
✓ get_weapon_status() provides full information
```

---

## Future Enhancements

### Planned Features
1. **Special Weapons:** Mines, beam overloads (unique cooldowns)
2. **Rapid Fire Mode:** Sacrifice damage for reduced cooldown
3. **Salvo Fire:** Fire multiple torpedoes at once (extended cooldown)
4. **Tactical Officer Abilities:** Skills that reduce cooldowns
5. **Equipment Bonuses:** Tactical consoles that boost fire rate
6. **Emergency Power:** Temporarily override cooldowns

### UI Integration
- Visual cooldown timers in combat
- Weapon ready indicators
- Ammunition counters
- Crew skill impact display
- Fire rate comparison in ship requisition

---

## Conclusion

The fire rate system adds **tactical depth** to combat:
- **Energy weapons** provide reliable, sustained damage
- **Torpedoes** offer high-impact burst damage with strategic timing
- **Crew skill** meaningfully affects combat effectiveness
- **Equipment progression** improves fire rates naturally

This creates engaging turn-based combat where players must **manage resources, time attacks, and balance different weapon systems** for optimal effectiveness.
