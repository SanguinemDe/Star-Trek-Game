# Star Trek: Captain's Career Simulator - Changelog

## Version 0.2.0 - Ship Requisition Update (November 2, 2025)

### Major New Features

#### Ship Requisition System
- ✅ **24 Canonical Federation Ships** - Expanded from 7 to 24 playable starships
- ✅ **Reputation System** - Earn reputation points through gameplay
- ✅ **Progressive Unlocks** - Ships require both rank and reputation to purchase
- ✅ **Universal Miranda Start** - All captains now begin with Miranda-class
- ✅ **Ship Purchase Interface** - New menu system for browsing and buying ships

#### New Ships Added
**Tier 1 (Starting):**
- Oberth-class Science Vessel

**Tier 2 (Early Career):**
- Constitution Refit
- Saber-class Light Escort

**Tier 3 (Mid-Level):**
- Ambassador-class Heavy Cruiser
- Steamrunner-class Frigate
- Norway-class Frigate

**Tier 4 (Advanced):**
- Nebula-class Science Cruiser
- Akira-class Heavy Cruiser

**Tier 5 (Elite):**
- Prometheus-class Advanced Escort
- Luna-class Deep Space Science Vessel
- Vesta-class Multi-Mission Explorer

**Tier 6 (Command):**
- Odyssey-class Star Cruiser
- Venture-class Galaxy Dreadnought
- Excelsior Refit

**Tier 7 (Ultimate):**
- Universe-class Temporal Dreadnought
- Yorktown-class Science Star Cruiser
- Enterprise-J Universe-class Dreadnought

#### Reputation Earning System
- ✅ Exploration: +5 Rep per new system, +10 for canonical systems
- ✅ Combat: +5 to +50 Rep based on enemy difficulty
- ✅ Diplomacy: +10 to +50 Rep for diplomatic successes
- ✅ First Contact: +30 Rep for successful missions
- ✅ Experience Bonus: Gain 50% of XP as Reputation

#### Ship Details
- ✅ Each ship has unique stats, era, and description
- ✅ Detailed specifications display in requisition menu
- ✅ Ship comparison before purchase
- ✅ Custom ship naming system
- ✅ Resource and crew transfer on ship change

