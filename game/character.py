"""
Character Creation and Management
"""

import random

class Character:
    """Represents the player character (Captain)"""
    
    SPECIES = {
        'Human': {'command': 0, 'tactical': 0, 'science': 0, 'engineering': 0, 'diplomacy': 5},
        'Vulcan': {'command': 0, 'tactical': 0, 'science': 10, 'engineering': 5, 'diplomacy': 5},
        'Andorian': {'command': 5, 'tactical': 10, 'science': 0, 'engineering': 0, 'diplomacy': -5},
        'Tellarite': {'command': 0, 'tactical': 0, 'science': 0, 'engineering': 10, 'diplomacy': 0},
        'Betazoid': {'command': 0, 'tactical': 0, 'science': 5, 'engineering': 0, 'diplomacy': 10},
        'Trill': {'command': 5, 'tactical': 0, 'science': 5, 'engineering': 0, 'diplomacy': 5},
        'Bajoran': {'command': 0, 'tactical': 5, 'science': 0, 'engineering': 5, 'diplomacy': 0},
        'Klingon': {'command': 5, 'tactical': 15, 'science': -5, 'engineering': 0, 'diplomacy': -10},
        'Caitian': {'command': 0, 'tactical': 10, 'science': 5, 'engineering': 0, 'diplomacy': 0}
    }
    
    BACKGROUNDS = {
        'Command School': {'command': 15, 'tactical': 5, 'science': 0, 'engineering': 0, 'diplomacy': 5},
        'Security/Tactical': {'command': 5, 'tactical': 15, 'science': 0, 'engineering': 5, 'diplomacy': 0},
        'Sciences Division': {'command': 0, 'tactical': 0, 'science': 15, 'engineering': 5, 'diplomacy': 5},
        'Engineering Corps': {'command': 0, 'tactical': 5, 'science': 5, 'engineering': 15, 'diplomacy': 0},
        'Diplomatic Corps': {'command': 5, 'tactical': 0, 'science': 5, 'engineering': 0, 'diplomacy': 15}
    }
    
    RANKS = [
        'Ensign', 'Lieutenant Junior Grade', 'Lieutenant', 'Lieutenant Commander',
        'Commander', 'Captain', 'Fleet Captain', 'Commodore', 'Rear Admiral',
        'Vice Admiral', 'Admiral', 'Fleet Admiral'
    ]
    
    def __init__(self, name, species, background):
        self.name = name
        self.species = species
        self.background = background
        self.rank = 'Lieutenant Commander'  # Starting rank
        self.rank_level = 3
        
        # Base attributes (0-100 scale)
        self.attributes = {
            'command': 50,
            'tactical': 50,
            'science': 50,
            'engineering': 50,
            'diplomacy': 50
        }
        
        # Apply species bonuses
        for attr, bonus in self.SPECIES[species].items():
            self.attributes[attr] += bonus
            
        # Apply background bonuses
        for attr, bonus in self.BACKGROUNDS[background].items():
            self.attributes[attr] += bonus
            
        # Ensure attributes stay in valid range
        for attr in self.attributes:
            self.attributes[attr] = max(0, min(100, self.attributes[attr]))
            
        self.experience = 0
        self.reputation = 0  # Reputation points for ship purchases
        self.commendations = []
        self.traits = []
        
    def gain_experience(self, amount, category=None):
        """Gain experience and possibly level up attributes"""
        self.experience += amount
        
        # Also gain reputation (50% of experience as reputation)
        rep_gain = int(amount * 0.5)
        self.reputation += rep_gain
        
        if category and category in self.attributes:
            # Small chance to increase specific attribute
            if random.random() < 0.1:
                self.attributes[category] = min(100, self.attributes[category] + 1)
                
        # Check for rank promotion
        ranks_needed = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500, 7500, 10000]
        for i, exp_needed in enumerate(ranks_needed):
            if self.experience >= exp_needed and i > self.rank_level:
                self.rank_level = i
                self.rank = self.RANKS[i]
                return True  # Promoted
        return False
    
    def gain_reputation(self, amount):
        """Gain reputation points"""
        self.reputation += amount
        
    def add_commendation(self, commendation):
        """Add a commendation to the character's record"""
        self.commendations.append(commendation)
        
    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'species': self.species,
            'background': self.background,
            'rank': self.rank,
            'rank_level': self.rank_level,
            'attributes': self.attributes,
            'experience': self.experience,
            'reputation': self.reputation,
            'commendations': self.commendations,
            'traits': self.traits
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create character from dictionary"""
        char = cls(data['name'], data['species'], data['background'])
        char.rank = data['rank']
        char.rank_level = data['rank_level']
        char.attributes = data['attributes']
        char.experience = data['experience']
        char.reputation = data.get('reputation', 0)  # Backwards compatibility
        char.commendations = data['commendations']
        char.traits = data['traits']
        return char


class CharacterCreation:
    """Handles the character creation process"""
    
    @staticmethod
    def create_character(ui):
        """Guide player through character creation"""
        ui.display_header("CHARACTER CREATION")
        
        # Name
        name = ui.get_input("\nEnter your character's name: ")
        while not name or len(name) < 2:
            ui.display_message("Please enter a valid name (at least 2 characters)")
            name = ui.get_input("Enter your character's name: ")
            
        # Species
        ui.display_message("\n=== SPECIES SELECTION ===")
        species_list = list(Character.SPECIES.keys())
        for i, species in enumerate(species_list, 1):
            bonuses = Character.SPECIES[species]
            bonus_str = ", ".join([f"{k.title()}: +{v}" for k, v in bonuses.items() if v != 0])
            ui.display_message(f"{i}. {species} ({bonus_str})")
            
        species_choice = ui.get_choice(f"\nSelect species (1-{len(species_list)}): ", 
                                       list(range(1, len(species_list) + 1)))
        species = species_list[species_choice - 1]
        
        # Background
        ui.display_message("\n=== BACKGROUND SELECTION ===")
        background_list = list(Character.BACKGROUNDS.keys())
        for i, background in enumerate(background_list, 1):
            bonuses = Character.BACKGROUNDS[background]
            bonus_str = ", ".join([f"{k.title()}: +{v}" for k, v in bonuses.items() if v != 0])
            ui.display_message(f"{i}. {background} ({bonus_str})")
            
        background_choice = ui.get_choice(f"\nSelect background (1-{len(background_list)}): ",
                                          list(range(1, len(background_list) + 1)))
        background = background_list[background_choice - 1]
        
        # Create character
        character = Character(name, species, background)
        
        # Display summary
        ui.display_message("\n=== CHARACTER SUMMARY ===")
        ui.display_message(f"Name: {character.name}")
        ui.display_message(f"Species: {character.species}")
        ui.display_message(f"Background: {character.background}")
        ui.display_message(f"Rank: {character.rank}")
        ui.display_message("\nAttributes:")
        for attr, value in character.attributes.items():
            ui.display_message(f"  {attr.title()}: {value}")
            
        confirm = ui.confirm("\nConfirm character creation?")
        if not confirm:
            return CharacterCreation.create_character(ui)
            
        return character
