"""
Ship Requisition System
Allows players to purchase new ships using reputation points
"""

import random
from game.ships import get_federation_ships_by_rank, get_federation_ship


def ship_requisition(game_state, ui):
    """Handle ship requisition/purchase"""
    while True:
        ui.display_header("STARFLEET SHIP REQUISITION")
        
        # Get available ships
        available_ships = get_federation_ships_by_rank(
            min_rank=0,
            max_rank=game_state.character.rank_level,
            player_reputation=game_state.character.reputation
        )
        
        if not available_ships:
            ui.display_message("\nNo ships available for requisition.")
            input("\nPress Enter to continue...")
            return
        
        # Display current ship
        ui.display_message(f"\nCurrent Ship: {game_state.ship.name} ({game_state.ship.ship_class}-class)")
        ui.display_message(f"Your Reputation: {game_state.character.reputation}")
        ui.display_message(f"Your Rank: {game_state.character.rank} (Level {game_state.character.rank_level})")
        
        # Display available ships grouped by rank
        ui.display_message("\n=== AVAILABLE SHIPS ===\n")
        
        current_rank = -1
        for i, ship_info in enumerate(available_ships, 1):
            if ship_info['minimum_rank'] != current_rank:
                current_rank = ship_info['minimum_rank']
                rank_names = ['Lt Commander', 'Lt Commander', 'Commander', 'Commander', 
                             'Captain', 'Captain', 'Commodore', 'Rear Admiral', 'Vice Admiral']
                rank_name = rank_names[current_rank] if current_rank < len(rank_names) else f"Rank {current_rank}"
                ui.display_message(f"\n--- RANK {current_rank}: {rank_name} ---")
            
            is_current = (ship_info['class'] == game_state.ship.ship_class)
            status = "[CURRENT]" if is_current else ""
            
            ui.display_message(
                f"{i}. {ship_info['class']}-class {status}\n"
                f"   Type: {ship_info['type']} | Era: {ship_info['era']}\n"
                f"   Cost: {ship_info['reputation_cost']} Rep | Hull: {ship_info['hull']} | "
                f"Crew: {ship_info['crew']}\n"
                f"   Size: {ship_info['size']} | Warp: {ship_info['warp']} | Sensors: {ship_info['sensors']}"
            )
        
        ui.display_message(f"\n{len(available_ships) + 1}. View Ship Details")
        ui.display_message(f"{len(available_ships) + 2}. Return to Ship Command")
        
        try:
            choice = int(ui.get_input("\nSelect option: "))
            
            if choice == len(available_ships) + 2:
                return
            elif choice == len(available_ships) + 1:
                # View detailed stats
                class_name = ui.get_input("\nEnter ship class name to view: ")
                view_ship_details(class_name, ui)
                input("\nPress Enter to continue...")
            elif 1 <= choice <= len(available_ships):
                ship_info = available_ships[choice - 1]
                
                if ship_info['class'] == game_state.ship.ship_class:
                    ui.display_message("\n✗ You already command this ship class!")
                    input("\nPress Enter to continue...")
                else:
                    # Purchase ship
                    purchase_ship(game_state, ui, ship_info)
            else:
                ui.display_message("✗ Invalid selection.")
                input("\nPress Enter to continue...")
        except (ValueError, EOFError, KeyboardInterrupt):
            ui.display_message("✗ Invalid input.")
            input("\nPress Enter to continue...")


