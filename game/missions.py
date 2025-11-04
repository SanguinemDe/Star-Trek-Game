"""
Mission System
Players can accept missions at starbases to earn reputation, experience, and rewards
"""

import random

class Mission:
    """Represents a mission"""
    
    # Mission types with base rewards
    MISSION_TYPES = {
        'patrol': {
            'name': 'Patrol Sector',
            'description': 'Patrol the {location} sector and report any hostile activity.',
            'difficulty': 'Easy',
            'base_reputation': 15,
            'base_experience': 20,
            'required_skill': 'tactical',
            'required_level': 40,
            'time_days': 3
        },
        'escort': {
            'name': 'Escort Convoy',
            'description': 'Escort a civilian convoy through {location}.',
            'difficulty': 'Easy',
            'base_reputation': 20,
            'base_experience': 25,
            'required_skill': 'command',
            'required_level': 40,
            'time_days': 4
        },
        'survey': {
            'name': 'Scientific Survey',
            'description': 'Conduct a detailed survey of the {location} system.',
            'difficulty': 'Easy',
            'base_reputation': 25,
            'base_experience': 30,
            'required_skill': 'science',
            'required_level': 50,
            'time_days': 5
        },
        'rescue': {
            'name': 'Search and Rescue',
            'description': 'Locate and rescue missing vessel in {location}.',
            'difficulty': 'Medium',
            'base_reputation': 35,
            'base_experience': 40,
            'required_skill': 'command',
            'required_level': 50,
            'time_days': 4
        },
        'diplomatic': {
            'name': 'Diplomatic Mission',
            'description': 'Represent the Federation in negotiations at {location}.',
            'difficulty': 'Medium',
            'base_reputation': 40,
            'base_experience': 35,
            'required_skill': 'diplomacy',
            'required_level': 60,
            'time_days': 5
        },
        'investigate': {
            'name': 'Investigation',
            'description': 'Investigate reports of unusual activity in {location}.',
            'difficulty': 'Medium',
            'base_reputation': 30,
            'base_experience': 35,
            'required_skill': 'science',
            'required_level': 55,
            'time_days': 4
        },
        'combat': {
            'name': 'Combat Operation',
            'description': 'Engage hostile forces threatening {location}.',
            'difficulty': 'Hard',
            'base_reputation': 50,
            'base_experience': 60,
            'required_skill': 'tactical',
            'required_level': 65,
            'time_days': 3
        },
        'first_contact': {
            'name': 'First Contact Mission',
            'description': 'Make first contact with newly discovered species in {location}.',
            'difficulty': 'Hard',
            'base_reputation': 60,
            'base_experience': 55,
            'required_skill': 'diplomacy',
            'required_level': 70,
            'time_days': 6
        },
        'deep_space': {
            'name': 'Deep Space Exploration',
            'description': 'Explore uncharted regions beyond {location}.',
            'difficulty': 'Hard',
            'base_reputation': 55,
            'base_experience': 50,
            'required_skill': 'science',
            'required_level': 65,
            'time_days': 7
        },
        'border_defense': {
            'name': 'Border Defense',
            'description': 'Defend Federation border installations near {location}.',
            'difficulty': 'Very Hard',
            'base_reputation': 75,
            'base_experience': 80,
            'required_skill': 'tactical',
            'required_level': 75,
            'time_days': 5
        },
        'crisis_response': {
            'name': 'Crisis Response',
            'description': 'Respond to emergency situation at {location}.',
            'difficulty': 'Very Hard',
            'base_reputation': 80,
            'base_experience': 75,
            'required_skill': 'command',
            'required_level': 75,
            'time_days': 4
        },
        'temporal': {
            'name': 'Temporal Investigation',
            'description': 'Investigate temporal anomalies detected in {location}.',
            'difficulty': 'Extreme',
            'base_reputation': 100,
            'base_experience': 90,
            'required_skill': 'science',
            'required_level': 80,
            'time_days': 6
        }
    }
    
    def __init__(self, mission_type, location, mission_id):
        self.mission_id = mission_id
        self.mission_type = mission_type
        self.location = location
        
        template = self.MISSION_TYPES[mission_type]
        self.name = template['name']
        self.description = template['description'].format(location=location)
        self.difficulty = template['difficulty']
        self.reputation_reward = template['base_reputation']
        self.experience_reward = template['base_experience']
        self.required_skill = template['required_skill']
        self.required_level = template['required_level']
        self.time_days = template['time_days']
        
        # Additional rewards
        self.dilithium_reward = random.randint(50, 150)
        
        # Mission status
        self.accepted = False
        self.completed = False
        self.failed = False
        
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'mission_id': self.mission_id,
            'mission_type': self.mission_type,
            'location': self.location,
            'accepted': self.accepted,
            'completed': self.completed,
            'failed': self.failed
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        mission = cls(data['mission_type'], data['location'], data['mission_id'])
        mission.accepted = data['accepted']
        mission.completed = data['completed']
        mission.failed = data['failed']
        return mission


