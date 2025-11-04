# Star Trek Game - Crew Officer System

## Overview
The crew officer system allows captains to recruit specialized officers for their ship's bridge stations. Each officer has unique skills, species bonuses, and provides station-specific bonuses to ship operations.

## Features

### Officers
- **10 Rank Levels**: Ensign → Lieutenant JG → Lieutenant → Lt. Commander → Commander → Captain → Commodore → Rear Admiral → Vice Admiral → Admiral
- **9 Species Available**: Human, Vulcan, Andorian, Tellarite, Betazoid, Trill, Bajoran, Caitian, Klingon
- **5 Skills**: Command, Tactical, Science, Engineering, Diplomacy
- **Species Bonuses**: Each species has unique skill bonuses (e.g., Vulcans +10 Science, Andorians +10 Tactical)
- **Extensive Name Lists**: 40+ first names and 30+ last names per species for authentic character generation

### Bridge Stations
1. **Conn Officer** (Helm/Navigation)
   - Primary Skill: Tactical
   - Effects: Evasion, Navigation Speed, Initiative

2. **Tactical Officer** (Weapons/Shields)
   - Primary Skill: Tactical
   - Effects: Weapons Accuracy, Shield Efficiency, Targeting

3. **Chief Engineer** (Systems/Power)
   - Primary Skill: Engineering
   - Effects: Repair Rate, Power Efficiency, Warp Speed, System Reliability

4. **Science Officer** (Sensors/Research)
   - Primary Skill: Science
   - Effects: Scanning Range, Anomaly Detection, Analysis Speed

5. **Chief Medical Officer** (Sickbay)
   - Primary Skill: Science
   - Effects: Crew Recovery, Medical Efficiency, Combat Casualty Reduction

6. **Communications Officer** (Subspace Comms)
   - Primary Skill: Diplomacy
   - Effects: Diplomacy Bonus, Hailing Range, Translation Accuracy

### Recruitment System
- **Recruitment Pool**: 15 randomly generated officers available at starbases
- **Rank Restrictions**: Can only recruit officers below your current rank
- **Reputation Cost**: Based on officer's rank and total skill levels
  - Ensign: 50+ reputation
  - Lieutenant: 200+ reputation
  - Commander: 550+ reputation
  - Admiral: 2300+ reputation
- **Pool Refresh**: Automatically refreshes every 30 stardates
- **Weighted Generation**: Lower ranks are more common than higher ranks

### Station Bonuses
Officers provide percentage bonuses to their station's operations based on their primary skill:
- **Formula**: Bonus = (Skill - 30) / 5
- **Example**: Officer with 70 Tactical skill = +8% bonus
- **Range**: 0% (skill 30) to 20% (skill 130)

### Crew Management
- **View Current Crew**: See all assigned officers and their bonuses
- **Recruit Officers**: Browse available officers by rank, species, and skills
- **Reassign Officers**: Move officers between stations or swap positions
- **Dismiss Officers**: Remove officers from your crew
- **Skill Comparison**: View officer skills with primary skill highlighted

## Skill Generation
Officer skills are generated based on rank level:
- **Base Skill**: 30 + (Rank Level × 7)
  - Ensign (Rank 0): 30-40
  - Commander (Rank 4): 58-68
  - Admiral (Rank 9): 93-103
- **Variance**: ±10 points per skill
- **Species Bonuses**: Applied after base generation
- **Total Range**: 30-110+ (with species bonuses)

## Species Bonuses
- **Human**: Command +5, Diplomacy +5
- **Vulcan**: Science +10, Diplomacy +5
- **Andorian**: Tactical +10, Command +5
- **Tellarite**: Engineering +10, Diplomacy -5
- **Betazoid**: Diplomacy +15, Science +5
- **Trill**: Science +5, Command +5, Diplomacy +5
- **Bajoran**: Diplomacy +5, Science +5
- **Caitian**: Tactical +10, Science +5
- **Klingon**: Tactical +15, Command +5, Diplomacy -10

## Integration Points

### Ship Class (federation_ship.py)
- Add `crew_roster` dictionary: `{station_name: Officer}`
- Add methods to calculate crew bonuses
- Apply bonuses to ship operations

### Combat System (combat.py)
- Tactical Officer: Increase weapon hit chance and damage
- Conn Officer: Improve evasion chance
- Engineering Officer: Faster emergency repairs
- Medical Officer: Reduce crew casualties

### Exploration System (exploration.py)
- Science Officer: Improved scan results and anomaly detection
- Communications Officer: Better first contact outcomes
- Add "Crew Recruitment" option at starbases

### Save System (game_state.py)
- Save crew roster and officer details
- Save recruitment pool state
- Load and restore Officer objects

## Usage Example

### At a Starbase:
```
CREW RECRUITMENT
Your Rank: Commander (Level 4)
Reputation: 850

CURRENT BRIDGE CREW:
Conn Officer           : Lieutenant    James Kirk         (Bonus: +6.5%)
Tactical Officer       : Lt. Commander  Worf              (Bonus: +10.2%)
Chief Engineer         : (Empty)

1. View Available Officers
2. Manage Current Crew
3. Station Information
4. Return to Station

> 1

AVAILABLE OFFICERS
#   Rank            Name                 Species      Cost    CMD  TAC  SCI  ENG  DIP
1   Ensign          T'Pol of Vulcan      Vulcan       215     35   38   52   40   45   ✓
2   Lieutenant      Thy'lek th'Thane     Andorian     380     48   65   42   45   40   ✓
3   Lt. Commander   Montgomery Scott     Human        520     55   50   48   70   52   ✓
4   Commander       Beverly Crusher      Human        890     60   48   68   55   62   ✗
```

## Implementation Status
✅ Officer class with skills and species bonuses
✅ Extensive name lists for all 9 species
✅ 6 bridge stations with defined effects
✅ Recruitment pool generation
✅ Recruitment interface
✅ Crew management (view, reassign, dismiss)
✅ Station information display
⏳ Ship class integration
⏳ Combat system integration
⏳ Exploration system integration
⏳ Save/load system integration

## Files
- `game/crew.py`: Officer class, station definitions, name lists
- `game/crew_recruitment.py`: Recruitment pool, recruitment interface, crew management
- `CREW_SYSTEM.md`: This documentation file
