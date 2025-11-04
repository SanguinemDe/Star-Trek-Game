"""
Options Screen
Settings and configuration interface
"""
import pygame
import json
import os
from gui.lcars_theme import LCARS_COLORS, get_current_theme, set_theme, AVAILABLE_THEMES, get_font
from gui.components import Button, Panel


class OptionsScreen:
    """Options menu for game settings"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Fonts
        self.font_large = get_font(48, bold=True)
        self.font_medium = get_font(32, bold=True)
        self.font_small = get_font(24)
        
        # State
        self.next_screen = None
        self.current_theme = get_current_theme()
        
        # Create UI
        self._create_ui()
        
    def _create_ui(self):
        """Create options UI elements"""
        # Back button
        self.back_button = Button(
            50, 50, 150, 50,
            "< BACK", color='orange',
            callback=self.go_back
        )
        
        # Theme selection buttons
        button_width = 400
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        start_y = 250
        spacing = 80
        
        self.theme_buttons = []
        for i, theme_name in enumerate(AVAILABLE_THEMES):
            button = Button(
                button_x, start_y + (i * spacing),
                button_width, button_height,
                f"INTERFACE: {theme_name.upper()}",
                color='blue',
                callback=lambda t=theme_name: self.select_theme(t)
            )
            self.theme_buttons.append(button)
        
        # Update current theme button appearance
        self._update_theme_buttons()
        
    def _update_theme_buttons(self):
        """Update theme button colors to show selection"""
        for button in self.theme_buttons:
            theme_name = button.text.replace("INTERFACE: ", "").lower()
            if theme_name == self.current_theme:
                button.color = LCARS_COLORS['green']
                button.text_color = LCARS_COLORS['black']
            else:
                button.color = LCARS_COLORS['blue']
                button.text_color = LCARS_COLORS['black']
    
    def select_theme(self, theme_name):
        """Change the interface theme"""
        set_theme(theme_name)
        self.current_theme = theme_name
        self._update_theme_buttons()
        
        # Save preference
        self._save_settings()
        
        print(f"Theme changed to: {theme_name}")
    
    def _save_settings(self):
        """Save settings to file"""
        settings = {
            'theme': self.current_theme
        }
        
        try:
            os.makedirs('settings', exist_ok=True)
            with open('settings/options.json', 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def go_back(self):
        """Return to main menu"""
        self.next_screen = "main_menu"
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()
            
            # Handle back button
            self.back_button.handle_event(event)
            
            # Handle theme buttons
            for button in self.theme_buttons:
                button.handle_event(event)
    
    def update(self, dt):
        """Update screen state"""
        pass
    
    def draw(self):
        """Draw the options screen"""
        # Background
        self.screen.fill(LCARS_COLORS['bg_dark'])
        
        # Title
        title_text = "OPTIONS"
        title_surface = self.font_large.render(title_text, True, LCARS_COLORS['orange'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Section header
        section_text = "INTERFACE STYLE"
        section_surface = self.font_medium.render(section_text, True, LCARS_COLORS['light_blue'])
        section_rect = section_surface.get_rect(center=(self.screen_width // 2, 180))
        self.screen.blit(section_surface, section_rect)
        
        # Draw back button
        self.back_button.draw(self.screen, self.font_small)
        
        # Draw theme buttons
        for button in self.theme_buttons:
            button.draw(self.screen, self.font_medium)
        
        # Draw theme preview info
        preview_y = 250 + (len(self.theme_buttons) * 80) + 40
        if self.current_theme == 'lcars_v1':
            preview_text = "Classic LCARS style with rounded corners and warm colors"
        else:
            preview_text = "Modern LCARS style with angular elements and cool tones"
        
        preview_surface = self.font_small.render(preview_text, True, LCARS_COLORS['text_gray'])
        preview_rect = preview_surface.get_rect(center=(self.screen_width // 2, preview_y))
        self.screen.blit(preview_surface, preview_rect)
        
        pygame.display.flip()