class MissionBoard:
    """Manages available missions"""
    
    def __init__(self):
        self.available_missions = []
        self.active_missions = []
        self.completed_missions = []
        self.mission_counter = 0
        
    def generate_missions(self, game_state, num_missions=5):
        """Generate new missions at a starbase"""
        self.available_missions = []
        
        # Get some nearby systems for mission locations
        current_system = game_state.galaxy.current_system
        nearby = game_state.galaxy.get_nearby_systems(current_system, 30)
        
        if not nearby:
            return
        
        # Generate mix of mission types based on player level
        player_rank = game_state.character.rank_level
        
        for _ in range(num_missions):
            self.mission_counter += 1
            
            # Select mission type based on difficulty progression
            available_types = []
            for mtype, template in Mission.MISSION_TYPES.items():
                # Only offer missions the player is qualified for (within reason)
                skill_value = game_state.character.attributes[template['required_skill']]
                if skill_value >= template['required_level'] - 20:  # Allow slightly challenging missions
                    available_types.append(mtype)
            
            if not available_types:
                available_types = ['patrol', 'escort', 'survey']  # Fallback easy missions
            
            mission_type = random.choice(available_types)
            
            # Select location from nearby systems
            location = random.choice(nearby)[0] if nearby else "Unknown Sector"
            
            mission = Mission(mission_type, location, self.mission_counter)
            self.available_missions.append(mission)
            
    def accept_mission(self, mission):
        """Accept a mission"""
        if mission in self.available_missions:
            mission.accepted = True
            self.available_missions.remove(mission)
            self.active_missions.append(mission)
            return True
        return False
        
    def complete_mission(self, mission, success=True):
        """Complete or fail a mission"""
        if mission in self.active_missions:
            self.active_missions.remove(mission)
            if success:
                mission.completed = True
                self.completed_missions.append(mission)
            else:
                mission.failed = True
            return True
        return False
        
    def get_active_missions(self):
        """Get list of active missions"""
        return self.active_missions
        
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'available_missions': [m.to_dict() for m in self.available_missions],
            'active_missions': [m.to_dict() for m in self.active_missions],
            'completed_missions': [m.to_dict() for m in self.completed_missions],
            'mission_counter': self.mission_counter
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        board = cls()
        board.available_missions = [Mission.from_dict(m) for m in data.get('available_missions', [])]
        board.active_missions = [Mission.from_dict(m) for m in data.get('active_missions', [])]
        board.completed_missions = [Mission.from_dict(m) for m in data.get('completed_missions', [])]
        board.mission_counter = data.get('mission_counter', 0)
        return board


