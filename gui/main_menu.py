"""
Main Menu Screen
Start screen with title and menu options
"""
import pygame
import sys
from gui.lcars_theme import LCARS_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_LARGE, FONT_MEDIUM, get_font
from gui.components import Button, Panel


class MainMenuScreen:
    """Main menu screen with LCARS styling"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_large = get_font(FONT_LARGE, bold=True)
        self.font_medium = get_font(FONT_MEDIUM, bold=True)
        
        # State
        self.next_screen = None
        
        # Create UI elements
        self._create_ui()
        
    def _create_ui(self):
        """Create menu buttons and panels"""
        # Background panels for LCARS aesthetic
        self.top_panel = Panel(0, 0, self.screen_width, 100, color='bg_dark', 
                              border_color='orange')
        self.side_panel = Panel(0, 100, 200, self.screen_height - 100, color='orange')
        
        # Title area
        self.title_text = "STAR TREK"
        self.subtitle_text = "Federation Command"
        
        # Menu buttons (centered)
        button_width = 400
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        start_y = 250
        spacing = 80
        
        self.buttons = [
            Button(button_x, start_y, button_width, button_height, 
                  "NEW GAME", color='orange', callback=self.new_game),
            Button(button_x, start_y + spacing, button_width, button_height, 
                  "LOAD GAME", color='blue', callback=self.load_game),
            Button(button_x, start_y + spacing * 2, button_width, button_height, 
                  "COMBAT TEST", color='green', callback=self.combat_test),
            Button(button_x, start_y + spacing * 3, button_width, button_height, 
                  "OPTIONS", color='purple', callback=self.options),
            Button(button_x, start_y + spacing * 4, button_width, button_height, 
                  "QUIT", color='red', callback=self.quit_game),
        ]
        
    def new_game(self):
        """Start new game - go to character creation"""
        self.next_screen = "character_creation"
        
    def load_game(self):
        """Load saved game"""
        print("Load game - not yet implemented")
        
    def combat_test(self):
        """Launch combat test arena"""
        self.next_screen = "combat_test"
        
    def options(self):
        """Show options menu"""
        self.next_screen = "options"
        
    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                    
            # Pass events to buttons
            for button in self.buttons:
                button.handle_event(event)
                
    def update(self, dt):
        """Update screen state"""
        pass
        
    def draw(self):
        """Draw the main menu"""
        # Background
        self.screen.fill(LCARS_COLORS['bg_dark'])
        
        # Draw panels
        self.top_panel.draw(self.screen)
        self.side_panel.draw(self.screen)
        
        # Draw title
        title_surface = self.font_large.render(self.title_text, True, 
                                               LCARS_COLORS['orange'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.font_medium.render(self.subtitle_text, True, 
                                                   LCARS_COLORS['light_blue'])
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw version info in corner
        version_text = "v1.0.0"
        version_surface = pygame.font.Font(None, 20).render(version_text, True, 
                                                            LCARS_COLORS['text_dim'])
        self.screen.blit(version_surface, (self.screen_width - 80, self.screen_height - 30))
        
        # Draw stardate
        import time
        stardate = 41000 + (time.time() % 100000) / 100
        stardate_text = f"Stardate: {stardate:.1f}"
        stardate_surface = pygame.font.Font(None, 24).render(stardate_text, True, 
                                                             LCARS_COLORS['text_gray'])
        self.screen.blit(stardate_surface, (220, 20))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.font_medium)
            
        pygame.display.flip()
