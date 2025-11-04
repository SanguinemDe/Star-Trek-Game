"""
Star Trek Game - Crew Recruitment System
Handles officer recruitment at starbases
"""

import random
from game.crew import Officer, OFFICER_RANKS, STATIONS, get_available_species


class RecruitmentPool:
    """Manages available officers for recruitment"""
    
    def __init__(self):
        self.available_officers = []
        self.last_refresh_stardate = 0
        
    def generate_pool(self, player_rank_level, current_stardate, max_officers=15):
        """Generate a pool of available officers for recruitment"""
        # Refresh pool if it's been a while or empty
        if not self.available_officers or (current_stardate - self.last_refresh_stardate) > 30:
            self.available_officers = []
            self.last_refresh_stardate = current_stardate
            
            # Generate officers of various ranks below player's rank
            for _ in range(max_officers):
                # Officers must be below player's rank
                max_officer_rank = max(0, player_rank_level - 1)
                
                # Weight towards lower ranks (more common)
                if max_officer_rank > 0:
                    weights = [10, 8, 6, 5, 4, 3, 2, 1, 1, 1][:max_officer_rank + 1]
                    officer_rank = random.choices(range(max_officer_rank + 1), weights=weights)[0]
                else:
                    officer_rank = 0
                
                # Random species
                species = random.choice(get_available_species())
                
                # Create officer without station assignment
                officer = Officer(species, officer_rank)
                self.available_officers.append(officer)
            
            # Sort by rank then by cost
            self.available_officers.sort(key=lambda x: (x.rank_level, x.reputation_cost))
    
    def remove_officer(self, officer):
        """Remove an officer from the pool after recruitment"""
        if officer in self.available_officers:
            self.available_officers.remove(officer)
    
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'officers': [officer.to_dict() for officer in self.available_officers],
            'last_refresh': self.last_refresh_stardate
        }
    
    @staticmethod
    def from_dict(data):
        """Load from dictionary"""
        pool = RecruitmentPool()
        pool.available_officers = [Officer.from_dict(o) for o in data.get('officers', [])]
        pool.last_refresh_stardate = data.get('last_refresh', 0)
        return pool


def crew_recruitment_menu(game_state, ui):
    """Main crew recruitment interface"""
    # Initialize recruitment pool if it doesn't exist
    if not hasattr(game_state, 'recruitment_pool'):
        game_state.recruitment_pool = RecruitmentPool()
    
    while True:
        # Generate/refresh pool
        game_state.recruitment_pool.generate_pool(
            game_state.character.rank_level,
            game_state.stardate
        )
        
        ui.display_header("CREW RECRUITMENT")
        
        print(f"\nYour Rank: {game_state.character.rank}")
        print(f"Reputation: {game_state.character.reputation}")
        print(f"\nAvailable Officers: {len(game_state.recruitment_pool.available_officers)}")
        
        # Show current crew roster
        print("\n--- CURRENT BRIDGE CREW ---")
        if hasattr(game_state.ship, 'crew_roster') and game_state.ship.crew_roster:
            for station, officer in game_state.ship.crew_roster.items():
                bonus = officer.get_station_bonus()
                print(f"{STATIONS[station]['name']:25s}: {officer.rank:15s} {officer.name:20s} (Bonus: +{bonus:.1f}%)")
        else:
            print("No officers assigned to bridge stations.")
        
        print("\n1. View Available Officers")
        print("2. Manage Current Crew")
        print("3. Station Information")
        print("4. Return to Station")
        
        try:
            choice = int(ui.get_input("\nSelect option: "))
            
            if choice == 1:
                view_and_recruit_officers(game_state, ui)
            elif choice == 2:
                manage_crew(game_state, ui)
            elif choice == 3:
                show_station_info(ui)
            elif choice == 4:
                return
            else:
                ui.display_message("Invalid selection.")
                input("\nPress Enter to continue...")
        except ValueError:
            ui.display_message("Invalid input.")
            input("\nPress Enter to continue...")


