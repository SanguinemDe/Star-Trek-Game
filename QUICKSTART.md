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
1. Check your ship status (Option 3)
2. Scan the Sol system (Option 2)
3. Visit Earth's space station to:
   - Get familiar with station services
   - Restock if needed
   - Check out the bar to boost crew morale

4. Navigate to a nearby system (Option 1):
   - Try Vulcan (16 LY away)
   - Or Andoria (close by)
   - Or any Federation system

5. Practice exploration:
   - Scan new systems
   - Investigate anomalies
   - Conduct away team missions

### Important Tips

**Resource Management:**
- Watch your dilithium levels (fuel for warp travel)
- Dock at starbases to refuel and repair
- Gather resources on away missions

**Crew Morale:**
- Keep morale above 70% for optimal performance
- Use shore leave at stations
- Conduct training exercises
- Avoid prolonged combat without rest

**Combat:**
- Scan enemies before engaging
- Use diplomacy when possible
- Manage shields and weapons
- Retreat if overwhelmed

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

All controls are menu-based. Simply:
1. Read the options
2. Type the number of your choice
3. Press Enter

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

### Need Help?

Check the README.md file for:
- Detailed gameplay mechanics
- Ship class information
- Species bonuses
- Faction details
- Advanced strategies

## Keyboard Shortcuts

- **Ctrl+C** - Emergency exit (will lose unsaved progress)
- **Enter** - Confirm choice
- Numbers (1-9) - Select menu options

## Game Progression

**Ranks** (by experience):
- Lieutenant Commander (Start)
- Commander (100 XP)
- Captain (300 XP)
- Fleet Captain (600 XP)
- Commodore (1000 XP)
- Rear Admiral (1500 XP)
- Vice Admiral (2200 XP)
- Admiral (3000 XP)
- Fleet Admiral (10000 XP)

**Skills** (0-100):
- **Command** - Ship operations, crew management
- **Tactical** - Combat, weapons systems
- **Science** - Research, scanning, analysis
- **Engineering** - Repairs, system efficiency
- **Diplomacy** - Negotiations, first contact

### Sample Play Session

```
1. Start game, create character
2. Navigate to Vulcan (practice warp travel)
3. Scan Vulcan system
4. Visit space station, check services
5. Navigate to an unexplored system
6. Deploy away team to M-class planet
7. Investigate spatial anomaly
8. Return to Sol
9. Save game
```

---

**Ready to begin your journey?**

```powershell
python main.py
```

**Live Long and Prosper! 🖖**
