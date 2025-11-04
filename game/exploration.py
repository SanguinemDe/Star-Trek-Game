"""
Exploration and Scanning System
"""

import random

def scan_sector(game_state, ui):
    """Scan the current sector/system"""
    current_system_name = game_state.galaxy.current_system
    current_system = game_state.galaxy.get_system(current_system_name)
    
    if not current_system:
        ui.display_message("Error: Current location unknown.")
        input("\nPress Enter to continue...")
        return
        
    # Display scan results
    ui.display_scan_results(current_system)
    
    # Check for interaction options
    print("\n--- AVAILABLE ACTIONS ---")
    actions = []
    
    if current_system.planets:
        actions.append("1. Scan Planets in Detail")
    if current_system.has_station:
        actions.append(f"{len(actions) + 1}. Dock at Space Station")
    if current_system.has_anomaly:
        actions.append(f"{len(actions) + 1}. Investigate Anomaly")
    if current_system.inhabited:
        actions.append(f"{len(actions) + 1}. Initiate First Contact Protocol")
        
    actions.append(f"{len(actions) + 1}. Return")
    
    for action in actions:
        print(action)
        
    if len(actions) == 1:  # Only "Return" option
        input("\nPress Enter to continue...")
        return
        
    try:
        choice = int(ui.get_input("\nSelect action: "))
        
        if choice == len(actions):
            return
        elif choice == 1 and "Scan Planets" in actions[0]:
            scan_planets(game_state, ui, current_system)
        elif current_system.has_station and "Dock at Space Station" in actions[choice - 1]:
            dock_at_station(game_state, ui, current_system)
        elif current_system.has_anomaly and "Investigate Anomaly" in actions[choice - 1]:
            investigate_anomaly(game_state, ui, current_system)
        elif current_system.inhabited and "First Contact" in actions[choice - 1]:
            first_contact(game_state, ui, current_system)
            
    except (ValueError, IndexError):
        ui.display_message("Invalid selection.")
        input("\nPress Enter to continue...")


def scan_planets(game_state, ui, system):
    """Perform detailed planetary scan"""
    ui.display_header(f"PLANETARY SCAN - {system.name}")
    
    science_bonus = game_state.character.attributes['science']
    
    for planet in system.planets:
        print(f"\n--- PLANET {planet['number']} ---")
        print(f"Classification: {planet['type']}")
        
        # Science check for detailed info
        if science_bonus >= 60:
            print(f"Life Signs: {'Detected' if planet['has_life'] else 'None'}")
            print(f"Resources: {planet['resources']}")
            
            if planet['type'] == 'M-Class' and planet['has_life']:
                print("⚠ Prime Directive considerations apply")
                
        elif science_bonus >= 40:
            print(f"Life Signs: {'Possible' if planet['has_life'] else 'Unlikely'}")
            print(f"Resources: {planet['resources'] if planet['resources'] != 'None' else 'Scanning...'}")
        else:
            print("Limited sensor data. Higher Science skill needed for detailed scan.")
            
    game_state.character.gain_experience(10, 'science')
    input("\nPress Enter to continue...")


def dock_at_station(game_state, ui, system):
    """Dock at a space station"""
    ui.display_header(f"DOCKING AT STATION - {system.name}")
    
    faction = system.controlling_faction or "Independent"
    relation = game_state.faction_relations.get(faction, 50)
    
    if relation < 0:
        ui.display_message(f"\n⚠ The {faction} station is refusing docking permission!")
        ui.display_message("Relations with this faction are too poor.")
        input("\nPress Enter to continue...")
        return
        
    ui.display_message(f"\nDocking clearance granted by {faction} station.")
    
    print("\n--- STATION SERVICES ---")
    print("1. Mission Board")
    print("2. Crew Recruitment")
    print("3. Repair Ship")
    print("4. Restock Supplies")
    print("5. Trade")
    print("6. Station Bar (Crew Morale)")
    print("7. Depart")
    
    while True:
        try:
            choice = int(ui.get_input("\nSelect service: "))
            
            if choice == 7:  # Depart
                break
            elif choice == 1:  # Mission Board
                from game.missions import mission_board_menu
                mission_board_menu(game_state, ui)
            elif choice == 2:  # Crew Recruitment
                from game.crew_recruitment import crew_recruitment_menu
                crew_recruitment_menu(game_state, ui)
            elif choice == 3:  # Repair Ship
                # Calculate total repair cost (hull + armor + systems)
                hull_repair = (game_state.ship.max_hull - game_state.ship.hull) * 2
                armor_repair = 0  # Armor is just a rating, not a resource that needs repair
                
                # Add system repair costs
                system_repair = 0
                for system_name, health in game_state.ship.systems.items():
                    if health < 100:
                        system_repair += (100 - health) * 5  # 5 dilithium per percent
                
                repair_cost = hull_repair + system_repair
                
                ui.display_message(f"\nHull repair: {hull_repair:.0f} dilithium")
                if system_repair > 0:
                    ui.display_message(f"System repairs: {system_repair:.0f} dilithium")
                ui.display_message(f"Total cost: {repair_cost:.0f} dilithium")
                
                if game_state.ship.dilithium >= repair_cost and ui.confirm("Proceed with repairs?"):
                    game_state.ship.dilithium -= int(repair_cost)
                    game_state.ship.hull = game_state.ship.max_hull
                    # Restore all shields to max
                    for arc in game_state.ship.shields:
                        game_state.ship.shields[arc] = game_state.ship.max_shields[arc]
                    # Restore all systems
                    for system in game_state.ship.systems:
                        game_state.ship.systems[system] = 100
                    ui.display_message("✓ Ship fully repaired!")
            elif choice == 4:  # Restock Supplies
                cost = 100
                ui.display_message(f"\nSupply cost: {cost} dilithium")
                if game_state.ship.dilithium >= cost and ui.confirm("Purchase supplies?"):
                    game_state.ship.dilithium -= cost
                    game_state.ship.provisions = 100
                    ui.display_message("✓ Supplies restocked!")
            elif choice == 5:  # Trade
                ui.display_message("\nTrade system coming soon!")
            elif choice == 6:  # Station Bar (Crew Morale)
                cost = 20
                if game_state.ship.dilithium >= cost and ui.confirm(f"Shore leave for crew? ({cost} dilithium)"):
                    game_state.ship.dilithium -= cost
                    game_state.ship.crew_morale = min(100, game_state.ship.crew_morale + 15)
                    ui.display_message("✓ Crew morale improved!")
            else:
                ui.display_message("Invalid selection.")
                
            input("\nPress Enter to continue...")
        except ValueError:
            ui.display_message("Invalid input.")