def view_and_recruit_officers(game_state, ui):
    """View available officers and recruit"""
    pool = game_state.recruitment_pool
    
    if not pool.available_officers:
        ui.display_message("\nNo officers currently available for recruitment.")
        input("\nPress Enter to continue...")
        return
    
    ui.display_header("AVAILABLE OFFICERS")
    
    print(f"\nYour Reputation: {game_state.character.reputation}")
    print(f"Your Rank: {game_state.character.rank} (Level {game_state.character.rank_level})")
    
    print("\n" + "=" * 100)
    print(f"{'#':<3} {'Rank':<15} {'Name':<20} {'Species':<12} {'Cost':<7} {'CMD':<4} {'TAC':<4} {'SCI':<4} {'ENG':<4} {'DIP':<4}")
    print("=" * 100)
    
    for idx, officer in enumerate(pool.available_officers, 1):
        can_afford = game_state.character.reputation >= officer.reputation_cost
        status = "✓" if can_afford else "✗"
        
        print(f"{idx:<3} {officer.rank:<15} {officer.name:<20} {officer.species:<12} " 
              f"{officer.reputation_cost:<7} "
              f"{officer.skills['command']:<4} {officer.skills['tactical']:<4} "
              f"{officer.skills['science']:<4} {officer.skills['engineering']:<4} "
              f"{officer.skills['diplomacy']:<4} {status}")
    
    print("\n0. Return to menu")
    
    try:
        choice = int(ui.get_input("\nSelect officer to recruit (or 0 to cancel): "))
        
        if choice == 0:
            return
        elif 1 <= choice <= len(pool.available_officers):
            officer = pool.available_officers[choice - 1]
            recruit_officer(game_state, ui, officer)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def recruit_officer(game_state, ui, officer):
    """Recruit a specific officer"""
    ui.display_header(f"RECRUIT: {officer.rank} {officer.name}")
    
    print(f"\nOfficer: {officer.rank} {officer.name}")
    print(f"Species: {officer.species}")
    print(f"\n--- SKILLS ---")
    print(f"Command:     {officer.skills['command']}")
    print(f"Tactical:    {officer.skills['tactical']}")
    print(f"Science:     {officer.skills['science']}")
    print(f"Engineering: {officer.skills['engineering']}")
    print(f"Diplomacy:   {officer.skills['diplomacy']}")
    
    print(f"\nRecruitment Cost: {officer.reputation_cost} Reputation")
    print(f"Your Reputation: {game_state.character.reputation}")
    
    if game_state.character.reputation < officer.reputation_cost:
        ui.display_message("\n✗ Insufficient reputation to recruit this officer.")
        input("\nPress Enter to continue...")
        return
    
    # Select station assignment
    print("\n--- ASSIGN TO STATION ---")
    stations = list(STATIONS.keys())
    for idx, station in enumerate(stations, 1):
        station_info = STATIONS[station]
        current = game_state.ship.crew_roster.get(station) if hasattr(game_state.ship, 'crew_roster') else None
        current_text = f" (Current: {current.name})" if current else " (Empty)"
        print(f"{idx}. {station_info['name']}{current_text}")
    
    print(f"{len(stations) + 1}. Do not recruit")
    
    try:
        station_choice = int(ui.get_input("\nAssign to station: "))
        
        if station_choice == len(stations) + 1:
            return
        elif 1 <= station_choice <= len(stations):
            station = stations[station_choice - 1]
            
            # Initialize crew roster if needed
            if not hasattr(game_state.ship, 'crew_roster'):
                game_state.ship.crew_roster = {}
            
            # Check if station is occupied
            if station in game_state.ship.crew_roster:
                current_officer = game_state.ship.crew_roster[station]
                print(f"\nStation currently occupied by {current_officer.rank} {current_officer.name}")
                if not ui.confirm("Replace current officer?"):
                    return
                # Current officer goes back to pool (dismissed)
                ui.display_message(f"\n{current_officer.name} has been dismissed from duty.")
            
            # Confirm recruitment
            if ui.confirm(f"\nRecruit {officer.name} as {STATIONS[station]['name']}?"):
                # Deduct reputation
                game_state.character.reputation -= officer.reputation_cost
                
                # Assign station
                officer.station = station
                game_state.ship.crew_roster[station] = officer
                
                # Remove from pool
                game_state.recruitment_pool.remove_officer(officer)
                
                ui.display_message(f"\n✓ Successfully recruited {officer.rank} {officer.name}!")
                ui.display_message(f"Assigned to: {STATIONS[station]['name']}")
                ui.display_message(f"Station Bonus: +{officer.get_station_bonus():.1f}%")
                
                game_state.add_log_entry(f"Recruited {officer.rank} {officer.name} as {STATIONS[station]['name']}.")
                
                input("\nPress Enter to continue...")
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def manage_crew(game_state, ui):
    """Manage current crew - reassign or dismiss officers"""
    if not hasattr(game_state.ship, 'crew_roster') or not game_state.ship.crew_roster:
        ui.display_message("\nNo crew officers currently assigned.")
        input("\nPress Enter to continue...")
        return
    
    ui.display_header("MANAGE CREW")
    
    officers_list = list(game_state.ship.crew_roster.items())
    
    for idx, (station, officer) in enumerate(officers_list, 1):
        station_info = STATIONS[station]
        bonus = officer.get_station_bonus()
        print(f"\n{idx}. {station_info['name']}")
        print(f"   {officer.rank} {officer.name} ({officer.species})")
        print(f"   Primary Skill ({station_info['primary_skill'].title()}): {officer.skills[station_info['primary_skill']]}")
        print(f"   Station Bonus: +{bonus:.1f}%")
    
    print("\n0. Return")
    
    try:
        choice = int(ui.get_input("\nSelect officer to manage: "))
        
        if choice == 0:
            return
        elif 1 <= choice <= len(officers_list):
            station, officer = officers_list[choice - 1]
            manage_single_officer(game_state, ui, station, officer)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def manage_single_officer(game_state, ui, station, officer):
    """Manage a single officer - view details, reassign, or dismiss"""
    ui.display_header(f"{officer.rank} {officer.name}")
    
    print(f"\nSpecies: {officer.species}")
    print(f"Current Station: {STATIONS[station]['name']}")
    print(f"Station Bonus: +{officer.get_station_bonus():.1f}%")
    
    print(f"\n--- SKILLS ---")
    for skill, value in officer.skills.items():
        primary = " (PRIMARY)" if skill == STATIONS[station]['primary_skill'] else ""
        print(f"{skill.title():12s}: {value}{primary}")
    
    print("\n1. Reassign to Different Station")
    print("2. Dismiss Officer")
    print("3. Return")
    
    try:
        choice = int(ui.get_input("\nSelect option: "))
        
        if choice == 1:
            reassign_officer(game_state, ui, station, officer)
        elif choice == 2:
            if ui.confirm(f"\nDismiss {officer.name} from duty?"):
                del game_state.ship.crew_roster[station]
                ui.display_message(f"\n{officer.name} has been dismissed.")
                game_state.add_log_entry(f"Dismissed {officer.rank} {officer.name}.")
                input("\nPress Enter to continue...")
        elif choice == 3:
            return
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def reassign_officer(game_state, ui, current_station, officer):
    """Reassign an officer to a different station"""
    ui.display_header(f"REASSIGN: {officer.name}")
    
    print(f"\nCurrent Assignment: {STATIONS[current_station]['name']}")
    print("\n--- AVAILABLE STATIONS ---")
    
    stations = list(STATIONS.keys())
    for idx, station in enumerate(stations, 1):
        if station == current_station:
            print(f"{idx}. {STATIONS[station]['name']} (CURRENT)")
        else:
            current_officer = game_state.ship.crew_roster.get(station)
            if current_officer:
                print(f"{idx}. {STATIONS[station]['name']} (Occupied by {current_officer.name})")
            else:
                print(f"{idx}. {STATIONS[station]['name']} (Empty)")
    
    print(f"{len(stations) + 1}. Cancel")
    
    try:
        choice = int(ui.get_input("\nSelect new station: "))
        
        if choice == len(stations) + 1:
            return
        elif 1 <= choice <= len(stations):
            new_station = stations[choice - 1]
            
            if new_station == current_station:
                ui.display_message("\nOfficer is already assigned to this station.")
                input("\nPress Enter to continue...")
                return
            
            # Check if new station is occupied
            if new_station in game_state.ship.crew_roster:
                other_officer = game_state.ship.crew_roster[new_station]
                if ui.confirm(f"\nSwap positions with {other_officer.name}?"):
                    # Swap officers
                    game_state.ship.crew_roster[current_station] = other_officer
                    other_officer.station = current_station
                    game_state.ship.crew_roster[new_station] = officer
                    officer.station = new_station
                    
                    ui.display_message(f"\n✓ Officers successfully reassigned!")
                    game_state.add_log_entry(f"Reassigned {officer.name} to {STATIONS[new_station]['name']}.")
            else:
                # Move to empty station
                del game_state.ship.crew_roster[current_station]
                game_state.ship.crew_roster[new_station] = officer
                officer.station = new_station
                
                ui.display_message(f"\n✓ {officer.name} reassigned to {STATIONS[new_station]['name']}!")
                game_state.add_log_entry(f"Reassigned {officer.name} to {STATIONS[new_station]['name']}.")
            
            input("\nPress Enter to continue...")
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def show_station_info(ui):
    """Display information about all stations and their effects"""
    ui.display_header("STATION INFORMATION")
    
    for station, info in STATIONS.items():
        print(f"\n--- {info['name'].upper()} ---")
        print(f"Primary Skill: {info['primary_skill'].title()}")
        print(f"Description: {info['description']}")
        print("\nEffects:")
        for effect_name, effect_desc in info['effects'].items():
            print(f"  • {effect_name.replace('_', ' ').title()}: {effect_desc}")
    
    input("\nPress Enter to continue...")