### Enhancements
- ✅ Updated UI to show reputation points
- ✅ New ship command menu option (#7 - Ship Requisition)
- ✅ Reputation bonuses integrated across all game systems
- ✅ Ship progression documentation (SHIP_SYSTEM.md)

### Balance Changes
- ✅ All species now start with Miranda-class (was varied)
- ✅ Combat victories now grant reputation
- ✅ Diplomatic resolutions grant significant reputation
- ✅ Exploration rewards reputation for discoveries

### Documentation
- ✅ New SHIP_SYSTEM.md guide with complete ship roster
- ✅ Updated README.md with ship system information
- ✅ Updated QUICKSTART.md for new features

---

## Version 0.1.0 - Initial Release (November 2, 2025)

### Core Features Implemented

#### Character System
- ✅ Character creation with 8 species options
- ✅ 5 background specializations
- ✅ 5 core attributes (Command, Tactical, Science, Engineering, Diplomacy)
- ✅ 12 rank progression levels
- ✅ Experience and skill leveling system
- ✅ Commendations and traits system

#### Ship Management
- ✅ 7 ship classes (Miranda, Constitution, Excelsior, Intrepid, Defiant, Galaxy, Sovereign)
- ✅ Hull integrity and shield systems
- ✅ 6 ship subsystems (weapons, shields, sensors, engines, life support, transporter)
- ✅ Damage and repair mechanics
- ✅ Dilithium fuel management
- ✅ Crew capacity and morale system
- ✅ Provisions and resource tracking

#### Galaxy & Exploration
- ✅ Procedurally generated galaxy (150-250 star systems)
- ✅ 13 canonical Star Trek systems (Sol, Vulcan, Qo'noS, Romulus, etc.)
- ✅ Star type classification (M, K, G, F, A, B, O)
- ✅ Planetary system generation (0-12 planets per system)
- ✅ Planet types (M-Class, Gas Giant, Ice, Desert, Volcanic, Ocean, Barren, Toxic)
- ✅ Space stations and anomalies
- ✅ Inhabited worlds with civilization levels
- ✅ Resource detection (Dilithium, Rare Minerals)

#### Navigation System
- ✅ Warp drive travel between systems
- ✅ Distance calculation and travel time
- ✅ Fuel consumption based on distance
- ✅ Random encounters during travel
- ✅ System discovery and exploration tracking

#### Combat System
- ✅ Tactical space combat
- ✅ 5 enemy ship classes (Scout, Frigate, Cruiser, Battleship, Dreadnought)
- ✅ Multiple combat actions (phasers, torpedoes, evasive maneuvers)
- ✅ Shield management and hull damage
- ✅ Combat diplomacy options
- ✅ Retreat mechanics
- ✅ Ship destruction and game over conditions

#### Diplomacy System
- ✅ 7 major faction relationships
- ✅ Relation status tracking (-100 to +100)
- ✅ Diplomatic communications
- ✅ Trade agreements
- ✅ Alliance negotiations
- ✅ Faction-based encounters
- ✅ Incoming transmission system

#### Away Team Missions
- ✅ Planetary landing capabilities
- ✅ 4 mission types (exploration, resource gathering, first contact, rescue)
- ✅ Prime Directive considerations
- ✅ Random encounter events
- ✅ Resource collection from planets
- ✅ Scientific discoveries
- ✅ Crew safety mechanics

#### Crew Management
- ✅ Crew complement tracking
- ✅ Crew morale system (0-100%)
- ✅ Key personnel roster (6 positions)
- ✅ Officer generation with skills
- ✅ Crew training programs
- ✅ Shore leave system
- ✅ Crew status reports

#### User Interface
- ✅ ASCII art title screen
- ✅ Menu-based navigation
- ✅ Status displays with progress bars
- ✅ Detailed ship information screens
- ✅ System scan displays
- ✅ Combat interface
- ✅ Diplomatic interface
- ✅ Captain's log viewer

#### Game State & Persistence
- ✅ Save game functionality
- ✅ Load game functionality
- ✅ JSON-based save format
- ✅ Captain's log with stardate tracking
- ✅ Statistics tracking (missions, enemies, systems explored)
- ✅ Turn-based time progression
- ✅ Stardate system

### Known Limitations (To Be Addressed in Future Versions)
- Single save slot (manual backup required for multiple saves)
- Text-only interface (no graphics)
- No sound effects or music
- Limited ship customization
- Basic AI for combat encounters
- No multiplayer features
- Limited story missions (mostly procedural)

### Technical Specifications
- Language: Python 3.7+
- Dependencies: None (Python standard library only)
- Platform: Cross-platform (Windows, macOS, Linux)
- Save Format: JSON
- File Structure: Modular design with 11 game modules

---

## Planned Features for Future Versions

### Version 0.2.0 (Planned)
- Multiple save slots
- Enhanced combat AI
- More ship customization options
- Additional random events
- Expanded crew interactions
- More mission types
- Trade and economy system
- Ship upgrades and modifications

### Version 0.3.0 (Planned)
- Story missions and campaign
- More alien species encounters
- Borg encounters and mechanics
- Temporal anomalies
- Fleet command (multiple ships)
- Advanced diplomacy trees
- Reputation system

### Version 1.0.0 (Future)
- GUI interface option
- Sound effects and music
- Enhanced graphics (ASCII art)
- Steam/itch.io release
- Achievement system
- Modding support
- Multiplayer elements

---

## Bug Reports and Feedback

If you encounter any issues or have suggestions:
1. Check the README.md for gameplay tips
2. Verify your Python version (3.7+)
3. Ensure all game files are present
4. Try starting a new game if saves are corrupted

---

**Current Version: 0.1.0**
**Release Date: November 2, 2025**
**Status: Initial Release - Fully Playable**

🖖 Live Long and Prosper!
