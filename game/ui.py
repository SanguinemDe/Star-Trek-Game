"""
User Interface System
"""

import os

class UI:
    """Handles all user interface and display"""
    
    def __init__(self):
        self.width = 80
        
    def display_title(self):
        """Display the game title"""
        title = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║    ███████╗████████╗ █████╗ ██████╗     ████████╗██████╗ ███████╗██╗  ██╗║
║    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝║
║    ███████╗   ██║   ███████║██████╔╝       ██║   ██████╔╝█████╗  █████╔╝ ║
║    ╚════██║   ██║   ██╔══██║██╔══██╗       ██║   ██╔══██╗██╔══╝  ██╔═██╗ ║
║    ███████║   ██║   ██║  ██║██║  ██║       ██║   ██║  ██║███████╗██║  ██╗║
║    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝║
║                                                                           ║
║                      CAPTAIN'S CAREER SIMULATOR                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """
        print(title)
        
    def display_header(self, text):
        """Display a section header"""
        print("\n" + "=" * self.width)
        print(text.center(self.width))
        print("=" * self.width)
        
    def display_message(self, message):
        """Display a message"""
        print(message)
        
    def get_input(self, prompt):
        """Get input from user"""
        return input(prompt)
        
    def get_choice(self, prompt, valid_choices):
        """Get a validated choice from user"""
        while True:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"Invalid choice. Please enter a number between {min(valid_choices)} and {max(valid_choices)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    def confirm(self, prompt):
        """Get yes/no confirmation"""
        while True:
            response = input(f"{prompt} (y/n): ").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
                
    def main_menu(self):
        """Display main menu and get choice"""
        print("\n" + "=" * self.width)
        print("1. New Game")
        print("2. Load Game")
        print("3. Settings")
        print("4. Exit")
        print("=" * self.width)
        
        return self.get_input("\nEnter your choice: ")
        
    def ship_command_menu(self):
        """Display ship command menu"""
        print("\n" + "=" * self.width)
        print("SHIP OPERATIONS")
        print("=" * self.width)
        print("1. Navigation")
        print("2. Scan Sector")
        print("3. Ship Status")
        print("4. Crew Management")
        print("5. Communications")
        print("6. Away Team")
        print("7. Ship Requisition (Buy New Ships)")
        print("8. Captain's Log")
        print("9. Save Game")
        print("0. Return to Main Menu")
        print("=" * self.width)
        
        return self.get_input("\nEnter command: ")
        
    def display_status(self, game_state):
        """Display current game status"""
        char = game_state.character
        ship = game_state.ship
        
        print("\n" + "═" * self.width)
        print(f"Captain: {char.name} ({char.species}) | Rank: {char.rank}")
        print(f"Ship: {ship.name} ({ship.ship_class}-class) | Registry: {ship.registry}")
        print(f"Location: {game_state.galaxy.current_system}")
        print(f"Stardate: {game_state.stardate:.1f}")
        print(f"Experience: {char.experience} | Reputation: {char.reputation}")
        
        # Active missions
        if hasattr(game_state, 'mission_board') and game_state.mission_board.active_missions:
            print(f"Active Missions: {len(game_state.mission_board.active_missions)}/3")
        
        # Status bars for advanced ship
        hull_bar = self._create_status_bar(ship.hull, ship.max_hull, "Hull")
        # Average shield strength across all arcs
        avg_shields = sum(ship.shields.values()) / 4
        avg_max_shields = sum(ship.max_shields.values()) / 4
        shield_bar = self._create_status_bar(avg_shields, avg_max_shields, "Shields")
        
        print(f"{hull_bar}")
        print(f"{shield_bar}")
        print(f"Crew: {ship.crew_count}/{ship.max_crew} ({ship.crew_skill_level})")
        print("═" * self.width)
        
    def _create_status_bar(self, current, maximum, label):
        """Create a visual status bar"""
        percent = (current / maximum) * 100
        bar_width = 30
        filled = int((percent / 100) * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        if percent >= 70:
            color = ""
        elif percent >= 30:
            color = ""
        else:
            color = ""
            
        return f"{label}: [{bar}] {current:.0f}/{maximum:.0f} ({percent:.0f}%)"
        
    def display_ship_details(self, ship):
        """Display detailed ship information"""
        self.display_header(f"{ship.name} - SHIP STATUS")
        
        print(f"\nClass: {ship.ship_class} ({ship.type})")
        print(f"Registry: {ship.registry}")
        print(f"Era: {ship.era}")
        print(f"Size: {ship.size}")
        
        print(f"\n--- CREW ---")
        print(f"Crew: {ship.crew_count}/{ship.max_crew}")
        skill_level = ship.crew_skill_level
        skill_bonus = int(ship.get_crew_bonus() * 100)
        print(f"Crew Skill: {skill_level} (+{skill_bonus}% bonus)")
        
        print(f"\n--- DEFENSES ---")
        print(f"Hull Integrity: {ship.hull:.0f}/{ship.max_hull:.0f}")
        print(f"Armor Rating: {ship.armor}% damage reduction")
        print(f"Shields:")
        print(f"  Fore:      {ship.shields['fore']:.0f}/{ship.max_shields['fore']:.0f}")
        print(f"  Aft:       {ship.shields['aft']:.0f}/{ship.max_shields['aft']:.0f}")
        print(f"  Port:      {ship.shields['port']:.0f}/{ship.max_shields['port']:.0f}")
        print(f"  Starboard: {ship.shields['starboard']:.0f}/{ship.max_shields['starboard']:.0f}")
        
        print(f"\n--- POWER SYSTEMS ---")
        available_power = ship.get_available_power()
        print(f"Warp Core: {available_power:.0f}/{ship.warp_core_max_power:.0f} MW")
        print(f"Power Distribution:")
        print(f"  Engines: {ship.power_distribution['engines']} MW")
        print(f"  Shields: {ship.power_distribution['shields']} MW")
        print(f"  Weapons: {ship.power_distribution['weapons']} MW")
        
        print(f"\n--- NAVIGATION ---")
        print(f"Sensor Range: {ship.sensor_range} hexes")
        print(f"Turn Speed: {ship.turn_speed} (0=instant, 4=slow)")
        print(f"Impulse Speed: {ship.impulse_speed}")
        print(f"Maximum Warp: Warp {ship.warp_speed}")
        
        print(f"\n--- WEAPONS ---")
        print(f"Energy Weapons: {len(ship.weapon_arrays)}")
        for i, weapon in enumerate(ship.weapon_arrays, 1):
            arcs = ", ".join(weapon.firing_arcs)
            print(f"  {i}. {weapon.weapon_type.title()} Array - {weapon.base_damage} base dmg [{arcs}]")
        
        print(f"Torpedo Bays: {len(ship.torpedo_bays)}")
        for i, torp in enumerate(ship.torpedo_bays, 1):
            arcs = ", ".join(torp.firing_arcs)
            print(f"  {i}. {torp.torpedo_type.title()} - {torp.base_damage} base dmg, {torp.torpedoes}/{torp.max_torpedoes} [{arcs}]")
        
        print(f"\n--- SHIP SYSTEMS (Health 0-100) ---")
        systems_status = {
            'Warp Core': ship.warp_core,
            'Life Support': ship.life_support,
            'Warp Engines': ship.warp_engines,
            'Impulse Engines': ship.impulse_engines,
            'Weapons': ship.weapons_system,
            'Sensors': ship.sensors_system,
            'Shields': ship.shields_system,
            'Engineering': ship.engineering_system,
            'Sick Bay': ship.sick_bay
        }
        
        for system_name, health in systems_status.items():
            if health >= 75:
                status_indicator = "●"  # Green
            elif health >= 50:
                status_indicator = "◐"  # Yellow
            elif health >= 25:
                status_indicator = "◔"  # Orange
            else:
                status_indicator = "○"  # Red
            print(f"{status_indicator} {system_name}: {health:.0f}%")
        
        # Show efficiency impacts
        print(f"\n--- SYSTEM EFFICIENCY ---")
        print(f"Overall Crew Bonus: +{int(ship.get_crew_bonus() * 100)}%")
        print(f"Warp Core Efficiency: {ship.get_system_efficiency('warp_core')*100:.0f}%")
        print(f"Weapons Efficiency: {ship.get_system_efficiency('weapons')*100:.0f}%")
        print(f"Shields Efficiency: {ship.get_system_efficiency('shields')*100:.0f}%")
        print(f"Sensor Efficiency: {ship.get_system_efficiency('sensors')*100:.0f}%")
        
    def display_captain_log(self, game_state):
        """Display the captain's log"""
        self.display_header("CAPTAIN'S LOG")
        
        if not game_state.captain_log:
            print("\nNo log entries yet.")
            return
            
        # Display last 10 entries
        for entry in game_state.captain_log[-10:]:
            print(f"\n[Stardate {entry['stardate']:.1f}]")
            print(f"{entry['entry']}")
            
    def display_navigation_menu(self, nearby_systems):
        """Display navigation options"""
        self.display_header("NAVIGATION")
        
        if not nearby_systems:
            print("\nNo systems detected within warp range.")
            return None
            
        print("\nSystems within range:")
        for i, (name, system, distance) in enumerate(nearby_systems[:15], 1):
            explored = "✓" if system.explored else " "
            faction = system.controlling_faction or "Unclaimed"
            print(f"{i:2d}. [{explored}] {name:20s} - {distance:5.1f} LY - {faction}")
            
        print(f"{len(nearby_systems) + 1}. Return")
        return len(nearby_systems)
        
    def display_scan_results(self, system):
        """Display scan results for current system"""
        self.display_header(f"SCANNING: {system.name}")
        
        print(f"\nStar Type: {system.star_type}-class")
        print(f"Controlling Faction: {system.controlling_faction or 'Unclaimed Territory'}")
        print(f"Planets: {len(system.planets)}")
        
        if system.has_station:
            print("⚑ Space Station detected")
        if system.has_anomaly:
            print("⚠ Spatial anomaly detected")
        if system.inhabited:
            print(f"👥 Inhabited - Civilization Level {system.civilization_level}")
            
        if system.planets:
            print("\n--- PLANETARY BODIES ---")
            for planet in system.planets:
                life = "🌱" if planet['has_life'] else ""
                print(f"  Planet {planet['number']}: {planet['type']} {life}")
                if planet['resources'] != 'None':
                    print(f"    Resources: {planet['resources']}")
    
    def display_ship_requisition(self, character, current_ship_class):
        """Display available ships for requisition"""
        # NOTE: This method is deprecated. Ship requisition now uses advanced_ship.py directly.
        # Kept for backwards compatibility only.
        
        self.display_header("STARFLEET SHIP REQUISITION")
        
        print(f"\nYour Rank: {character.rank} (Level {character.rank_level})")
        print(f"Your Reputation: {character.reputation} points")
        print(f"Current Ship: {current_ship_class}-class")
        
        available_ships = Ship.get_available_ships(character)
        
        if not available_ships:
            print("\nNo ships available.")
            return None
        
        print("\n" + "=" * self.width)
        print("AVAILABLE STARSHIPS")
        print("=" * self.width)
        
        # Group by tier
        tiers = {}
        for ship_data in available_ships:
            tier = ship_data['specs']['min_rank']
            if tier not in tiers:
                tiers[tier] = []
            tiers[tier].append(ship_data)
        
        ship_list = []
        index = 1
        
        for tier in sorted(tiers.keys()):
            tier_names = ['Starting', 'Early Career', 'Early Career', 'Mid-Level', 
                         'Mid-Level', 'Advanced', 'Advanced', 'Elite', 'Elite', 
                         'Command', 'Command', 'Ultimate']
            tier_name = tier_names[tier] if tier < len(tier_names) else 'Maximum'
            
            print(f"\n--- TIER {tier}: {tier_name} ---")
            
            for ship_data in tiers[tier]:
                specs = ship_data['specs']
                can_afford = ship_data['can_afford']
                
                # Status indicators
                if ship_data['class'] == current_ship_class:
                    status = "[CURRENT]"
                elif not can_afford:
                    status = "[LOCKED - Need {0} Rep]".format(specs['reputation_cost'] - character.reputation)
                else:
                    status = "[AVAILABLE]"
                
                print(f"{index:2d}. {ship_data['class']:<20s} {status}")
                print(f"    Type: {specs['type']}")
                print(f"    Cost: {specs['reputation_cost']} Reputation | Min Rank: {character.RANKS[specs['min_rank']]}")
                armor_display = f" | Armor {specs.get('armor', 0)}" if specs.get('armor', 0) > 0 else ""
                print(f"    Stats: Hull {specs['hull']} | Shields {specs['shields']}{armor_display} | Weapons {specs['weapons']}")
                print(f"    Warp: {specs['warp']} | Crew: {specs['crew_capacity']}")
                
                ship_list.append((ship_data['class'], can_afford, ship_data['class'] == current_ship_class))
                index += 1
        
        return ship_list
    
    def display_ship_details_catalog(self, ship_class):
        """Display detailed information about a ship class"""
        # NOTE: This method is deprecated. Ship details now handled by advanced_ship.py.
        # Kept for backwards compatibility only.
        from game.ships import get_federation_ship
        
        temp_ship = get_federation_ship(ship_class, "USS Temp", "NCC-TEMP")
        if not temp_ship:
            self.display_message("Ship class not found.")
            return
            
        specs = {
            'type': temp_ship.type,
            'era': temp_ship.era,
            'description': f"{ship_class}-class starship",
            'reputation_cost': temp_ship.reputation_cost,
            'min_rank': temp_ship.minimum_rank,
            'hull': temp_ship.max_hull,
            'shields': sum(temp_ship.shields.values()) // 4,
            'armor': temp_ship.armor,
            'power': temp_ship.warp_core_max_power,
            'weapons': len(temp_ship.weapon_arrays),
            'sensors': temp_ship.sensor_range,
            'warp': temp_ship.warp_speed,
            'crew_capacity': temp_ship.max_crew
        }
        if not specs:
            self.display_message("Ship class not found.")
            return
        
        self.display_header(f"{ship_class.upper()}-CLASS STARSHIP")
        
        print(f"\nType: {specs['type']}")
        print(f"Era: {specs['era']}")
        print(f"\n{specs['description']}")
        
        print(f"\n--- REQUIREMENTS ---")
        print(f"Reputation Cost: {specs['reputation_cost']} points")
        from game.character import Character
        print(f"Minimum Rank: {Character.RANKS[specs['min_rank']]}")
        
        print(f"\n--- SPECIFICATIONS ---")
        print(f"Hull Strength: {specs['hull']}")
        print(f"Shield Capacity: {specs['shields']}")
        armor_value = specs.get('armor', 0)
        if armor_value > 0:
            print(f"Armor Plating: {armor_value}")
        print(f"Power Output: {specs['power']}")
        print(f"Weapon Systems: {specs['weapons']}")
        print(f"Sensor Array: {specs['sensors']}")
        print(f"Maximum Warp: {specs['warp']}")
        print(f"Crew Capacity: {specs['crew_capacity']}")
        
        # Calculate combat rating (now includes armor)
        combat_rating = (specs['hull'] + specs['shields'] + specs.get('armor', 0) + specs['weapons']) / 4
        science_rating = (specs['sensors'] + specs['power']) / 2
        
        print(f"\n--- RATINGS ---")
        print(f"Combat Effectiveness: {combat_rating:.0f}")
        print(f"Science Capability: {science_rating:.0f}")
        print(f"Exploration Range: {specs['warp']:.1f}")
