# Star Trek: Federation Command

A comprehensive Star Trek simulation game with a graphical LCARS-style interface where you take on the role of a Starfleet captain, managing your ship, crew, and career across a procedurally generated galaxy with famous canonical Star Trek locations.

## Features

### 🚀 Core Gameplay
- **LCARS GUI Interface**: Authentic Star Trek LCARS-themed graphical interface with multiple theme options
- **Theme System**: ⭐ NEW! Choose between LCARS V1 (classic TNG) and LCARS V2 (modern Discovery/Picard) styles!
- **Combat Test Arena**: ⭐ Fully functional hex-based tactical combat system with 8-phase turns
- **Character Creation**: Create your captain with 9 species including the agile Caitian race
- **Career Progression**: Rise through the ranks from Lieutenant Commander to Fleet Admiral
- **Mission System**: ⭐ Accept missions at starbases - 12 mission types from patrol duty to temporal investigations!
- **Crew Officer System**: ⭐ Recruit specialized bridge officers for 6 stations with unique bonuses!
- **Ship Requisition System**: Command 64 different canonical Federation starships - earn reputation to unlock legendary vessels from Miranda-class to the mighty Odyssey-class!
- **Reputation System**: Earn reputation through missions, exploration, combat, and diplomacy to purchase better ships and recruit elite officers
- **Galaxy Exploration**: Navigate a procedurally generated galaxy with 200+ star systems
- **Canonical Systems**: Visit famous locations like Earth (Sol), Vulcan, Qo'noS, Romulus, Bajor, and more

### 🌌 Exploration
- Scan star systems for planets, anomalies, and resources
- Discover new civilizations and phenomena
- Investigate spatial anomalies
- Chart unexplored space
- Land on planets and survey for resources

### ⚔️ Combat System
**NEW: Hex-Based Tactical Combat Arena** ⭐
- **8-Phase Turn System**: Initiative, Movement, Targeting, Firing, Damage, Power, Repair, Housekeeping
- **Hex Grid Movement**: WASD controls with turning rules (must move before turning)
- **Multi-Targeting**: Select up to 3 targets with accuracy penalties (100%/75%/50%)
- **Shield Arc System**: Damage applied to correct facing (fore/aft/port/starboard)
- **Weapon Arcs**: Tactical firing arcs based on ship facing
- **Range Bands**: Point Blank, Close, Medium, Long, Extreme
- **AI Opponents**: Intelligent enemy AI with personalities (Aggressive, Defensive, Balanced, Sniper)
- **Smooth Animation**: Cubic ease-in-out interpolation for movement and rotation
- **Mark System**: Mk I-XV weapon progression (Mk XII Phasers = 70 damage!)
- **Tabbed UI**: STATUS, WEAPONS, POWER, DAMAGE panels for complete ship information

See **COMBAT_TEST_ARENA_GUIDE.md** for complete combat mechanics!

### 🤝 Diplomacy
- Manage relations with 7 major factions:
  - United Federation of Planets
  - Klingon Empire
  - Romulan Star Empire
  - Cardassian Union
  - Ferengi Alliance
  - Borg Collective
  - The Dominion
- Negotiate treaties and trade agreements
- Resolve conflicts peacefully
- First contact protocols

### 👥 Crew Officer System
Build your bridge crew with specialized officers for enhanced ship performance:

**6 Bridge Stations:**
- **Conn Officer**: Improves evasive maneuvers and ship handling (+bonus to evasion in combat)
- **Tactical Officer**: Enhances weapon accuracy and damage (+bonus to phaser/torpedo systems)
- **Engineering Officer**: Boosts shield restoration and power management (+bonus to shield repairs)
- **Science Officer**: Increases success rate for anomaly investigations (+30% bonus to discoveries)
- **Medical Officer**: Reduces casualty rates and improves crew recovery (effects vary)
- **Communications Officer**: Enhances diplomacy and first contact outcomes (+20-30% to negotiations)

**Officer Features:**
- **10 Rank Levels**: Ensign → Lieutenant → Lt. Commander → Commander → Captain → Fleet Captain → Commodore → Rear Admiral → Vice Admiral → Admiral
- **Skill-Based Bonuses**: Officers provide 0-20%+ bonuses based on their skill levels (Formula: `(skill - 30) / 5`)
- **Reputation Costs**: Higher-ranked officers cost more reputation (50-2300+)
- **Rank Restrictions**: Cannot recruit officers at or above your captain's rank
- **Diverse Crew**: 300+ authentic names across 9 species (Human, Vulcan, Andorian, Tellarite, Trill, Bajoran, Betazoid, Caitian, Bolian)
- **Dynamic Pool**: Recruitment pool refreshes every 30 stardates with 15 available officers
- **Crew Management**: Assign, reassign, and dismiss officers as needed

**Where to Recruit:**
- Visit any starbase or station
- Access "Crew Recruitment" from the station menu
- Review available officers' ranks, species, and reputation costs
- Assign officers to specific bridge stations for immediate bonuses

