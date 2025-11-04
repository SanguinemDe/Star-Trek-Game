# Mission System & Caitian Race - Update Summary

## Version 0.2.0 - Mission System Release

### New Features

#### 1. Mission System
A comprehensive mission system has been added, allowing players to accept and complete missions at starbases throughout the galaxy.

**Mission Types (12 Total)**:
- Patrol Sector (Easy)
- Escort Convoy (Easy)
- Scientific Survey (Easy)
- Search and Rescue (Medium)
- Diplomatic Mission (Medium)
- Investigation (Medium)
- Combat Operation (Hard)
- First Contact Mission (Hard)
- Deep Space Exploration (Hard)
- Border Defense (Very Hard)
- Crisis Response (Very Hard)
- Temporal Investigation (Extreme)

**Mission Rewards**:
- Reputation: 15-100 per mission
- Experience: 20-90 per mission
- Dilithium: 50-150 per mission
- 15% chance for critical success with bonus reputation

**Mission Mechanics**:
- Accept up to 3 active missions at once
- Skill-based success chances (40%-95%)
- Mission duration: 3-7 days
- Partial rewards for failed missions
- Refresh mission board for new options

#### 2. New Playable Species: Caitian
Added the Caitian species to character creation!

**Caitian Bonuses**:
- Tactical: +10 (excellent combat abilities)
- Science: +5 (curious explorers)

**Background**:
Caitians are a feline humanoid species known for their agility, keen senses, and warrior traditions. They make excellent tactical officers and security personnel.

### Files Modified

#### game/missions.py (NEW)
- Complete mission system implementation
- Mission class with 12 mission types
- MissionBoard class for mission management
- Success/failure mechanics with skill checks
- Mission acceptance, completion, and tracking
- Integration functions for UI

#### game/character.py
- Added Caitian to SPECIES dictionary
- Caitian bonuses: tactical +10, science +5

#### game/exploration.py
- Added "Mission Board" option to station docking
- Integrated mission_board_menu function
- Renumbered station service options

#### game/game_state.py
- Added mission_board saving to save_game()
- Added mission_board loading to load_game()
- Persistence support for mission data

#### game/ui.py
- Added active mission count to status display
- Shows "Active Missions: X/3" in status bar

#### README.md
- Updated core gameplay features
- Added Caitian to species bonuses
- Updated reputation earning methods (missions primary)
- Enhanced gameplay tips with mission strategies
- Updated project structure
- Added MISSION_SYSTEM.md reference

#### MISSION_SYSTEM.md (NEW)
- Complete mission system documentation
- All 12 mission types detailed
- Success mechanics explained
- Strategy guide for all career levels
- Quick reference tables
- Troubleshooting section

### How to Use

#### Accessing Missions
1. Navigate to any system with a station/starbase
2. Select "Explore System" from main menu
3. Choose "Dock at Station"
4. Select "1. Mission Board"

#### Mission Board Options
- View active missions (current progress)
- View available missions (new missions to accept)
- Accept mission (up to 3 at once)
- Complete active mission (attempt with skill check)
- Refresh mission board (generate new missions)
- Return to station services

#### Completing Missions
1. Have an active mission
2. Return to any station
3. Select "Complete Active Mission"
4. Choose which mission to attempt
5. Success determined by skill check
6. Receive rewards (or partial rewards if failed)

### Reputation Earning Strategy

**Before Mission System**:
- Primary: Combat victories (+5-50)
- Secondary: Exploration, diplomacy
- Slow progression to higher-tier ships

**With Mission System**:
- Primary: Missions (+15-100 per mission)
- Secondary: Combat, exploration, diplomacy
- Faster, more predictable progression
- Can stack 3 missions for efficient reputation farming

**Example Progression**:
- Miranda → Constellation (500 rep): ~15-20 missions
- Constellation → Galaxy (2000 rep): ~30-40 missions total
- Galaxy → Sovereign (3500 rep): ~50-60 missions total

### Mission Difficulty Progression

**Starting Out (Lieutenant Commander, Miranda-class)**:
- Focus on Easy missions (Patrol, Escort, Survey)
- Skills around 40-50
- Earn 15-25 reputation per mission
- Build skills through mission experience

**Mid-Career (Commander/Captain, Constellation-Excelsior)**:
- Progress to Medium missions (Rescue, Investigation)
- Skills around 50-60
- Earn 30-40 reputation per mission
- Diversify skill development

**Advanced (Captain/Admiral, Galaxy-Sovereign)**:
- Take Hard missions (Combat, First Contact, Exploration)
- Skills around 65-70
- Earn 50-60 reputation per mission
- Focus on high-reputation rewards

**Elite (Admiral+, Odyssey and beyond)**:
- Very Hard and Extreme missions
- Skills 75-80+
- Earn 75-100 reputation per mission
- Master-level challenges

### Integration with Existing Systems

**Ship Requisition**:
- Missions are now the primary way to earn reputation
- More consistent than relying on random encounters
- Plan mission runs to save for specific ships
- See SHIP_SYSTEM.md for ship requirements