def view_ship_details(ship_class, ui):
    """Display detailed stats for a ship class"""
    # Create temporary ship to get stats
    temp_ship = get_federation_ship(ship_class, "USS Temp", "NCC-TEMP")
    
    if not temp_ship:
        ui.display_message(f"\n✗ Ship class '{ship_class}' not found.")
        return
    
    ui.display_header(f"{ship_class.upper()}-CLASS SPECIFICATIONS")
    
    ui.display_message(f"\nShip Type: {temp_ship.type}")
    ui.display_message(f"Era: {temp_ship.era}")
    ui.display_message(f"Size Category: {temp_ship.size}")
    
    ui.display_message(f"\n--- REQUIREMENTS ---")
    ui.display_message(f"Minimum Rank: {temp_ship.minimum_rank}")
    ui.display_message(f"Reputation Cost: {temp_ship.reputation_cost}")
    
    ui.display_message(f"\n--- NAVIGATION ---")
    ui.display_message(f"Sensor Range: {temp_ship.sensor_range} hexes")
    ui.display_message(f"Turn Speed: {temp_ship.turn_speed} (0=instant, 4=slow)")
    ui.display_message(f"Impulse Speed: {temp_ship.impulse_speed}")
    ui.display_message(f"Warp Speed: Warp {temp_ship.warp_speed}")
    
    ui.display_message(f"\n--- DEFENSES ---")
    ui.display_message(f"Hull: {temp_ship.hull}/{temp_ship.max_hull}")
    ui.display_message(f"Armor: {temp_ship.armor}% damage reduction")
    ui.display_message(f"Shields:")
    ui.display_message(f"  Fore: {temp_ship.shields['fore']}")
    ui.display_message(f"  Aft:  {temp_ship.shields['aft']}")
    ui.display_message(f"  Port: {temp_ship.shields['port']}")
    ui.display_message(f"  Starboard: {temp_ship.shields['starboard']}")
    
    ui.display_message(f"\n--- POWER & SYSTEMS ---")
    ui.display_message(f"Warp Core: {temp_ship.warp_core_max_power} MW")
    ui.display_message(f"Power Distribution: Engines {temp_ship.power_distribution['engines']}MW | "
                      f"Shields {temp_ship.power_distribution['shields']}MW | "
                      f"Weapons {temp_ship.power_distribution['weapons']}MW")
    
    ui.display_message(f"\n--- OFFENSE ---")
    ui.display_message(f"Weapon Arrays: {len(temp_ship.weapon_arrays)}")
    for i, weapon in enumerate(temp_ship.weapon_arrays, 1):
        arcs = ", ".join(weapon.firing_arcs)
        ui.display_message(f"  {i}. {weapon.weapon_type.title()} Array - {weapon.base_damage} dmg [{arcs}]")
    
    ui.display_message(f"Torpedo Bays: {len(temp_ship.torpedo_bays)}")
    for i, torp in enumerate(temp_ship.torpedo_bays, 1):
        arcs = ", ".join(torp.firing_arcs)
        ui.display_message(f"  {i}. {torp.torpedo_type.title()} - {torp.base_damage} dmg, {torp.torpedoes}/{torp.max_torpedoes} [{arcs}]")
    
    ui.display_message(f"\n--- CAPACITY ---")
    ui.display_message(f"Crew: {temp_ship.crew_count}/{temp_ship.max_crew}")
    ui.display_message(f"Cargo Space: {temp_ship.cargo_space}")
    ui.display_message(f"Upgrade Space: {temp_ship.upgrade_space}")


