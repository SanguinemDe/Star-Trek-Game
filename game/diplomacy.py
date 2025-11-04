"""
Diplomacy and Communications System
"""

import random

def communications(game_state, ui):
    """Handle communications and diplomacy"""
    ui.display_header("COMMUNICATIONS")
    
    print("\n--- COMMUNICATIONS OPTIONS ---")
    print("1. Faction Relations Status")
    print("2. Send Diplomatic Message")
    print("3. Receive Transmissions")
    print("4. Return")
    
    try:
        choice = int(ui.get_input("\nSelect option: "))
        
        if choice == 1:
            display_faction_relations(game_state, ui)
        elif choice == 2:
            send_diplomatic_message(game_state, ui)
        elif choice == 3:
            receive_transmissions(game_state, ui)
        elif choice == 4:
            return
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
            
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def display_faction_relations(game_state, ui):
    """Display current faction relations"""
    ui.display_header("FACTION RELATIONS")
    
    print("\nCurrent standing with major powers:\n")
    
    for faction, relation in sorted(game_state.faction_relations.items()):
        status = game_state.get_faction_status(faction)
        
        # Visual indicator
        if relation >= 70:
            indicator = "✓✓"
        elif relation >= 40:
            indicator = "✓ "
        elif relation >= 0:
            indicator = "~ "
        elif relation >= -40:
            indicator = "✗ "
        else:
            indicator = "✗✗"
            
        print(f"{indicator} {faction:25s}: {relation:4d} ({status})")
        
    input("\nPress Enter to continue...")


def send_diplomatic_message(game_state, ui):
    """Send a diplomatic message to a faction"""
    ui.display_header("DIPLOMATIC COMMUNICATIONS")
    
    print("\nSelect faction to contact:")
    factions = list(game_state.faction_relations.keys())
    for i, faction in enumerate(factions, 1):
        status = game_state.get_faction_status(faction)
        print(f"{i}. {faction} ({status})")
    print(f"{len(factions) + 1}. Cancel")
    
    try:
        choice = int(ui.get_input("\nSelect faction: "))
        
        if choice == len(factions) + 1:
            return
        elif 1 <= choice <= len(factions):
            faction = factions[choice - 1]
            conduct_diplomacy(game_state, ui, faction)
        else:
            ui.display_message("Invalid selection.")
            input("\nPress Enter to continue...")
            
    except ValueError:
        ui.display_message("Invalid input.")
        input("\nPress Enter to continue...")


