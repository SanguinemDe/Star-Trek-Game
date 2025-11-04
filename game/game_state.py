"""
Game State Management
Handles the overall game state, saving, and loading
"""

import json
import os
from datetime import datetime

class GameState:
    """Manages the overall game state"""
    
    def __init__(self, character, ship, galaxy):
        self.character = character
        self.ship = ship
        self.galaxy = galaxy
        self.stardate = 2380.0  # Start in year 2380
        self.turn = 0
        self.captain_log = []
        self.discovered_systems = set()
        self.faction_relations = {
            'Federation': 100,
            'Klingon Empire': 50,
            'Romulan Star Empire': 30,
            'Cardassian Union': 40,
            'Ferengi Alliance': 60,
            'Borg Collective': -100,
            'Dominion': 20
        }
        self.missions_completed = 0
        self.enemies_defeated = 0
        self.systems_explored = 0
        self.diplomatic_victories = 0
        
    def advance_time(self, days=1):
        """Advance the stardate"""
        self.stardate += days / 365.0
        self.turn += 1
        
    def add_log_entry(self, entry):
        """Add an entry to the captain's log"""
        log = {
            'stardate': self.stardate,
            'turn': self.turn,
            'entry': entry,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.captain_log.append(log)
        
    def modify_faction_relation(self, faction, change):
        """Modify relationship with a faction"""
        if faction in self.faction_relations:
            self.faction_relations[faction] = max(-100, min(100, 
                self.faction_relations[faction] + change))
            
    def get_faction_status(self, faction):
        """Get the relationship status with a faction"""
        if faction not in self.faction_relations:
            return "Unknown"
        
        relation = self.faction_relations[faction]
        if relation >= 80:
            return "Allied"
        elif relation >= 50:
            return "Friendly"
        elif relation >= 20:
            return "Neutral"
        elif relation >= -20:
            return "Unfriendly"
        elif relation >= -50:
            return "Hostile"
        else:
            return "At War"
            
    def save_game(self, filename="savegame.json"):
        """Save the game state to a file"""
        save_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
        os.makedirs(save_dir, exist_ok=True)
        
        save_path = os.path.join(save_dir, filename)
        
        save_data = {
            'version': '0.1.0',
            'character': self.character.to_dict(),
            'ship': self.ship.to_dict(),
            'galaxy': self.galaxy.to_dict(),
            'stardate': self.stardate,
            'turn': self.turn,
            'captain_log': self.captain_log,
            'discovered_systems': list(self.discovered_systems),
            'faction_relations': self.faction_relations,
            'missions_completed': self.missions_completed,
            'enemies_defeated': self.enemies_defeated,
            'systems_explored': self.systems_explored,
            'diplomatic_victories': self.diplomatic_victories,
            'mission_board': self.mission_board.to_dict() if hasattr(self, 'mission_board') else None,
            'recruitment_pool': self.recruitment_pool.to_dict() if hasattr(self, 'recruitment_pool') else None
        }
        
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
            
        return True
        
    @classmethod
    def load_game(cls, ui, filename="savegame.json"):
        """Load a game state from a file"""
        save_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
        save_path = os.path.join(save_dir, filename)
        
        if not os.path.exists(save_path):
            return None
            
        try:
            with open(save_path, 'r') as f:
                save_data = json.load(f)
                
            from game.character import Character
            from game.advanced_ship import AdvancedShip
            from game.galaxy import Galaxy
            
            character = Character.from_dict(save_data['character'])
            ship = AdvancedShip.from_dict(save_data['ship'])
            galaxy = Galaxy.from_dict(save_data['galaxy'])
            
            game_state = cls(character, ship, galaxy)
            game_state.stardate = save_data['stardate']
            game_state.turn = save_data['turn']
            game_state.captain_log = save_data['captain_log']
            game_state.discovered_systems = set(save_data['discovered_systems'])
            game_state.faction_relations = save_data['faction_relations']
            game_state.missions_completed = save_data['missions_completed']
            game_state.enemies_defeated = save_data['enemies_defeated']
            game_state.systems_explored = save_data['systems_explored']
            game_state.diplomatic_victories = save_data['diplomatic_victories']
            
            # Load mission board if present
            if save_data.get('mission_board'):
                from game.missions import MissionBoard
                game_state.mission_board = MissionBoard.from_dict(save_data['mission_board'])
            
            # Load recruitment pool if present
            if save_data.get('recruitment_pool'):
                from game.crew_recruitment import RecruitmentPool
                game_state.recruitment_pool = RecruitmentPool.from_dict(save_data['recruitment_pool'])
            
            return game_state
        except Exception as e:
            ui.display_message(f"Error loading game: {e}")
            return None
