"""
Away Team Mission System
"""

import random

def away_team_mission(game_state, ui):
    """Launch an away team mission"""
    ui.display_header("AWAY TEAM OPERATIONS")
    
    current_system = game_state.galaxy.get_system(game_state.galaxy.current_system)
    
    if not current_system:
        ui.display_message("Error: Current location unknown.")
        input("\nPress Enter to continue...")
        return
        
    # Check if there's a suitable target
    if not current_system.planets:
        ui.display_message("\nNo planetary bodies available for away team missions.")
        input("\nPress Enter to continue...")
        return
        
    print("\n--- AWAY TEAM TARGET SELECTION ---")
    
    # List available targets
    targets = []
    for planet in current_system.planets:
        if planet['type'] in ['M-Class', 'Desert', 'Ice', 'Ocean']:
            targets.append(planet)
            
    if not targets:
        ui.display_message("\nNo suitable planets for away team deployment.")
        input("\nPress Enter to continue...")
        return
        
    for i, planet in enumerate(targets, 1):
        life = "🌱" if planet['has_life'] else ""
        print(f"{i}. Planet {planet['number']} - {planet['type']} {life}")
    print(f"{len(targets) + 1}. Cancel")
    
    try:
        choice = int(ui.get_input("\nSelect target: "))
        
        if choice == len(targets) + 1:
            return
        elif 1 <= choice <= len(targets):
            target = targets[choice - 1]
            deploy_away_team(game_state, ui, current_system, target)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
            
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def deploy_away_team(game_state, ui, system, planet):
    """Deploy away team to planet surface"""
    ui.display_header(f"AWAY TEAM - {system.name} PLANET {planet['number']}")
    
    # Check transporter systems
    if game_state.ship.systems['transporter'] < 50:
        ui.display_message("\n⚠ Warning: Transporter systems damaged!")
        ui.display_message("Away team deployment is risky.")
        if not ui.confirm("Proceed anyway?"):
            return
            
    # Mission briefing
    ui.display_message(f"\nPlanet Type: {planet['type']}")
    ui.display_message(f"Life Signs: {'Detected' if planet['has_life'] else 'None'}")
    ui.display_message(f"Resources: {planet['resources']}")
    
    print("\n--- MISSION OBJECTIVES ---")
    print("1. Survey and Exploration")
    print("2. Resource Gathering")
    print("3. First Contact (if inhabited)")
    print("4. Rescue Mission")
    print("5. Cancel")
    
    try:
        objective = int(ui.get_input("\nSelect mission objective: "))
        
        if objective == 5:
            return
        elif objective == 1:
            exploration_mission(game_state, ui, planet)
        elif objective == 2:
            resource_mission(game_state, ui, planet)
        elif objective == 3:
            contact_mission(game_state, ui, planet)
        elif objective == 4:
            rescue_mission(game_state, ui, planet)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
            
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def exploration_mission(game_state, ui, planet):
    """Conduct planetary survey and exploration"""
    ui.display_message("\n🔵 Energizing... Away team deployed.")
    ui.display_message("Beginning planetary survey...")
    
    science = game_state.character.attributes['science']
    success_mod = science / 100
    
    # Random encounter
    encounter = random.random()
    
    if encounter < 0.1:  # Danger
        ui.display_message("\n⚠ EMERGENCY!")
        dangers = [
            "hostile wildlife",
            "geological instability",
            "toxic atmosphere",
            "unknown pathogen"
        ]
        danger = random.choice(dangers)
        ui.display_message(f"Away team encountered {danger}!")
        
        if random.random() < success_mod:
            ui.display_message("✓ Team handled situation professionally.")
            game_state.character.gain_experience(15, 'command')
            ui.display_message("All team members beamed back safely.")
        else:
            ui.display_message("✗ Minor injuries reported.")
            game_state.ship.crew_morale -= 5
            game_state.character.gain_experience(10, 'command')
            
    elif encounter < 0.4:  # Discovery
        ui.display_message("\n✓ Away team made a significant discovery!")
        discoveries = [
            ("Ancient ruins", 30, 'science'),
            ("Unique crystalline formations", 25, 'science'),
            ("New botanical species", 20, 'science'),
            ("Prehistoric fossils", 20, 'science'),
            ("Advanced technology remnants", 40, 'science')
        ]
        discovery, exp, skill = random.choice(discoveries)
        ui.display_message(f"Discovery: {discovery}")
        game_state.character.gain_experience(exp, skill)
        
        if "technology" in discovery:
            game_state.ship.dilithium += 50
            ui.display_message("Salvaged technology yielded 50 dilithium.")
            
    else:  # Routine survey
        ui.display_message("\n✓ Planetary survey completed successfully.")
        ui.display_message("Standard geological and biological samples collected.")
        game_state.character.gain_experience(15, 'science')
        
    game_state.add_log_entry(f"Away team mission to {planet['type']} planet completed.")
    input("\nPress Enter to continue...")


