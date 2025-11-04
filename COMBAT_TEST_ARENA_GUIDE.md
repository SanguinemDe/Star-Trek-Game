# Combat Test Arena - User Guide

## 🎯 Overview

The Combat Test Arena allows you to test the AdvancedShip combat system in a controlled environment with two Odyssey-class starships.

## 🚀 How to Access

1. Launch the game: `python main.py`
2. Click **"COMBAT TEST"** on the main menu
3. You'll enter the arena with two ships ready for battle

## 🛸 Arena Setup

- **Player Ship:** USS Enterprise (NCC-1701-F) - Left side, facing right
- **Target Ship:** USS Target Drone (NX-99999) - Right side, facing left
- **Distance:** Approximately 16 hexes (adjustable by editing ship positions)

## 🎮 Controls

| Key | Action |
|-----|--------|
| **SPACE** | Fire all ready weapons |
| **ENTER** | End turn (advance cooldowns) |
| **R** | Reset arena (restore ships to full health) |
| **ESC** | Exit to main menu |

### Mouse Controls

| Button | Action |
|--------|--------|
| **FIRE WEAPONS** | Same as SPACE key |
| **END TURN** | Same as ENTER key |
| **RESET ARENA** | Same as R key |
| **EXIT TO MENU** | Same as ESC key |

## 📊 HUD Elements

### Main Arena (Center)
- Grid showing range (50 pixels = 1 hex)
- Two ships with sprite graphics
- Distance line with range measurement
- Range description (e.g., "LONG RANGE (-20% accuracy)")
- Hull status bars below each ship (green→orange→red)

### Right Panel - Ship Status
- **Hull:** Current/Max hull integrity
- **Shields:** All 4 arcs (Fore/Aft/Port/Starboard)
- **Weapons:** Status for each weapon array
  - GREEN "READY" = Can fire
  - RED "CD: X" = Cooldown remaining (X turns)
- **Sensor Range:** Effective sensor range in hexes
- **Crew:** Crew count and skill level

### Bottom Panel - Combat Log
- Last 3 combat messages
- Shows weapon hits, damage dealt, and results

### Top Display
- Turn number
- "YOUR TURN" / "ENEMY TURN" indicator

## ⚔️ Combat Mechanics

### Odyssey-Class Ship Stats

**Hull:** 5,000  
**Shields:** Fore 1,600 | Aft 1,400 | Port/Starboard 1,500 each

**Weapons:**
- **Mk XII Phaser Arrays:** 70 damage, fires every turn, 0 cooldown
- **Mk XII Photon Torpedoes:** 190 damage, 2-turn cooldown
- **Mk XII Quantum Torpedoes:** 210 damage, 3-turn cooldown

**Sensors:** 10 hex base range (12 hexes with Mk IV deflector)

### Fire Rates

- **Energy Weapons (Phasers):** Fire every turn (cooldown = 0)
- **Photon Torpedoes:** 2-turn cooldown after firing
- **Quantum Torpedoes:** 3-turn cooldown after firing

**Mark Bonuses:**
- Mk IV equipment = -1 turn cooldown
- Veteran crew (15% bonus) reduces cooldown by ~15%

### Range & Accuracy

Distance affects weapon accuracy based on sensor range:

| Range | Distance | Accuracy Modifier |
|-------|----------|-------------------|
| **Point Blank** | 0-1 hexes | +50% (1.5×) |
| **Close Range** | 2-6 hexes | +25% to +50% |
| **Sensor Range** | 7-12 hexes | +10% to +25% |
| **Long Range** | 13-24 hexes | -40% to +10% |
| **Out of Range** | >24 hexes | Cannot target |

**Example:** At 16 hexes (long range), accuracy is approximately -20%, so:
- Mk XII Phaser: 70 × 0.8 = **56 damage**
- Mk XII Photon: 190 × 0.8 = **152 damage**

### Torpedo Mechanics

Torpedoes have special penetration mechanics:
- **90% blocked by shields** (depletes shield energy)
- **10% bleeds through** to hull (even if shields up)
- **20% shield cost** (additional shield depletion)

**Example:** Photon torpedo deals 190 damage:
- Shield damage: 190 × 0.9 = **171 damage**
- Hull damage: 190 × 0.1 = **19 damage** (bypasses shields)

### Damage Application

Currently, all damage hits the **fore shields** (simplified for testing).

**Future Implementation:**
- Damage will hit shields based on attacker's position
- Port/Starboard/Aft shields will be used based on facing
- Shield transfer between arcs
- System damage from hull hits

## 🧪 Testing Scenarios

### Test 1: Fire Rate Verification
1. Press SPACE to fire all weapons
2. Note which weapons show "READY" vs "CD: X"
3. Press ENTER to end turn
4. Observe cooldowns decrease by 1
5. Verify phasers are always ready, torpedoes have cooldowns