**Character Progression**:
- Mission experience increases skills
- Higher skills improve mission success rates
- Skill specialization matters (match missions to strengths)
- Rank unlocks are unchanged (still through experience)

**Exploration**:
- Missions complement exploration gameplay
- Some missions send you to specific systems
- Discovery bonuses stack with mission rewards
- First contact can earn both mission and exploration rep

**Combat**:
- Combat missions test tactical skills
- Some missions may trigger combat encounters
- Combat reputation rewards still apply
- Ship capabilities affect mission success

**Diplomacy**:
- Diplomatic missions require high diplomacy skill
- Good faction relations help mission generation
- Diplomatic victories can be missions
- Federation standing improves with completed missions

### Technical Details

**Save Compatibility**:
- Mission data automatically saved with game state
- Backward compatible with old saves (no missions)
- Mission board initialized on first station visit
- No data loss when loading old saves

**Mission Generation**:
- 5 missions generated per refresh
- Based on player skill levels
- Uses nearby systems for mission locations
- Difficulty scales with character progression

**Skill Checks**:
- Each mission requires specific skill
- Success chance: 40% (under-skilled) to 95% (over-skilled)
- Critical success: 15% chance for 50% bonus reputation
- Partial rewards on failure (25% rep, 33% exp)

**Mission Tracking**:
- Mission counter tracks all generated missions
- Active missions limited to 3
- Completed missions logged in captain's log
- Statistics tracked (missions_completed counter)

### Testing Recommendations

1. **Start New Game**:
   - Create Caitian character to test new species
   - Should see tactical +10, science +5 bonuses
   - Character creation should list 9 species total

2. **Mission System Basic**:
   - Travel to Sol or another system with station
   - Dock at station
   - Access mission board (option 1)
   - Should see 5 available missions

3. **Mission Acceptance**:
   - Accept a mission matching your skills
   - Should appear in "Active Missions" section
   - Status display should show "Active Missions: 1/3"
   - Try accepting 3 missions (hit limit)

4. **Mission Completion**:
   - Attempt to complete an active mission
   - Should see skill check and success percentage
   - Receive reputation and experience rewards
   - Mission should move to completed list

5. **Save/Load**:
   - Accept some missions
   - Save game
   - Load game
   - Active missions should persist

6. **Mission Refresh**:
   - Use "Refresh Mission Board"
   - Should generate 5 new missions
   - Old unaccepted missions are replaced

### Known Limitations

**Mission Locations**:
- Mission locations are descriptive only
- No requirement to physically travel there
- Future enhancement: require visiting mission system
- Current system focuses on skill checks

**Mission Variety**:
- 12 mission types with fixed templates
- Location names vary but missions are procedural
- Future: Story missions, chain missions, unique missions
- Current: Repeatable missions for reputation farming

**Enemy Encounters**:
- Missions don't currently trigger specific encounters
- Future: Mission-specific combat/events
- Current: Skill checks abstract mission outcomes

**Time Passage**:
- Mission time (3-7 days) passes instantly
- No real-time waiting required
- Stardate advances by mission duration
- Player must return to station to complete

### Future Enhancements

**Planned Features**:
- Story-driven mission chains
- Unique missions with special rewards
- Specific mission locations requiring travel
- Mission failures affect faction relations
- Time limits on missions
- Mission-specific encounters and events
- Daily/weekly mission resets
- Mission difficulty settings
- Co-op mission support (future multiplayer)

**Balancing**:
- May adjust reputation rewards based on testing
- Success chance formula may be tuned
- Mission type distribution may change
- Critical success rate may be adjusted

### Changelog Entry

**v0.2.0 - Mission System & Caitian Race**
- Added comprehensive mission system with 12 mission types
- Added Caitian playable species (+10 tactical, +5 science)
- Missions available at all starbases and stations
- Reputation farming now structured and predictable
- Mission rewards: 15-100 rep, 20-90 XP, 50-150 dilithium
- Up to 3 active missions at once
- Skill-based success chances (40-95%)
- Critical success bonuses (15% chance for +50% rep)
- Mission board with refresh functionality
- Active mission tracking in status display
- Mission persistence in save/load system
- Complete documentation in MISSION_SYSTEM.md
- Updated README with mission strategies
- Enhanced character creation with 9th species option

### Documentation Files

**New Files**:
- `MISSION_SYSTEM.md` - Complete mission guide
- `MISSION_UPDATE.md` - This file

**Updated Files**:
- `README.md` - Mission system features, Caitian species
- `SHIP_SYSTEM.md` - No changes (still valid)
- `QUICKSTART.md` - May need mission section (future)
- `CHANGELOG.md` - Needs v0.2.0 entry (future)

### Special Thanks

The mission system draws inspiration from:
- Star Trek Online's duty officer missions
- Star Trek: Bridge Commander's campaign missions
- Classic Star Trek episodes featuring Starfleet orders
- The Caitian species featured in Star Trek: The Animated Series and Lower Decks

---

**Live long and prosper! 🖖**

*This update brings structured progression and the agile Caitians to your Star Trek adventure!*