def mission_board_menu(game_state, ui):
    """Display and handle mission board at starbase"""
    # Initialize mission board if not exists
    if not hasattr(game_state, 'mission_board'):
        game_state.mission_board = MissionBoard()
        
    # Generate missions if none available
    if not game_state.mission_board.available_missions:
        game_state.mission_board.generate_missions(game_state)
        
    while True:
        ui.display_header("STARFLEET MISSION BOARD")
        
        print("\n--- ACTIVE MISSIONS ---")
        active = game_state.mission_board.get_active_missions()
        if active:
            for i, mission in enumerate(active, 1):
                print(f"{i}. {mission.name} - {mission.location}")
                print(f"   Status: In Progress")
        else:
            print("No active missions")
            
        print("\n--- AVAILABLE MISSIONS ---")
        available = game_state.mission_board.available_missions
        if available:
            for i, mission in enumerate(available, 1):
                skill_name = mission.required_skill.title()
                skill_value = game_state.character.attributes[mission.required_skill]
                
                # Check if qualified
                if skill_value >= mission.required_level:
                    qualified = "✓"
                else:
                    qualified = f"✗ Need {skill_name} {mission.required_level}"
                
                print(f"\n{i}. {mission.name} [{mission.difficulty}] {qualified}")
                print(f"   {mission.description}")
                print(f"   Rewards: {mission.reputation_reward} Rep, {mission.experience_reward} XP, {mission.dilithium_reward} Dilithium")
                print(f"   Required: {skill_name} {mission.required_level} | Duration: {mission.time_days} days")
        else:
            print("No missions available. Check back later.")
            
        print(f"\n{len(available) + 1}. Accept Mission")
        print(f"{len(available) + 2}. Complete Active Mission")
        print(f"{len(available) + 3}. Refresh Mission Board")
        print(f"{len(available) + 4}. Return")
        
        try:
            choice = int(ui.get_input("\nSelect option: "))
            
            if choice == len(available) + 4:
                return
            elif choice == len(available) + 3:
                game_state.mission_board.generate_missions(game_state)
                ui.display_message("\n✓ Mission board refreshed!")
                input("\nPress Enter to continue...")
            elif choice == len(available) + 2:
                complete_mission_menu(game_state, ui)
            elif choice == len(available) + 1:
                accept_mission_menu(game_state, ui, available)
            else:
                ui.display_message("Invalid selection.")
                input("\nPress Enter to continue...")
        except ValueError:
            ui.display_message("Invalid input.")
            input("\nPress Enter to continue...")


