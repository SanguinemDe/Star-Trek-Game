"""
Combat System
"""

import random

class Enemy:
    """Represents an enemy vessel"""
    
    SHIP_TYPES = {
        'Scout': {'hull': 50, 'shields': 40, 'weapons': 30},
        'Frigate': {'hull': 80, 'shields': 70, 'weapons': 60},
        'Cruiser': {'hull': 120, 'shields': 100, 'weapons': 90},
        'Battleship': {'hull': 180, 'shields': 150, 'weapons': 130},
        'Dreadnought': {'hull': 250, 'shields': 200, 'weapons': 170}
    }
    
    def __init__(self, faction, ship_type):
        self.faction = faction
        self.ship_type = ship_type
        self.specs = self.SHIP_TYPES[ship_type].copy()
        self.current_hull = self.specs['hull']
        self.current_shields = self.specs['shields']
        
    def take_damage(self, amount):
        """Enemy takes damage"""
        overflow = max(0, amount - self.current_shields)
        self.current_shields = max(0, self.current_shields - amount)
        if overflow > 0:
            self.current_hull = max(0, self.current_hull - overflow)
            
    def is_destroyed(self):
        """Check if enemy is destroyed"""
        return self.current_hull <= 0
        
    def attack(self):
        """Enemy attacks, returns damage amount and weapon type"""
        base_damage = self.specs['weapons']
        damage = random.randint(int(base_damage * 0.7), int(base_damage * 1.3))
        
        # Enemy ships choose weapons randomly based on ship type
        # Smaller ships favor phasers, larger ships use more torpedoes
        if self.ship_type in ['Scout', 'Frigate']:
            weapon_type = random.choice(['phaser', 'phaser', 'phaser', 'torpedo'])  # 75% phaser
        elif self.ship_type == 'Cruiser':
            weapon_type = random.choice(['phaser', 'phaser', 'torpedo'])  # 66% phaser
        else:  # Battleship, Dreadnought
            weapon_type = random.choice(['phaser', 'torpedo', 'torpedo'])  # 66% torpedo
        
        return damage, weapon_type


def initiate_combat(game_state, ui, enemy_faction):
    """Start a combat encounter"""
    ui.display_header("COMBAT ENGAGEMENT")
    
    # Determine enemy ship type based on player strength
    player_strength = (game_state.ship.specs['hull'] + 
                      game_state.ship.specs['weapons'] + 
                      game_state.ship.specs['shields']) / 3
    
    if player_strength < 80:
        ship_type = random.choice(['Scout', 'Frigate'])
    elif player_strength < 120:
        ship_type = random.choice(['Frigate', 'Cruiser'])
    elif player_strength < 160:
        ship_type = random.choice(['Cruiser', 'Battleship'])
    else:
        ship_type = random.choice(['Battleship', 'Dreadnought'])
        
    enemy = Enemy(enemy_faction, ship_type)
    
    ui.display_message(f"\n⚠ Engaging {enemy_faction} {ship_type}!")
    game_state.add_log_entry(f"Combat engagement with {enemy_faction} {ship_type}.")
    
    combat_loop(game_state, ui, enemy)