📖 **See CREW_SYSTEM.md for complete crew mechanics and integration details!**

### 👥 Away Team Missions
- Deploy away teams to planetary surfaces
- Multiple mission types:
  - Exploration and survey
  - Resource gathering
  - First contact
  - Rescue operations
- Prime Directive considerations

### 🛸 Ship Systems
- **24 Canonical Federation Ships**: Miranda, Constitution, Excelsior, Intrepid, Defiant, Galaxy, Sovereign, Prometheus, Odyssey, Enterprise-J, and many more!
- **Progression System**: Start in a Miranda-class and work your way up through rank and reputation
- **Ship Requirements**: Each vessel has rank and reputation requirements (Enterprise-J needs Admiral rank!)
- Hull integrity and shield management
- Warp drive navigation
- Dilithium crystal management
- Crew morale system
- Key personnel roster
- System damage and repairs

### 📊 Career Features
- Skill progression (Command, Tactical, Science, Engineering, Diplomacy)
- Experience and leveling system
- **Reputation Points**: Earned through exploration, combat victories, diplomacy, and first contact
- **Ship Requisition**: Use reputation to purchase progressively more powerful starships
- Captain's log
- Mission tracking
- Commendations and achievements
- Save/Load game functionality

## Installation

### Requirements
- Python 3.7 or higher
- Pygame library (for graphical interface)

### Setup
1. Clone or download this repository
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. Navigate to the game directory
4. Run the game:
```powershell
python main.py
```

### Quick Test - Combat Arena
To jump straight into tactical combat testing:
1. Launch the game
2. Select "COMBAT TEST" from the main menu
3. Control your ship with WASD keys and test the hex-based combat system

See **COMBAT_TEST_ARENA_GUIDE.md** for detailed combat mechanics and controls.

## How to Play

### Starting a New Game
1. Run `python main.py`
2. Select "New Game" from the main menu
3. Create your character:
   - Choose your name
   - Select species (affects starting attributes)
   - Choose background (Command, Tactical, Science, Engineering, or Diplomatic)
4. Review your starting ship and begin your career!

### Controls
The game uses a numbered menu system. Simply enter the number corresponding to your choice and press Enter.

### Key Commands
- **Navigation**: Travel between star systems using warp drive
- **Scan Sector**: Explore your current location
- **Ship Status**: View detailed ship information
- **Crew Management**: Manage your crew and improve morale
- **Communications**: Interact with other factions
- **Away Team**: Deploy landing parties to planets
- **Ship Requisition**: ⭐ NEW! Purchase new ships with reputation points
- **Captain's Log**: Review your journey
- **Save Game**: Save your progress

## Ship Progression System

### How It Works
All captains start in a **Miranda-class** light cruiser. To command more powerful vessels, you must:
1. **Earn Reputation Points** through exploration, combat, diplomacy, and missions
2. **Achieve Required Rank** by gaining experience
3. **Purchase Ships** from Starfleet Ship Requisition

### Earning Reputation
- **Missions**: ⭐ +15 to +100 per mission (primary source!)
- **Exploration**: +5 per new system discovered, +10 for canonical systems
- **Combat**: +5 to +50 depending on enemy difficulty
- **Diplomacy**: +10 for trade, +25 for combat resolution, +50 for alliances
- **First Contact**: +30 for successful first contact
- **Experience Bonus**: Gain 50% of experience as reputation

### Ship Tiers
- **Tier 1 (0-500 Rep)**: Miranda, Oberth, Constitution
- **Tier 2 (500-1500 Rep)**: Excelsior, Ambassador, Intrepid, Defiant
- **Tier 3 (1500-3000 Rep)**: Galaxy, Sovereign, Prometheus, Vesta
- **Tier 4 (3000-6000 Rep)**: Odyssey, Venture
- **Tier 5 (6000+ Rep)**: Universe, Yorktown, Enterprise-J

### Featured Ships
- **Miranda-class**: Starting ship, reliable workhorse
- **Constitution-class**: Legendary TOS explorer (Enterprise!)
- **Defiant-class**: Tough little ship, anti-Borg warship
- **Intrepid-class**: Long-range science vessel (Voyager!)
- **Galaxy-class**: Flagship explorer (Enterprise-D!)
- **Sovereign-class**: Premier battlecruiser (Enterprise-E!)
- **Prometheus-class**: Advanced multi-vector assault ship
- **Odyssey-class**: Massive 25th-century star cruiser
- **Enterprise-J**: Ultimate Universe-class dreadnought

📖 **See SHIP_SYSTEM.md for complete ship list and detailed progression guide!**

## Gameplay Tips