def investigate_anomaly(game_state, ui, system):
    """Investigate a spatial anomaly"""
    ui.display_header(f"INVESTIGATING ANOMALY - {system.name}")
    
    science_skill = game_state.character.attributes['science']
    
    # Apply science officer bonus to investigation
    science_bonus = game_state.ship.get_crew_bonus('science') / 100.0
    success_chance = (science_skill / 100.0) + (science_bonus * 0.3)
    
    ui.display_message("\nScanning spatial anomaly...")
    ui.display_message("This could be dangerous...")
    if science_bonus > 0:
        ui.display_message(f"(Science officer analyzing data: +{science_bonus*30:.1f}% success chance)")
    
    if not ui.confirm("Proceed with investigation?"):
        return
        
    if random.random() < success_chance:
        ui.display_message("\n✓ Investigation successful!")
        rewards = random.choice([
            ("valuable scientific data", 30, 'science'),
            ("unique mineral samples", 50, 'science'),
            ("new subspace phenomenon documented", 40, 'science')
        ])
        ui.display_message(f"Discovery: {rewards[0]}")
        game_state.character.gain_experience(rewards[1], rewards[2])
        game_state.add_log_entry(f"Successfully investigated anomaly in {system.name}: {rewards[0]}")
    else:
        ui.display_message("\n⚠ Anomaly destabilized!")
        damage = random.randint(10, 30)
        game_state.ship.take_damage(damage, 'fore')  # Assume damage hits forward shields
        ui.display_message(f"Ship took {damage} damage!")
        game_state.add_log_entry(f"Anomaly investigation in {system.name} caused ship damage.")
        
    system.has_anomaly = False  # Anomaly resolved
    input("\nPress Enter to continue...")


def first_contact(game_state, ui, system):
    """Initiate first contact with a civilization"""
    ui.display_header(f"FIRST CONTACT - {system.name}")
    
    diplomacy_skill = game_state.character.attributes['diplomacy']
    civ_level = system.civilization_level
    
    ui.display_message(f"\nCivilization Level: {civ_level}/10")
    ui.display_message("Initiating first contact protocols...")
    
    if civ_level < 4:
        ui.display_message("\n⚠ PRIME DIRECTIVE WARNING")
        ui.display_message("This civilization has not achieved warp capability.")
        ui.display_message("Contact would violate the Prime Directive.")
        
        if ui.confirm("Proceed anyway? (This will have consequences)"):
            game_state.modify_faction_relation('Federation', -20)
            ui.display_message("\nYour actions will be noted in your service record.")
            game_state.add_log_entry(f"Prime Directive violation in {system.name} system.")
        input("\nPress Enter to continue...")
        return
        
    # Diplomatic encounter - apply communications officer bonus
    comm_bonus = game_state.ship.get_crew_bonus('communications') / 100.0
    success_chance = ((diplomacy_skill + civ_level * 5) / 150.0) + (comm_bonus * 0.2)
    
    if comm_bonus > 0:
        ui.display_message(f"(Communications officer facilitating translation: +{comm_bonus*20:.1f}%)")
    
    if random.random() < success_chance:
        ui.display_message("\n✓ First contact successful!")
        ui.display_message("The civilization responds positively to Federation overtures.")
        game_state.character.gain_experience(50, 'diplomacy')
        game_state.character.gain_reputation(30)  # Good reputation for first contact
        ui.display_message("Reputation gained: +30 (First Contact Success)")
        game_state.diplomatic_victories += 1
        game_state.modify_faction_relation('Federation', 5)
        game_state.add_log_entry(f"Successful first contact with civilization in {system.name}.")
    else:
        ui.display_message("\n⚠ First contact unsuccessful.")
        ui.display_message("Cultural misunderstanding caused diplomatic incident.")
        game_state.character.gain_experience(10, 'diplomacy')
        game_state.add_log_entry(f"First contact attempt in {system.name} was unsuccessful.")
        
    input("\nPress Enter to continue...")
