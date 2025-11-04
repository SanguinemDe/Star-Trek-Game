# Quick Start Guide - Star Trek Captain Simulator

## Installation Steps

### 1. Install Python
If you don't have Python installed:

**Option A: From Microsoft Store (Recommended for Windows)**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" or "Install"

**Option B: From Python.org**
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 or later
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation

### 2. Verify Installation
Open PowerShell or Command Prompt and type:
```powershell
python --version
```
You should see something like "Python 3.11.x" or "Python 3.12.x"

### 3. Run the Game
Navigate to the game directory and run:
```powershell
cd "e:\Star Trek Game"
python main.py
```

## First Time Playing

### Character Creation
1. Choose your captain's name
2. Select a species (each has different bonuses):
   - **Human** - Balanced, diplomatic
   - **Vulcan** - Science-focused, logical
   - **Andorian** - Combat-oriented, aggressive
   - **Tellarite** - Engineering expert
   - **Betazoid** - Diplomatic specialist
   - **Trill** - Versatile, experienced
   - **Bajoran** - Tactical and technical
   - **Klingon** - Warrior, combat expert

3. Choose your background:
   - **Command School** - Leadership focus
   - **Security/Tactical** - Combat focus
   - **Sciences Division** - Research focus
   - **Engineering Corps** - Technical focus
   - **Diplomatic Corps** - Negotiation focus

### Your First Mission

**Recommended First Steps:**
1. Check your ship status (Option 3) - Review your **Miranda-class** starting ship
2. View ship equipment (Option 4) - Understand your **Mk I** starting systems
3. Scan the Sol system (Option 2)
4. Visit Earth's space station to:
   - Get familiar with station services
   - Restock if needed
   - Check out the bar to boost crew morale
   - **NEW:** Visit the shipyard to upgrade equipment

5. Navigate to a nearby system (Option 1):
   - Try Vulcan (16 LY away)
   - Or Andoria (close by)
   - Or any Federation system

6. Practice exploration:
   - Scan new systems
   - Investigate anomalies
   - Conduct away team missions

7. **NEW - Combat Test Arena:**
   - Access from main menu or station menu
   - Practice combat with two Odyssey-class ships
   - Test weapon systems and tactics
   - No consequences - perfect for learning!

### Important Tips

**Ship Systems & Equipment (NEW!):**
- Your ship has modular equipment (weapons, shields, sensors, etc.)
- Equipment ranges from **Mk I** (basic) to **Mk XV** (elite)
- Higher marks provide better performance but cost more power
- Upgrade at station shipyards using reputation points
- Monitor your power budget - don't overload your reactor!
- Each ship has limited **upgrade space** for equipment

**Ship Progression:**
- Start with a **Miranda-class** cruiser (Rank 0)
- Earn **reputation points** through missions and combat
- Unlock better ships as you gain rank and reputation
- **64 Federation ships** available from Ranks 0-8:
  - Early: Miranda, Oberth, Saber
  - Mid: Excelsior, Intrepid, Defiant
  - Advanced: Sovereign, Luna, Akira
  - Elite: Odyssey, Vesta, Prometheus

**Resource Management:**
- Watch your **dilithium** levels (fuel for warp travel)
- Monitor **deuterium** for impulse engines
- Track **antimatter** for weapon systems
- Dock at starbases to refuel and repair
- Gather resources on away missions

**Crew Morale:**
- Keep morale above 70% for optimal performance
- Use shore leave at stations
- Conduct training exercises
- Avoid prolonged combat without rest

**Combat (ENHANCED!):**
- **Advanced shield system** with 4 facings (fore, aft, port, starboard)
- Distribute shield power strategically
- Target specific enemy shield facings
- Use **weapon arrays** and **torpedo bays** effectively
- Different firing arcs: forward, aft, broadside, turret
- Manage **power levels** between systems
- **Armor** provides protection when shields fail
- Scan enemies before engaging
- Retreat if overwhelmed

**Weapon Systems:**
- **Phaser Arrays**: Energy weapons in different firing arcs
- **Torpedo Bays**: Photon and Quantum torpedoes
- Higher mark weapons deal more damage
- Watch your weapon power allocation
- Some weapons have limited firing arcs