def conduct_diplomacy(game_state, ui, faction):
    """Conduct diplomatic negotiations with a faction"""
    current_relation = game_state.faction_relations[faction]
    status = game_state.get_faction_status(faction)
    
    ui.display_message(f"\nOpening channel to {faction}...")
    ui.display_message(f"Current relations: {status} ({current_relation})")
    
    print("\n--- DIPLOMATIC OPTIONS ---")
    print("1. Peaceful Greeting")
    print("2. Trade Proposal")
    print("3. Request Alliance")
    print("4. Issue Warning")
    print("5. Close Channel")
    
    try:
        choice = int(ui.get_input("\nSelect action: "))
        
        diplomacy = game_state.character.attributes['diplomacy']
        
        if choice == 1:  # Greeting
            success_chance = 0.7 + (diplomacy / 200)
            if random.random() < success_chance:
                change = random.randint(1, 5)
                game_state.modify_faction_relation(faction, change)
                ui.display_message(f"\n✓ {faction} responds positively. Relations improved by {change}.")
                game_state.character.gain_experience(5, 'diplomacy')
            else:
                ui.display_message(f"\n{faction} acknowledges your transmission.")
                
        elif choice == 2:  # Trade
            if current_relation < 20:
                ui.display_message(f"\n{faction} refuses to engage in trade negotiations.")
            else:
                success_chance = 0.5 + (diplomacy / 150)
                if random.random() < success_chance:
                    change = random.randint(3, 8)
                    game_state.modify_faction_relation(faction, change)
                    game_state.ship.dilithium += 100
                    ui.display_message(f"\n✓ Trade agreement reached! Relations improved by {change}.")
                    ui.display_message("Received 100 dilithium crystals.")
                    game_state.character.gain_experience(15, 'diplomacy')
                    game_state.character.gain_reputation(10)
                    ui.display_message("Reputation gained: +10 (Trade Agreement)")
                else:
                    ui.display_message(f"\n{faction} declines your trade proposal.")
                    game_state.character.gain_experience(5, 'diplomacy')
                    
        elif choice == 3:  # Alliance
            if current_relation < 60:
                ui.display_message(f"\n{faction} is not interested in an alliance at this time.")
                ui.display_message("Improve relations before making this request.")
            else:
                success_chance = 0.3 + (diplomacy / 120)
                if random.random() < success_chance:
                    change = 15
                    game_state.modify_faction_relation(faction, change)
                    ui.display_message(f"\n✓ {faction} agrees to a formal alliance!")
                    ui.display_message(f"Relations improved by {change}.")
                    game_state.character.gain_experience(30, 'diplomacy')
                    game_state.character.gain_reputation(50)  # Major reputation for alliance
                    ui.display_message("Reputation gained: +50 (Major Alliance)")
                    game_state.diplomatic_victories += 1
                else:
                    change = -5
                    game_state.modify_faction_relation(faction, change)
                    ui.display_message(f"\n{faction} rejects your proposal. Relations damaged.")
                    game_state.character.gain_experience(10, 'diplomacy')
                    
        elif choice == 4:  # Warning
            change = random.randint(-10, -5)
            game_state.modify_faction_relation(faction, change)
            ui.display_message(f"\n{faction} responds with hostility to your warning.")
            ui.display_message(f"Relations decreased by {abs(change)}.")
            
        elif choice == 5:  # Close
            return
        else:
            ui.display_message("Invalid selection.")
            
    except ValueError:
        ui.display_message("Invalid input.")
        
    input("\nPress Enter to continue...")


def receive_transmissions(game_state, ui):
    """Receive and respond to incoming transmissions"""
    ui.display_header("INCOMING TRANSMISSIONS")
    
    # Random transmission chance
    if random.random() < 0.4:
        transmission_types = ['mission_offer', 'distress', 'intel', 'greeting']
        trans_type = random.choice(transmission_types)
        
        if trans_type == 'mission_offer':
            ui.display_message("\n📡 Starfleet Command - Mission Assignment")
            missions = [
                "Investigate unusual readings in the Neutral Zone",
                "Escort convoy through contested space",
                "Mediate territorial dispute",
                "Respond to colony distress signal"
            ]
            mission = random.choice(missions)
            ui.display_message(f"Mission: {mission}")
            
            if ui.confirm("\nAccept mission?"):
                game_state.missions_completed += 1
                game_state.character.gain_experience(25, 'command')
                ui.display_message("✓ Mission accepted and logged.")
                game_state.add_log_entry(f"Accepted mission: {mission}")
                
        elif trans_type == 'distress':
            ui.display_message("\n📡 Distress Signal - Unknown Origin")
            ui.display_message("A vessel is requesting immediate assistance.")
            ui.display_message("Warning: This could be a trap.")
            
            if ui.confirm("\nInvestigate signal?"):
                if random.random() < 0.6:
                    ui.display_message("\n✓ Vessel rescued successfully!")
                    game_state.character.gain_experience(20, 'command')
                    game_state.modify_faction_relation('Federation', 5)
                else:
                    ui.display_message("\n⚠ It was a trap! Ambush detected!")
                    # Could trigger combat here
                    
        elif trans_type == 'intel':
            ui.display_message("\n📡 Starfleet Intelligence - Classified Report")
            factions = list(game_state.faction_relations.keys())
            faction = random.choice(factions)
            ui.display_message(f"Intelligence on {faction} activities in your sector.")
            game_state.character.gain_experience(10, 'command')
            
        elif trans_type == 'greeting':
            factions = [f for f, r in game_state.faction_relations.items() if r > 30]
            if factions:
                faction = random.choice(factions)
                ui.display_message(f"\n📡 {faction} - Friendly Hail")
                ui.display_message("A vessel from a friendly faction greets you.")
                game_state.modify_faction_relation(faction, 1)
    else:
        ui.display_message("\nNo new transmissions at this time.")
        
    input("\nPress Enter to continue...")