def combat_loop(game_state, ui, enemy):
    """Main combat loop"""
    turn = 0
    
    while True:
        turn += 1
        ui.display_header(f"COMBAT - TURN {turn}")
        
        # Display status
        print(f"\n=== YOUR SHIP ===")
        print(f"Hull: {game_state.ship.current_hull:.0f}/{game_state.ship.specs['hull']:.0f}")
        print(f"Shields: {game_state.ship.current_shields:.0f}/{game_state.ship.specs['shields']:.0f}")
        
        print(f"\n=== ENEMY ({enemy.faction} {enemy.ship_type}) ===")
        print(f"Hull: {enemy.current_hull:.0f}/{enemy.specs['hull']:.0f}")
        print(f"Shields: {enemy.current_shields:.0f}/{enemy.specs['shields']:.0f}")
        
        # Player actions
        print("\n--- TACTICAL OPTIONS ---")
        print("1. Fire Phasers (Moderate damage, accurate)")
        print("2. Fire Torpedoes (High damage, less accurate)")
        print("3. Evasive Maneuvers (Reduce incoming damage)")
        print("4. Raise Shields (Restore shield strength)")
        print("5. Hail Enemy (Attempt diplomacy)")
        print("6. Retreat (Attempt to flee)")
        
        try:
            action = int(ui.get_input("\nSelect action: "))
            
            if action == 1:  # Phasers
                tactical = game_state.character.attributes['tactical']
                
                # Get system penalties
                penalties = game_state.ship.get_system_penalties()
                
                # Apply tactical officer bonus and system penalties to hit chance
                tactical_bonus = game_state.ship.get_crew_bonus('tactical') / 100.0
                hit_chance = (0.8 + (tactical / 200) + tactical_bonus) * penalties['weapons_accuracy']
                
                if random.random() < hit_chance:
                    # Apply tactical officer bonus and system penalties to damage
                    base_damage = game_state.ship.specs['weapons'] * (1 + tactical_bonus)
                    damage = (base_damage * penalties['weapons_damage']) + random.randint(-10, 10)
                    enemy.take_damage(damage)
                    ui.display_message(f"\n✓ Direct hit! Enemy took {damage:.0f} damage.")
                    ui.display_message(f"   [Phaser: Depletes shields quickly, moderate hull damage]")
                    if tactical_bonus > 0:
                        ui.display_message(f"   (Tactical officer bonus: +{tactical_bonus*100:.1f}%)")
                    if penalties['weapons_damage'] < 1.0:
                        ui.display_message(f"   ⚠ Weapon systems damaged: {penalties['weapons_damage']*100:.0f}% effectiveness")
                    game_state.character.gain_experience(5, 'tactical')
                else:
                    ui.display_message("\n✗ Phaser fire missed!")
                    
            elif action == 2:  # Torpedoes
                tactical = game_state.character.attributes['tactical']
                
                # Get system penalties
                penalties = game_state.ship.get_system_penalties()
                
                # Apply tactical officer bonus and system penalties
                tactical_bonus = game_state.ship.get_crew_bonus('tactical') / 100.0
                hit_chance = (0.6 + (tactical / 250) + (tactical_bonus * 0.8)) * penalties['weapons_accuracy']
                
                if random.random() < hit_chance:
                    # Apply tactical officer bonus and system penalties to damage
                    base_damage = game_state.ship.specs['weapons'] * 1.5 * (1 + tactical_bonus)
                    damage = (base_damage * penalties['weapons_damage']) + random.randint(-15, 15)
                    enemy.take_damage(damage, 'shields', 'torpedo')
                    ui.display_message(f"\n✓ Torpedo impact! Enemy took {damage:.0f} damage.")
                    ui.display_message(f"   [Torpedo: Shields resist well, DEVASTATING if they fail!]")
                    if tactical_bonus > 0:
                        ui.display_message(f"   (Tactical officer bonus: +{tactical_bonus*100:.1f}%)")
                    if penalties['weapons_damage'] < 1.0:
                        ui.display_message(f"   ⚠ Weapon systems damaged: {penalties['weapons_damage']*100:.0f}% effectiveness")
                    game_state.character.gain_experience(8, 'tactical')
                else:
                    ui.display_message("\n✗ Torpedo missed its target!")
                    
            elif action == 3:  # Evasive maneuvers
                command = game_state.character.attributes['command']
                
                # Apply conn officer bonus to evasion
                conn_bonus = game_state.ship.get_crew_bonus('conn') / 100.0
                evasion = 0.3 + (command / 200) + (conn_bonus * 0.5)
                ui.display_message(f"\nExecuting evasive pattern delta. Evasion bonus: {evasion*100:.0f}%")
                if conn_bonus > 0:
                    ui.display_message(f"(Conn officer enhancing maneuverability: +{conn_bonus*50:.1f}%)")
                
                # Enemy attack with reduced damage
                enemy_damage, weapon_type = enemy.attack()
                enemy_damage = int(enemy_damage * (1 - evasion))
                game_state.ship.take_damage(enemy_damage, 'shields', weapon_type)
                weapon_name = "Phaser fire" if weapon_type == 'phaser' else "Torpedo"
                ui.display_message(f"Enemy {weapon_name} inflicted {enemy_damage:.0f} damage (evaded {evasion*100:.0f}%).")
                game_state.character.gain_experience(5, 'command')
                input("\nPress Enter to continue...")
                continue
                
            elif action == 4:  # Raise shields
                engineering = game_state.character.attributes['engineering']
                
                # Apply engineering officer bonus to shield restoration
                eng_bonus = game_state.ship.get_crew_bonus('engineering') / 100.0
                shield_restore = (game_state.ship.specs['shields'] * 0.2 + (engineering / 5)) * (1 + eng_bonus)
                game_state.ship.recharge_shields(shield_restore)
                ui.display_message(f"\nShields recharged by {shield_restore:.0f} points.")
                if eng_bonus > 0:
                    ui.display_message(f"(Engineering officer bonus: +{eng_bonus*100:.1f}%)")
                game_state.character.gain_experience(5, 'engineering')
                
            elif action == 5:  # Diplomacy
                diplomacy = game_state.character.attributes['diplomacy']
                
                # Apply communications officer bonus to diplomacy
                comm_bonus = game_state.ship.get_crew_bonus('communications') / 100.0
                success_chance = (diplomacy / 150) + (comm_bonus * 0.3)
                
                if random.random() < success_chance:
                    ui.display_message("\n✓ Enemy vessel is standing down!")
                    ui.display_message("Diplomatic resolution achieved.")
                    if comm_bonus > 0:
                        ui.display_message(f"(Communications officer aided negotiations: +{comm_bonus*30:.1f}%)")
                    game_state.character.gain_experience(30, 'diplomacy')
                    game_state.character.gain_reputation(25)  # Big bonus for diplomatic victory
                    ui.display_message("Reputation gained: +25 (Diplomatic Victory)")
                    game_state.diplomatic_victories += 1
                    game_state.add_log_entry("Combat resolved through diplomacy.")
                    input("\nPress Enter to continue...")
                    return
                else:
                    ui.display_message("\n✗ Enemy is not responding to hails.")
                    game_state.character.gain_experience(5, 'diplomacy')
                    
            elif action == 6:  # Retreat
                command = game_state.character.attributes['command']
                escape_chance = 0.4 + (command / 200)
                
                if random.random() < escape_chance:
                    ui.display_message("\n✓ Successfully disengaged from combat!")
                    game_state.add_log_entry("Retreated from combat engagement.")
                    input("\nPress Enter to continue...")
                    return
                else:
                    ui.display_message("\n✗ Unable to break off! Enemy is pursuing!")
            else:
                ui.display_message("Invalid action.")
                continue
                
        except ValueError:
            ui.display_message("Invalid input.")
            continue
            
        # Check if enemy destroyed
        if enemy.is_destroyed():
            ui.display_message(f"\n✓ Enemy {enemy.ship_type} destroyed!")
            game_state.character.gain_experience(40, 'tactical')
            
            # Reputation bonus for combat victories
            rep_bonus = {'Scout': 5, 'Frigate': 10, 'Cruiser': 20, 'Battleship': 30, 'Dreadnought': 50}
            rep_gain = rep_bonus.get(enemy.ship_type, 10)
            game_state.character.gain_reputation(rep_gain)
            ui.display_message(f"Reputation gained: +{rep_gain}")
            
            # Display combat aftermath
            if game_state.ship.casualties_this_combat > 0:
                ui.display_message(f"\n⚠ CASUALTIES: {game_state.ship.casualties_this_combat} crew members lost")
                ui.display_message(f"   Remaining crew: {game_state.ship.crew_count}/{game_state.ship.max_crew}")
            
            # Display system damage
            damaged_systems = [s for s, v in game_state.ship.systems.items() if v < 100]
            if damaged_systems:
                ui.display_message(f"\n⚠ SYSTEMS DAMAGED:")
                for system in damaged_systems:
                    ui.display_message(f"   {system.title()}: {game_state.ship.systems[system]}%")
            
            game_state.enemies_defeated += 1
            game_state.modify_faction_relation(enemy.faction, -5)
            game_state.add_log_entry(f"Destroyed {enemy.faction} {enemy.ship_type} in combat. {game_state.ship.casualties_this_combat} casualties.")
            
            # Reset casualties counter for next combat
            game_state.ship.casualties_this_combat = 0
            
            input("\nPress Enter to continue...")
            return
            
        # Enemy attacks (unless player used evasive maneuvers)
        if action != 3:
            enemy_damage, weapon_type = enemy.attack()
            game_state.ship.take_damage(enemy_damage, 'shields', weapon_type)
            weapon_name = "Phaser fire" if weapon_type == 'phaser' else "Torpedo"
            ui.display_message(f"\nEnemy {weapon_name}! Your ship took {enemy_damage:.0f} damage.")
            
        # Check if player destroyed
        if game_state.ship.is_destroyed():
            ui.display_header("SHIP DESTROYED")
            ui.display_message("\nYour ship has been destroyed.")
            ui.display_message("All hands lost.")
            ui.display_message("\nGAME OVER")
            input("\nPress Enter to exit...")
            import sys
            sys.exit(0)
            
        input("\nPress Enter to continue...")