### Test 2: Range & Accuracy
1. Note the distance between ships (shown on line)
2. Fire weapons with SPACE
3. Compare actual damage to weapon's base damage
4. Verify accuracy modifier matches range description
5. Example: At 16 hexes ("LONG RANGE -20%"), phaser should deal ~56 dmg (70 × 0.8)

### Test 3: Torpedo Penetration
1. Fire torpedoes at target
2. Check combat log for damage split
3. Verify ~90% hits shields, ~10% hits hull
4. Example: 190 damage photon → ~171 shield, ~19 hull

### Test 4: Shield Depletion
1. Fire multiple volleys at target
2. Watch fore shields decrease
3. Once shields reach 0, verify all damage goes to hull
4. Note: Currently simplified to fore shields only

### Test 5: Hull Destruction
1. Continue firing until target hull reaches 0
2. Combat log should show "*** Target Drone DESTROYED! ***"
3. Reset arena with R key to continue testing

### Test 6: Turn-Based System
1. Fire weapons (some will go on cooldown)
2. End turn (target doesn't attack, it's a dummy)
3. Verify turn counter increases
4. Verify cooldowns advance by 1 turn
5. Verify weapons come back online after cooldown expires

## 🔧 Testing Checklist

Use this checklist to verify combat mechanics:

- [ ] Phasers fire every turn (0 cooldown)
- [ ] Photon torpedoes have 2-turn cooldown
- [ ] Quantum torpedoes have 3-turn cooldown
- [ ] Cooldowns decrease by 1 each turn
- [ ] Accuracy decreases with distance
- [ ] Point blank range gives +50% damage boost
- [ ] Long range gives -20 to -40% damage penalty
- [ ] Out of sensor range prevents targeting
- [ ] Torpedoes deal ~10% hull damage even with shields up
- [ ] Torpedoes deal ~90% shield damage
- [ ] Combat log shows accurate damage numbers
- [ ] Hull bars change color (green→orange→red)
- [ ] Ship is destroyed when hull reaches 0
- [ ] Reset button restores ships to full health

## 📝 Known Limitations (Test Arena)

1. **Target doesn't fight back** - It's a static target for testing
2. **No movement** - Ships are stationary
3. **No facing** - All attacks hit fore shields
4. **No system damage** - Hull damage doesn't affect systems
5. **No shield regeneration** - Shields don't recharge
6. **No crew casualties** - Damage doesn't reduce crew count
7. **Simplified damage** - No armor calculation, no critical hits

These limitations are intentional for focused testing. The full combat system will include all these features.

## 🎯 What to Test

Focus on these areas:

### 1. Weapon Balance
- Do weapons feel powerful enough?
- Is the damage-to-cooldown ratio fair?
- Do marks provide meaningful upgrades?
- Are energy weapons vs torpedoes balanced?

### 2. Range System
- Does distance feel meaningful?
- Are accuracy modifiers fair?
- Is sensor range appropriate?
- Should long-range combat be more/less penalized?

### 3. Fire Rate System
- Do cooldowns feel right?
- Is waiting 2-3 turns for torpedoes acceptable?
- Does crew skill bonus matter?
- Should energy weapons have cooldowns?

### 4. Damage Values
- How many hits to destroy an Odyssey?
- Is combat too fast or too slow?
- Are shields effective enough?
- Does torpedo penetration feel right?

## 🐛 Report Issues

If you find bugs or balance issues, note:
- What you did (step-by-step)
- What you expected
- What actually happened
- Any error messages

## 🚀 Future Enhancements

Planned additions to the combat system:

1. **Ship Movement** - Move and rotate ships
2. **Enemy AI** - Target fights back
3. **Facing Mechanics** - Damage different shield arcs
4. **System Damage** - Hull hits damage ship systems
5. **Shield Regeneration** - Shields recharge over time
6. **Power Management** - Allocate power to systems
7. **Special Abilities** - Attack patterns, evasive maneuvers
8. **Multiple Enemies** - Fight 2-3 ships at once
9. **Environmental Hazards** - Asteroids, nebulae
10. **Victory Conditions** - Objectives beyond "destroy enemy"

## 📖 Related Documentation

- **MARK_SYSTEM_DOCUMENTATION.md** - Equipment progression system
- **FIRE_RATE_SYSTEM.md** - Weapon cooldown mechanics
- **SENSOR_SYSTEM_DOCUMENTATION.md** - Range and accuracy system
- **SHIP_SYSTEM_BREAKDOWN.md** - Complete ship system overview

---

**Live long and prosper!** 🖖

_Ready to test combat? Launch the arena and start firing!_
