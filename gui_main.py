"""
Main GUI Application - Star Trek: Federation Command

Pygame-based graphical interface featuring:
- LCARS-themed UI (Library Computer Access/Retrieval System)
- Multiple theme options (LCARS V1 classic, LCARS V2 modern)
- Fullscreen mode with dynamic screen size adaptation
- Screen management system for navigation between game states
- Event handling and game loop coordination

Manages these screens:
- MainMenuScreen: Start menu with New Game, Combat Test, Exit options
- OptionsScreen: Settings and interface customization
- CharacterCreationScreen: Create your captain with species and background
- GalaxyMapScreen: Explore the galaxy and manage your ship
- CombatTestScreen: Hex-based tactical combat arena for testing

The application uses a screen-based architecture where each screen
is responsible for its own drawing, event handling, and updates.
"""
import pygame
import sys
from gui.lcars_theme import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LCARS_COLORS, load_theme_preference
from gui.main_menu import MainMenuScreen
from gui.options_screen import OptionsScreen
from gui.character_creation import CharacterCreationScreen
from gui.galaxy_map_screen import GalaxyMapScreen


class StarTrekGUI:
    """
    Main GUI Application Controller
    
    Manages the game window, screens, and main game loop.
    Handles transitions between different game states.
    """
    
    def __init__(self):
        pygame.init()
        
        # Load theme preference before creating any screens
        load_theme_preference()
        
        # Set up display - fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Star Trek: Federation Command")
        
        # Get actual screen size
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Set icon (placeholder - can add ship icon later)
        # icon = pygame.image.load('assets/icon.png')
        # pygame.display.set_icon(icon)
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Screen management
        self.current_screen = None
        self.screens = {}
        
        # Initialize screens
        self._init_screens()
        
        # Start with main menu
        self.change_screen("main_menu")
        
    def _init_screens(self):
        """Initialize all game screens"""
        # Game state (shared across screens)
        self.game_state = {}
        
        self.screens['main_menu'] = MainMenuScreen(self.screen)
        self.screens['options'] = OptionsScreen(self.screen)
        self.screens['character_creation'] = CharacterCreationScreen(self.screen)
        self.screens['galaxy_map'] = GalaxyMapScreen(self.screen, self.game_state)
        
        # Combat test screen
        from gui.combat_test_screen import CombatTestScreen
        self.screens['combat_test'] = CombatTestScreen(self.screen)
        
    def change_screen(self, screen_name):
        """Change to a different screen"""
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]
            self.current_screen.next_screen = None
        else:
            print(f"Screen '{screen_name}' not found!")
            
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS)
            
            # Get events
            events = pygame.event.get()
            
            # Handle events
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # Update current screen
            if self.current_screen:
                self.current_screen.handle_events(events)
                self.current_screen.update(dt)
                self.current_screen.draw()
                
                # Check for screen transitions
                if self.current_screen.next_screen:
                    next_screen = self.current_screen.next_screen
                    
                    if next_screen == "game":
                        # Start actual game with character data
                        self.start_game()
                    else:
                        self.change_screen(next_screen)
            
        pygame.quit()
        sys.exit()
        
    def start_game(self):
        """Start the main game with created character"""
        from game.character import Character
        from game.ships import create_starting_ship
        from game.galaxy import Galaxy
        from game.game_state import GameState
        
        # Get character data from character creation screen
        char_screen = self.screens['character_creation']
        char_data = char_screen.character_data
        
        print("\n=== STARTING GAME ===")
        print(f"Name: {char_data['name']}")
        print(f"Species: {char_data['species']}")
        print(f"Tactical: {char_data['tactical']}")
        print(f"Science: {char_data['science']}")
        print(f"Engineering: {char_data['engineering']}")
        print(f"Diplomacy: {char_data['diplomacy']}")
        print(f"Command: {char_data['command']}")
        
        # Create proper Character object
        # Note: Character class calculates skills from species + background
        # GUI character creation provides pre-calculated values, so we need to use from_dict
        character = Character(
            name=char_data['name'],
            species=char_data['species'],
            background=char_data.get('background', 'Command School')  # Default if not in data
        )
        
        # Override with GUI-calculated values if provided
        if 'tactical' in char_data:
            character.attributes['tactical'] = char_data['tactical']
            character.attributes['science'] = char_data['science']
            character.attributes['engineering'] = char_data['engineering']
            character.attributes['diplomacy'] = char_data['diplomacy']
            character.attributes['command'] = char_data['command']
        
        # Create starting ship (Miranda-class with AdvancedShip system)
        ship = create_starting_ship(character.species)
        print(f"Assigned ship: USS {ship.name} ({ship.ship_class}-class)")
        
        # Generate galaxy
        galaxy = Galaxy()
        galaxy.generate()
        print(f"Galaxy generated with {len(galaxy.systems)} systems")
        
        # Create game state
        game_state = GameState(character, ship, galaxy)
        
        # Store in GUI game state
        self.game_state['character'] = character
        self.game_state['ship'] = ship
        self.game_state['galaxy'] = galaxy
        self.game_state['game_state'] = game_state
        
        print("=== GAME INITIALIZED ===\n")
        
        # Go to galaxy map
        self.change_screen("galaxy_map")


def main():
    """Entry point for GUI version"""
    app = StarTrekGUI()
    app.run()


if __name__ == '__main__':
    main()