def accept_mission_menu(game_state, ui, available):
    """Handle mission acceptance"""
    if not available:
        ui.display_message("\nNo missions available to accept.")
        input("\nPress Enter to continue...")
        return
        
    print("\n--- ACCEPT MISSION ---")
    for i, mission in enumerate(available, 1):
        print(f"{i}. {mission.name}")
    print(f"{len(available) + 1}. Cancel")
    
    try:
        choice = int(ui.get_input("\nSelect mission to accept: "))
        
        if choice == len(available) + 1:
            return
        elif 1 <= choice <= len(available):
            mission = available[choice - 1]
            
            # Check if qualified
            skill_value = game_state.character.attributes[mission.required_skill]
            if skill_value < mission.required_level:
                ui.display_message(f"\n✗ Insufficient {mission.required_skill.title()} skill!")
                ui.display_message(f"Required: {mission.required_level}, Your skill: {skill_value}")
                input("\nPress Enter to continue...")
                return
                
            # Check if player has too many active missions
            if len(game_state.mission_board.active_missions) >= 3:
                ui.display_message("\n✗ Maximum active missions reached (3/3)")
                ui.display_message("Complete some missions before accepting more.")
                input("\nPress Enter to continue...")
                return
                
            # Accept mission
            game_state.mission_board.accept_mission(mission)
            ui.display_message(f"\n✓ Mission accepted: {mission.name}")
            ui.display_message(f"You have {mission.time_days} days to complete this mission.")
            game_state.add_log_entry(f"Accepted mission: {mission.name} - {mission.location}")
            input("\nPress Enter to continue...")
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def complete_mission_menu(game_state, ui):
    """Handle mission completion"""
    active = game_state.mission_board.get_active_missions()
    
    if not active:
        ui.display_message("\nNo active missions to complete.")
        input("\nPress Enter to continue...")
        return
        
    print("\n--- COMPLETE MISSION ---")
    for i, mission in enumerate(active, 1):
        print(f"{i}. {mission.name} - {mission.location}")
    print(f"{len(active) + 1}. Cancel")
    
    try:
        choice = int(ui.get_input("\nSelect mission to complete: "))
        
        if choice == len(active) + 1:
            return
        elif 1 <= choice <= len(active):
            mission = active[choice - 1]
            attempt_mission_completion(game_state, ui, mission)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def attempt_mission_completion(game_state, ui, mission):
    """Attempt to complete a mission with skill check"""
    ui.display_header(f"MISSION: {mission.name}")
    
    print(f"\nLocation: {mission.location}")
    print(f"Difficulty: {mission.difficulty}")
    print(f"Required Skill: {mission.required_skill.title()}")
    
    skill_value = game_state.character.attributes[mission.required_skill]
    
    # Calculate success chance
    skill_diff = skill_value - mission.required_level
    base_chance = 0.7
    
    if skill_diff >= 20:
        success_chance = 0.95
    elif skill_diff >= 10:
        success_chance = 0.85
    elif skill_diff >= 0:
        success_chance = 0.75
    elif skill_diff >= -10:
        success_chance = 0.60
    else:
        success_chance = 0.40
        
    print(f"\nYour {mission.required_skill.title()} skill: {skill_value}")
    print(f"Success chance: {int(success_chance * 100)}%")
    
    if not ui.confirm("\nAttempt to complete mission?"):
        return
        
    # Time passes
    game_state.advance_time(mission.time_days)
    
    # Skill check
    if random.random() < success_chance:
        # Success!
        ui.display_message("\n" + "=" * 80)
        ui.display_message("✓ MISSION SUCCESSFUL")
        ui.display_message("=" * 80)
        
        # Awards
        game_state.character.gain_reputation(mission.reputation_reward)
        game_state.character.gain_experience(mission.experience_reward, mission.required_skill)
        game_state.ship.dilithium += mission.dilithium_reward
        
        ui.display_message(f"\nReputation gained: +{mission.reputation_reward}")
        ui.display_message(f"Experience gained: +{mission.experience_reward}")
        ui.display_message(f"Dilithium received: +{mission.dilithium_reward}")
        
        # Bonus for critical success
        if random.random() < 0.15:
            bonus_rep = mission.reputation_reward // 2
            game_state.character.gain_reputation(bonus_rep)
            ui.display_message(f"\n⭐ Outstanding performance! Bonus reputation: +{bonus_rep}")
            
        game_state.mission_board.complete_mission(mission, success=True)
        game_state.missions_completed += 1
        game_state.add_log_entry(f"Successfully completed mission: {mission.name}")
        
    else:
        # Failure
        ui.display_message("\n" + "=" * 80)
        ui.display_message("✗ MISSION FAILED")
        ui.display_message("=" * 80)
        ui.display_message("\nThe mission did not go as planned.")
        
        # Partial rewards
        partial_rep = mission.reputation_reward // 4
        partial_exp = mission.experience_reward // 3
        
        if partial_rep > 0:
            game_state.character.gain_reputation(partial_rep)
            ui.display_message(f"Partial reputation: +{partial_rep}")
        if partial_exp > 0:
            game_state.character.gain_experience(partial_exp, mission.required_skill)
            ui.display_message(f"Partial experience: +{partial_exp}")
            
        game_state.mission_board.complete_mission(mission, success=False)
        game_state.add_log_entry(f"Failed mission: {mission.name}")
        
    input("\nPress Enter to continue...")