def resource_mission(game_state, ui, planet):
    """Gather resources from planet"""
    ui.display_message("\n🔵 Away team deployed for resource gathering.")
    
    if planet['resources'] == 'None':
        ui.display_message("\n✗ Scan results were inaccurate.")
        ui.display_message("No significant resources detected on surface.")
        game_state.character.gain_experience(5, 'science')
    else:
        engineering = game_state.character.attributes['engineering']
        success_chance = 0.6 + (engineering / 200)
        
        if random.random() < success_chance:
            ui.display_message(f"\n✓ Successfully harvested {planet['resources']}!")
            
            if 'Dilithium' in planet['resources']:
                amount = random.randint(50, 150)
                game_state.ship.dilithium += amount
                ui.display_message(f"Collected {amount} units of dilithium.")
            else:
                amount = random.randint(30, 80)
                game_state.ship.dilithium += amount
                ui.display_message(f"Converted resources to {amount} dilithium equivalent.")
                
            game_state.character.gain_experience(20, 'engineering')
        else:
            ui.display_message("\n✗ Resource extraction unsuccessful.")
            ui.display_message("Geological conditions prevented extraction.")
            game_state.character.gain_experience(10, 'engineering')
            
    game_state.add_log_entry(f"Resource gathering mission on {planet['type']} planet.")
    input("\nPress Enter to continue...")


def contact_mission(game_state, ui, planet):
    """Attempt first contact on inhabited planet"""
    if not planet['has_life']:
        ui.display_message("\n✗ No sentient life detected on planet.")
        input("\nPress Enter to continue...")
        return
        
    ui.display_message("\n🔵 Away team deployed for first contact mission.")
    ui.display_message("Scanning for sentient life forms...")
    
    diplomacy = game_state.character.attributes['diplomacy']
    
    # Check for civilization
    if random.random() < 0.3:
        ui.display_message("\n✓ Sentient life forms detected!")
        
        success_chance = 0.5 + (diplomacy / 150)
        
        if random.random() < success_chance:
            ui.display_message("\n✓ First contact successful!")
            ui.display_message("The indigenous species responds positively.")
            ui.display_message("Cultural exchange initiated.")
            game_state.character.gain_experience(40, 'diplomacy')
            game_state.diplomatic_victories += 1
            game_state.modify_faction_relation('Federation', 5)
        else:
            ui.display_message("\n⚠ First contact complicated.")
            ui.display_message("Cultural barriers prevent meaningful communication.")
            ui.display_message("Team withdrew per Prime Directive guidelines.")
            game_state.character.gain_experience(15, 'diplomacy')
    else:
        ui.display_message("\n✓ Only non-sentient life forms detected.")
        ui.display_message("Biological survey conducted.")
        game_state.character.gain_experience(10, 'science')
        
    game_state.add_log_entry(f"First contact mission on {planet['type']} planet.")
    input("\nPress Enter to continue...")


def rescue_mission(game_state, ui, planet):
    """Conduct rescue operation"""
    ui.display_message("\n🔵 Away team deployed for rescue operation.")
    ui.display_message("Scanning for distress beacon...")
    
    if random.random() < 0.6:
        ui.display_message("\n✓ Distress beacon located!")
        
        command = game_state.character.attributes['command']
        tactical = game_state.character.attributes['tactical']
        success_chance = 0.5 + ((command + tactical) / 300)
        
        if random.random() < success_chance:
            ui.display_message("\n✓ Rescue operation successful!")
            survivors = random.randint(3, 15)
            ui.display_message(f"Rescued {survivors} survivors from crashed shuttle.")
            ui.display_message("All survivors beamed aboard for medical treatment.")
            game_state.character.gain_experience(30, 'command')
            game_state.ship.crew_morale = min(100, game_state.ship.crew_morale + 10)
            game_state.modify_faction_relation('Federation', 8)
        else:
            ui.display_message("\n⚠ Rescue operation partially successful.")
            ui.display_message("Hostile conditions complicated rescue efforts.")
            ui.display_message("Some survivors recovered.")
            game_state.character.gain_experience(15, 'command')
            game_state.ship.crew_morale = min(100, game_state.ship.crew_morale + 3)
    else:
        ui.display_message("\n✗ No distress signal detected.")
        ui.display_message("False alarm or signal source no longer active.")
        game_state.character.gain_experience(5, 'command')
        
    game_state.add_log_entry(f"Rescue mission on {planet['type']} planet.")
    input("\nPress Enter to continue...")
