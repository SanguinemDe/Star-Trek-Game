"""
Navigation System
"""

import random

def navigate(game_state, ui):
    """Handle navigation between star systems"""
    current_system = game_state.galaxy.get_system(game_state.galaxy.current_system)
    
    # Get nearby systems within warp range
    warp_range = game_state.ship.warp_speed * 5  # 5 LY per warp factor
    nearby = game_state.galaxy.get_nearby_systems(game_state.galaxy.current_system, warp_range)
    
    while True:
        max_options = ui.display_navigation_menu(nearby)
        
        if max_options is None:
            input("\nPress Enter to continue...")
            return
            
        try:
            choice = int(ui.get_input(f"\nSelect destination (1-{max_options + 1}): "))
            
            if choice == max_options + 1:
                return
            elif 1 <= choice <= max_options:
                target_name, target_system, distance = nearby[choice - 1]
                
                # Calculate travel time
                warp_speed = game_state.ship.warp_speed
                travel_time = distance / (warp_speed ** (10/3))  # Cochrane's equation (simplified)
                days = max(1, int(travel_time * 100))
                
                ui.display_message(f"\nEngaging warp drive to {target_name}...")
                ui.display_message(f"Distance: {distance:.1f} light years")
                ui.display_message(f"Estimated travel time: {days} days at Warp {warp_speed}")
                
                if ui.confirm("Proceed?"):
                    # Travel to system
                    game_state.galaxy.current_system = target_name
                    game_state.ship.location = target_name
                    game_state.advance_time(days)
                    
                    # Consume resources
                    dilithium_used = int(distance * 2)
                    game_state.ship.dilithium = max(0, game_state.ship.dilithium - dilithium_used)
                    
                    # Process crew regeneration during travel
                    stardates = days / 365.25  # Convert days to approximate stardates
                    crew_recovered = game_state.ship.regenerate_crew(stardates)
                    if crew_recovered > 0:
                        ui.display_message(f"\n✓ Medical: {crew_recovered} crew members recovered during voyage")
                    
                    # Process life support damage (crew deaths during travel if life support damaged)
                    life_support_casualties = 0
                    if game_state.ship.systems['life_support'] < 100:
                        # Check for casualties each day of travel
                        for _ in range(days):
                            daily_casualties = game_state.ship.process_life_support_damage()
                            if daily_casualties > 0:
                                life_support_casualties += daily_casualties
                        
                        if life_support_casualties > 0:
                            ui.display_message(f"\n⚠ CRITICAL: {life_support_casualties} crew members lost due to life support failure!")
                            ui.display_message(f"   Life support status: {game_state.ship.systems['life_support']}%")
                            ui.display_message(f"   Recommend immediate repairs at nearest starbase!")
                    
                    # Mark as explored
                    target_system.explored = True
                    first_discovery = False
                    if target_name not in game_state.discovered_systems:
                        game_state.discovered_systems.add(target_name)
                        game_state.systems_explored += 1
                        first_discovery = True
                        
                        # Reputation bonus for discovering new systems
                        if target_system.is_canonical:
                            game_state.character.gain_reputation(10)
                            ui.display_message(f"✓ First visit to canonical system! Reputation +10")
                        else:
                            game_state.character.gain_reputation(5)
                            ui.display_message(f"✓ New system discovered! Reputation +5")
                        
                    # Log entry
                    game_state.add_log_entry(
                        f"Arrived at {target_name} system. Travel time: {days} days. "
                        f"Dilithium consumed: {dilithium_used} units."
                    )
                    
                    # Random encounter chance
                    if random.random() < 0.3:
                        encounter_event(game_state, ui, target_system)
                    
                    ui.display_message(f"\n✓ Arrived at {target_name}")
                    input("\nPress Enter to continue...")
                    return
            else:
                ui.display_message("Invalid selection.")
        except ValueError:
            ui.display_message("Invalid input. Please enter a number.")


def encounter_event(game_state, ui, system):
    """Handle random encounters during travel"""
    encounter_types = ['hostile', 'neutral', 'friendly', 'anomaly', 'distress']
    encounter = random.choice(encounter_types)
    
    if encounter == 'hostile':
        ui.display_message("\n⚠ RED ALERT! Hostile vessel detected!")
        faction = system.controlling_faction or "Unknown"
        if faction == 'Federation':
            faction = random.choice(['Klingon Empire', 'Romulan Star Empire', 'Cardassian Union'])
        
        ui.display_message(f"Sensors identify the vessel as {faction}.")
        game_state.add_log_entry(f"Encountered hostile {faction} vessel in {system.name} system.")
        
        # Simplified combat
        from game.combat import initiate_combat
        initiate_combat(game_state, ui, faction)
        
    elif encounter == 'distress':
        ui.display_message("\n📡 Distress signal detected!")
        ui.display_message("A Federation vessel is requesting assistance.")
        game_state.add_log_entry(f"Responded to distress call in {system.name} system.")
        
        if ui.confirm("Respond to distress call?"):
            ui.display_message("\nRendering assistance to distressed vessel...")
            game_state.character.gain_experience(20, 'command')
            game_state.add_log_entry("Successfully provided assistance. Crew morale improved.")
            game_state.ship.crew_morale = min(100, game_state.ship.crew_morale + 5)
            
    elif encounter == 'anomaly':
        ui.display_message("\n🌀 Spatial anomaly detected!")
        game_state.add_log_entry(f"Investigated spatial anomaly in {system.name} system.")
        
        if ui.confirm("Investigate anomaly?"):
            ui.display_message("\nScanning anomaly...")
            game_state.character.gain_experience(15, 'science')
            
            # Random effect
            effect = random.choice(['positive', 'negative', 'neutral'])
            if effect == 'positive':
                ui.display_message("Anomaly contained valuable scientific data!")
                game_state.add_log_entry("Anomaly investigation yielded valuable data.")
            elif effect == 'negative':
                damage = random.randint(5, 15)
                game_state.ship.take_damage(damage, 'shields')
                ui.display_message(f"Anomaly caused shield fluctuation! Shields reduced by {damage}.")
            else:
                ui.display_message("Anomaly was a naturally occurring subspace distortion.")
        
        input("\nPress Enter to continue...")