**Diplomacy:**
- Build good relations with factions
- Complete diplomatic missions
- Avoid Prime Directive violations
- Trade benefits both sides

**Exploration:**
- Scan every system you visit
- Deploy away teams on M-class planets
- Investigate anomalies for scientific data
- Document first contact encounters

### Game Controls

**Main Menu:**
All controls are menu-based. Simply:
1. Read the options
2. Type the number of your choice
3. Press Enter

**Ship Command Menu:**
1. Navigate to system
2. Scan system
3. Ship status (view stats and equipment)
4. View equipment (detailed equipment list)
5. Crew management
6. Station menu (when docked)
7. System map
8. Save game
9. Exit to main menu

**Station Services:**
- **Shipyard**: Upgrade equipment, requisition new ships
- **Medical**: Heal crew, boost morale
- **Supply Depot**: Refuel, restock supplies
- **Bar**: Shore leave, crew morale boost
- **Trade**: Buy/sell resources
- **Missions**: Accept new assignments

**Combat Test Arena (GUI):**
- **Mouse**: Click targets, select weapons
- **Keyboard**: Number keys for quick weapon selection
- **Spacebar**: Fire selected weapon
- **Shield controls**: Distribute power between facings

### Saving Your Game

**To Save:**
- Select option 8 from the ship command menu
- Your game is saved automatically to `saves/savegame.json`

**To Load:**
- Select "Load Game" from the main menu
- Your last save will be loaded

**Multiple Saves:**
- You can backup save files by copying `saves/savegame.json`
- Rename copies to keep multiple saves

### New Features & Systems

**Advanced Ship System:**
- Modular equipment with Mk I-XV progression
- 4-facing shield system (fore/aft/port/starboard)
- Dynamic power management
- Weapon arrays with firing arcs
- Torpedo bay systems
- Armor and hull integrity
- Turn speed and impulse speed mechanics

**Combat Test Arena:**
- Practice combat without consequences
- Two fully-equipped Odyssey-class ships
- Test all weapon systems and tactics
- Learn shield management
- Perfect for experimenting with strategies

**Equipment Upgrades:**
- Visit station shipyards to upgrade
- Spend reputation points on better equipment
- Mark system: Mk I (basic) → Mk XV (elite)
- Balance power usage vs performance
- Upgrade space limits total equipment

**64 Federation Ships:**
- Complete catalogue from Miranda to Odyssey
- Ships span Ranks 0-8
- Each ship has unique stats and capabilities
- Progression system based on rank and reputation
- Famous classes: Enterprise, Defiant, Voyager variants

### Troubleshooting

**Game won't start:**
- Make sure Python is installed
- Check you're in the correct directory
- Verify all game files are present

**Python not found:**
- Reinstall Python with "Add to PATH" checked
- Restart your terminal after installation

**Save file error:**
- The saves folder will be created automatically
- Make sure you have write permissions

**Combat Test Arena Issues:**
- If GUI doesn't open, check tkinter is installed
- On Linux: `sudo apt-get install python3-tk`
- On macOS: tkinter included with Python
- On Windows: tkinter included with Python

### Need Help?

Check the additional documentation:
- **README.md** - Complete game mechanics and features
- **COMBAT_TEST_ARENA_GUIDE.md** - Combat system tutorial
- **SHIP_EQUIPMENT_GUIDE.md** - Equipment and upgrade details
- **game/ships/federation.py** - All 64 Federation ship specs

## Keyboard Shortcuts

- **Ctrl+C** - Emergency exit (will lose unsaved progress)
- **Enter** - Confirm choice
- Numbers (1-9) - Select menu options

## Game Progression

**Ranks** (by experience):
- **Rank 0**: Lieutenant Commander (Start) - Miranda-class
- **Rank 1**: Commander (100 XP) - Oberth, Centaur unlocked
- **Rank 2**: Captain (300 XP) - Saber, Norway unlocked
- **Rank 3**: Fleet Captain (600 XP) - Excelsior, Intrepid unlocked
- **Rank 4**: Commodore (1000 XP) - Defiant, Akira unlocked
- **Rank 5**: Rear Admiral (1500 XP) - Sovereign, Luna unlocked
- **Rank 6**: Vice Admiral (2200 XP) - Prometheus, Vesta unlocked
- **Rank 7**: Admiral (3000 XP) - Odyssey variants unlocked
- **Rank 8**: Fleet Admiral (10000 XP) - Ultimate ships unlocked