### For New Captains
1. **Accept missions at starbases** ⭐ - Primary way to earn reputation!
2. **Recruit bridge officers early** ⭐ - Even basic officers provide significant combat/exploration bonuses
3. **Start by exploring Sol system** - Familiarize yourself with the game mechanics
4. **Dock at starbases** - Access mission board, crew recruitment, repair ship, and restock supplies
5. **Manage resources** - Keep an eye on your dilithium reserves
6. **Build relationships** - Good diplomatic relations open new opportunities
7. **Train your crew** - Higher morale means better performance
8. **Save regularly** - Use the save feature to preserve your progress

### Advanced Strategies
1. **Stack missions** ⭐ - Accept up to 3 missions at once for efficient reputation gains
2. **Prioritize key stations** ⭐ - Tactical and Engineering officers provide immediate combat advantages
3. **Balance your skills** - Don't neglect any attribute; missions require specific skills
4. **Choose battles wisely** - Not every conflict needs to end in combat
5. **Explore systematically** - Map out the galaxy methodically
6. **Upgrade officers with rank** ⭐ - As you advance ranks, recruit higher-ranked officers for better bonuses
7. **Resource management** - Plan your routes to minimize dilithium consumption
8. **Crew morale matters** - Happy crews perform better in all situations
9. **Mission difficulty** ⭐ - Match mission requirements to your skills for best success rates
10. **Plan your ship upgrades** ⭐ - Save reputation for ships that match your playstyle
11. **Check recruitment pool regularly** ⭐ - Pool refreshes every 30 stardates with new officers

## Ship Classes

### Starting Ships
- **Miranda-class**: Light cruiser, balanced capabilities
- **Intrepid-class**: Science vessel, excellent sensors
- **Defiant-class**: Escort, heavy weapons

### Advanced Ships (Unlockable)
- **Constitution-class**: Classic heavy cruiser
- **Excelsior-class**: Fast heavy cruiser
- **Galaxy-class**: Explorer, largest crew capacity
- **Sovereign-class**: Battlecruiser, most powerful

## Species Bonuses

- **Human**: +5 Diplomacy (versatile)
- **Vulcan**: +10 Science, +5 Engineering, +5 Diplomacy (logical)
- **Andorian**: +10 Tactical, +5 Command, -5 Diplomacy (warriors)
- **Tellarite**: +10 Engineering (technical)
- **Betazoid**: +10 Diplomacy, +5 Science (empathic)
- **Trill**: +5 Command, +5 Science, +5 Diplomacy (joined)
- **Bajoran**: +5 Tactical, +5 Engineering (spiritual)
- **Caitian**: ⭐ NEW! +10 Tactical, +5 Science (agile hunters)
- **Klingon**: +15 Tactical, +5 Command, -5 Science, -10 Diplomacy (warriors)

## Faction Relations

Relations range from -100 (At War) to +100 (Allied):
- **80+**: Allied
- **50-79**: Friendly
- **20-49**: Neutral
- **-19-19**: Unfriendly
- **-50--20**: Hostile
- **Below -50**: At War

## Save System

- Saves are stored in the `saves/` directory
- Default save file: `savegame.json`
- Save files include all game state, character progress, and galaxy data
- You can have multiple save files by renaming them

## Future Enhancements

Potential features for future updates:
- Multiple save slots
- More ship classes and upgrades
- Complex mission storylines
- Crew personalities and interactions
- Trade and economy system
- Fleet command (multiple ships)
- Multiplayer elements
- Graphics/GUI version
- Sound effects and music
- More complex combat tactics
- Ship customization
- Random events and encounters

## Development

### Project Structure
```
Star Trek Game/
├── main.py                 # Main game loop
├── game/
│   ├── __init__.py
│   ├── game_state.py      # Game state management
│   ├── character.py       # Character creation and management
│   ├── ship.py            # Ship systems and crew roster
│   ├── ship_requisition.py # Ship purchase system
│   ├── galaxy.py          # Galaxy and star system generation
│   ├── ui.py              # User interface
│   ├── navigation.py      # Navigation system
│   ├── exploration.py     # Exploration mechanics
│   ├── combat.py          # Combat system
│   ├── diplomacy.py       # Diplomacy and communications
│   ├── missions.py        # Mission system
│   ├── away_team.py       # Away team missions
│   ├── crew.py            # ⭐ Officer class and crew definitions
│   └── crew_recruitment.py # ⭐ Crew recruitment system
├── saves/                 # Save game files
├── README.md              # This file
├── QUICKSTART.md          # Quick start guide
├── SHIP_SYSTEM.md         # Ship progression guide
├── MISSION_SYSTEM.md      # Mission system guide
├── CREW_SYSTEM.md         # ⭐ Crew officer system guide
└── INTEGRATION_SUMMARY.md # ⭐ Technical integration documentation
```

## Credits

Inspired by the Star Trek universe created by Gene Roddenberry.

This is a fan-made game and is not affiliated with or endorsed by CBS, Paramount, or any official Star Trek rights holders.

## License

This project is for educational and entertainment purposes only.

---

**Live Long and Prosper! 🖖**