def purchase_ship(game_state, ui, ship_info):
    """Purchase and transfer to a new ship"""
    ship_class = ship_info['class']
    
    ui.display_header(f"REQUISITION: {ship_class.upper()}-CLASS")
    
    # Create temporary ship to compare
    temp_ship = get_federation_ship(ship_class, "USS Temp", "NCC-TEMP")
    
    ui.display_message(f"\nYou are requesting transfer to a {ship_class}-class starship.")
    ui.display_message(f"\nCost: {ship_info['reputation_cost']} Reputation")
    ui.display_message(f"Your Current Reputation: {game_state.character.reputation}")
    ui.display_message(f"Remaining After Purchase: {game_state.character.reputation - ship_info['reputation_cost']}")
    
    ui.display_message(f"\n--- COMPARISON ---")
    ui.display_message(f"\nCurrent Ship: {game_state.ship.ship_class}-class")
    ui.display_message(f"  Hull: {game_state.ship.max_hull} | Armor: {game_state.ship.armor}% | Crew: {game_state.ship.max_crew}")
    ui.display_message(f"  Weapons: {len(game_state.ship.weapon_arrays)} arrays, {len(game_state.ship.torpedo_bays)} torpedo bays")
    ui.display_message(f"  Warp: {game_state.ship.warp_speed} | Sensors: {game_state.ship.sensor_range}")
    
    ui.display_message(f"\nNew Ship: {ship_class}-class")
    ui.display_message(f"  Hull: {temp_ship.max_hull} | Armor: {temp_ship.armor}% | Crew: {temp_ship.max_crew}")
    ui.display_message(f"  Weapons: {len(temp_ship.weapon_arrays)} arrays, {len(temp_ship.torpedo_bays)} torpedo bays")
    ui.display_message(f"  Warp: {temp_ship.warp_speed} | Sensors: {temp_ship.sensor_range}")
    
    if not ui.confirm("\nConfirm ship requisition?"):
        return
    
    # Deduct reputation
    game_state.character.reputation -= ship_info['reputation_cost']
    
    # Generate registry
    registry = f"NCC-{random.randint(70000, 99999)}"
    
    # Let player name the ship
    default_names = {
        'Miranda': 'USS Reliant',
        'Constitution': 'USS Enterprise',
        'Excelsior': 'USS Excelsior',
        'Defiant': 'USS Defiant',
        'Intrepid': 'USS Voyager',
        'Galaxy': 'USS Enterprise-D',
        'Sovereign': 'USS Enterprise-E',
        'Prometheus': 'USS Prometheus',
        'Odyssey': 'USS Enterprise-F',
    }
    
    suggested_name = default_names.get(ship_class, f'USS {ship_class}')
    
    ui.display_message(f"\n--- SHIP NAMING ---")
    ui.display_message(f"Suggested name: {suggested_name}")
    ship_name = ui.get_input(f"Enter ship name (or press Enter for '{suggested_name}'): ")
    
    if not ship_name:
        ship_name = suggested_name
    elif not ship_name.startswith('USS '):
        ship_name = f"USS {ship_name}"
    
    # Save current ship's location
    old_location = getattr(game_state.ship, 'location', None)
    old_sector_x = getattr(game_state.ship, 'sector_x', 0)
    old_sector_y = getattr(game_state.ship, 'sector_y', 0)
    
    # Create new ship
    new_ship = get_federation_ship(ship_class, ship_name, registry)
    
    # Transfer location
    if hasattr(new_ship, 'location'):
        new_ship.location = old_location
    if hasattr(new_ship, 'sector_x'):
        new_ship.sector_x = old_sector_x
        new_ship.sector_y = old_sector_y
    
    # Log the event
    old_ship_name = game_state.ship.name
    old_ship_class = game_state.ship.ship_class
    
    # Replace ship
    game_state.ship = new_ship
    
    game_state.add_log_entry(
        f"Transferred command from {old_ship_name} ({old_ship_class}-class) to "
        f"{ship_name} ({ship_class}-class). Registry: {registry}"
    )
    
    ui.display_message("\n" + "=" * 80)
    ui.display_message("✓ TRANSFER APPROVED")
    ui.display_message("=" * 80)
    ui.display_message(f"\nYou are now in command of the {ship_name}")
    ui.display_message(f"Ship Class: {ship_class}")
    ui.display_message(f"Registry: {registry}")
    ui.display_message(f"\nAll systems nominal. Ready for deployment.")
    ui.display_message(f"\nRemaining Reputation: {game_state.character.reputation}")
    
    # Bonus experience for getting a new ship
    exp_gain = ship_info['reputation_cost'] // 10
    promoted = game_state.character.gain_experience(exp_gain, 'command')
    ui.display_message(f"\nGained {exp_gain} Command experience for taking command of a new vessel!")
    
    if promoted:
        ui.display_message(f"\n🎖️  PROMOTED TO {game_state.character.rank.upper()}! 🎖️")
    
    input("\nPress Enter to continue...")