**Reputation System (NEW!):**
- Earn reputation through missions and combat
- Spend reputation to:
  - Requisition better ships
  - Upgrade equipment at shipyards
  - Unlock special services
- Higher rank ships require more reputation
- Balance reputation spending between ships and upgrades

**Skills** (0-100):
- **Command** - Ship operations, crew management
- **Tactical** - Combat, weapons systems, targeting
- **Science** - Research, scanning, analysis
- **Engineering** - Repairs, system efficiency, power management
- **Diplomacy** - Negotiations, first contact

**Equipment Progression:**
- **Mk I**: Starting equipment (basic)
- **Mk II-IV**: Early upgrades (modest improvements)
- **Mk V-VIII**: Mid-tier upgrades (significant boost)
- **Mk IX-XII**: Advanced upgrades (powerful)
- **Mk XIII-XV**: Elite upgrades (maximum performance)

### Sample Play Session

**Basic Session:**
```
1. Start game, create character (Miranda-class ship)
2. Check ship status - review your Mk I equipment
3. Try Combat Test Arena to learn combat mechanics
4. Navigate to Vulcan (practice warp travel)
5. Scan Vulcan system
6. Visit space station, check services
7. Navigate to an unexplored system
8. Deploy away team to M-class planet
9. Investigate spatial anomaly
10. Return to Sol
11. Save game
```

**Advanced Session (After gaining rank/reputation):**
```
1. Load saved game
2. Visit station shipyard
3. Upgrade weapons to Mk III phasers
4. Upgrade shields to Mk III covariant shields
5. Check power levels (should still be balanced)
6. Accept combat mission
7. Use new equipment in battle
8. Practice shield facing management
9. Use torpedo bays strategically
10. Earn reputation from victory
11. Check ship requisition for better ships
12. Save progress
```

**Combat Practice Session:**
```
1. Access Combat Test Arena from main menu
2. Review Odyssey-class ship loadout
3. Practice targeting specific shield facings
4. Test different weapon arrays
5. Experiment with power distribution
6. Try quantum torpedoes
7. Learn shield management
8. Exit when comfortable (no progress lost)
```

---

## Quick Reference Card

**Starting Resources:**
- Ship: Miranda-class cruiser
- Equipment: All Mk I systems
- Crew: Full complement
- Supplies: Basic loadout

**Key Concepts:**
- **Reputation** = Currency for ships and upgrades
- **Rank** = Experience level (unlocks ships)
- **Mark (Mk)** = Equipment tier (I-XV)
- **Upgrade Space** = Limits total equipment
- **Power Budget** = Balance equipment power usage

**Ship Stats to Watch:**
- **Hull**: Structural integrity (0 = destroyed)
- **Shields**: Protection (4 facings)
- **Power**: Available vs. used
- **Crew**: Affects performance
- **Morale**: Affects efficiency

**Combat Priorities:**
1. Manage shield facings
2. Target enemy weak shields
3. Balance weapon fire
4. Monitor power levels
5. Repair critical systems

**Upgrade Priority (Beginner):**
1. Shields (survival)
2. Weapons (effectiveness)
3. Engines (mobility)
4. Sensors (detection)
5. Other systems (optional)

**Recommended Ship Path:**
1. Miranda (Rank 0) - Learn basics
2. Centaur or Saber (Ranks 1-2) - First upgrade
3. Excelsior or Intrepid (Ranks 3-4) - Iconic ships
4. Sovereign or Defiant (Rank 5) - Powerful options
5. Odyssey (Rank 7+) - Endgame flagship

---

**Ready to begin your journey?**

```powershell
python main.py
```

**For Combat Practice:**
```powershell
# From main menu, select Combat Test Arena
# Or access via station menu
```

**Live Long and Prosper! 🖖**

*Boldly go where no one has gone before...*
