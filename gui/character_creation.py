"""
Character Creation Screen
Create player character with name, attributes, and customization
"""
import pygame
from gui.lcars_theme import LCARS_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_LARGE, FONT_MEDIUM, FONT_SMALL
from gui.components import Button, Panel, TextInput, Slider, RadioButtonList


class CharacterCreationScreen:
    """Character creation screen with LCARS styling"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        
        # Character data
        self.character_data = {
            'name': '',
            'species': 'Human',
            'tactical': 50,
            'science': 50,
            'engineering': 50,
            'diplomacy': 50,
            'command': 50,
        }
        
        self.total_points = 250
        self.points_spent = 250
        self.next_screen = None
        self.last_selected_species = 0  # Track species changes
        
        # Create UI elements
        self._create_ui()
        
    def _create_ui(self):
        """Create character creation UI"""
        # Panels
        self.header_panel = Panel(0, 0, self.screen_width, 80, color='bg_dark', 
                                 border_color='orange')
        self.left_panel = Panel(50, 100, 500, 580, color='bg_medium', 
                               border_color='blue')
        self.right_panel = Panel(580, 100, 650, 580, color='bg_medium', 
                                border_color='purple')
        
        # Name input
        self.name_input = TextInput(80, 125, 440, 45, placeholder="Enter Your Name")
        
        # Species radio buttons - all 10 Federation races
        species_list = ['Human', 'Vulcan', 'Andorian', 'Tellarite', 'Betazoid', 
                       'Trill', 'Bajoran', 'Caitian', 'Bolian', 'Klingon']
        self.species_radio = RadioButtonList(80, 200, 200, 35, species_list)
        
        # Attribute sliders
        slider_x = 300
        slider_y = 230
        slider_spacing = 58
        slider_width = 230
        
        self.sliders = {
            'tactical': Slider(slider_x, slider_y, slider_width, 20, 80, 50, 
                              "Tactical"),
            'science': Slider(slider_x, slider_y + slider_spacing, slider_width, 
                             20, 80, 50, "Science"),
            'engineering': Slider(slider_x, slider_y + slider_spacing * 2, slider_width, 
                                 20, 80, 50, "Engineering"),
            'diplomacy': Slider(slider_x, slider_y + slider_spacing * 3, slider_width, 
                               20, 80, 50, "Diplomacy"),
            'command': Slider(slider_x, slider_y + slider_spacing * 4, slider_width, 
                             20, 80, 50, "Command"),
        }
        
        # Buttons
        self.back_button = Button(80, 625, 180, 50, "BACK", color='red', 
                                 callback=self.go_back)
        self.create_button = Button(330, 625, 180, 50, "CREATE", color='green', 
                                   callback=self.create_character)
        
    def go_back(self):
        """Return to main menu"""
        self.next_screen = "main_menu"
        
    def create_character(self):
        """Create character and start game"""
        # Validate name
        if not self.name_input.text.strip():
            print("Please enter a name")
            return
            
        # Update character data
        self.character_data['name'] = self.name_input.text.strip()
        self.character_data['species'] = self.species_radio.options[
            self.species_radio.selected_index]
        
        for attr_name, slider in self.sliders.items():
            self.character_data[attr_name] = slider.value
            
        # Move to game
        self.next_screen = "game"
        
    def _calculate_points(self):
        """Calculate total points spent"""
        total = sum(slider.value for slider in self.sliders.values())
        return total
        
    def _apply_species_bonuses(self):
        """Apply species bonuses to attributes"""
        # Reset all sliders to base 50
        for slider in self.sliders.values():
            slider.value = 50
            slider.handle_x = slider._value_to_x(50)
        
        # Species bonuses (+10 to two attributes)
        bonuses = {
            'Human': {},  # No bonuses, balanced
            'Vulcan': {'science': 10, 'command': 10},
            'Andorian': {'tactical': 10, 'command': 10},
            'Tellarite': {'engineering': 10, 'diplomacy': 10},
            'Betazoid': {'diplomacy': 10, 'science': 10},
            'Trill': {'science': 10, 'diplomacy': 10},
            'Bajoran': {'diplomacy': 10, 'tactical': 10},
            'Caitian': {'tactical': 10, 'science': 10},
            'Bolian': {'diplomacy': 10, 'engineering': 10},
            'Klingon': {'tactical': 10, 'engineering': 10},
        }
        
        species = self.species_radio.options[self.species_radio.selected_index]
        species_bonuses = bonuses.get(species, {})
        
        for attr, bonus in species_bonuses.items():
            if attr in self.sliders:
                self.sliders[attr].value = 50 + bonus
                self.sliders[attr].handle_x = self.sliders[attr]._value_to_x(self.sliders[attr].value)
    
    def _get_species_description(self):
        """Get description for selected species"""
        descriptions = {
            'Human': "Versatile and adaptable. Balanced in all areas.",
            'Vulcan': "Logical and analytical. +Science, +Command",
            'Andorian': "Warriors and explorers. +Tactical, +Command",
            'Tellarite': "Skilled engineers and negotiators. +Engineering, +Diplomacy",
            'Betazoid': "Empathic diplomats. +Diplomacy, +Science",
            'Trill': "Joined symbionts with vast experience. +Science, +Diplomacy",
            'Bajoran': "Spiritual and resilient. +Diplomacy, +Tactical",
            'Caitian': "Agile hunters. +Tactical, +Science",
            'Bolian': "Friendly and social. +Diplomacy, +Engineering",
            'Klingon': "Honorable warriors. +Tactical, +Engineering",
        }
        species = self.species_radio.options[self.species_radio.selected_index]
        return descriptions.get(species, "")
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()
                    
            # Pass events to UI components
            self.name_input.handle_event(event)
            self.species_radio.handle_event(event)
            self.back_button.handle_event(event)
            self.create_button.handle_event(event)
            
            for slider in self.sliders.values():
                slider.handle_event(event)
                
    def update(self, dt):
        """Update screen state"""
        self.name_input.update(dt)
        self.points_spent = self._calculate_points()
        
        # Check if species changed and apply bonuses
        if self.species_radio.selected_index != self.last_selected_species:
            self._apply_species_bonuses()
            self.last_selected_species = self.species_radio.selected_index
        
    def draw(self):
        """Draw the character creation screen"""
        # Background
        self.screen.fill(LCARS_COLORS['bg_dark'])
        
        # Draw panels
        self.header_panel.draw(self.screen)
        self.left_panel.draw(self.screen)
        self.right_panel.draw(self.screen)
        
        # Header
        title_surface = self.font_large.render("CHARACTER CREATION", True, 
                                               LCARS_COLORS['orange'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Left panel - Character details
        # Name label
        name_label = self.font_small.render("NAME:", True, LCARS_COLORS['text_white'])
        self.screen.blit(name_label, (80, 105))
        self.name_input.draw(self.screen, self.font_small)
        
        # Species label
        species_label = self.font_small.render("SPECIES:", True, LCARS_COLORS['text_white'])
        self.screen.blit(species_label, (80, 180))
        
        # Draw species radio buttons
        self.species_radio.draw(self.screen, self.font_small)
        
        # Attributes label  
        attributes_label = self.font_small.render("ATTRIBUTES", True, 
                                                   LCARS_COLORS['light_blue'])
        self.screen.blit(attributes_label, (300, 180))
        
        # Draw sliders
        for slider in self.sliders.values():
            slider.draw(self.screen, self.font_small)
            
        # Points display
        points_color = LCARS_COLORS['green'] if self.points_spent <= self.total_points else LCARS_COLORS['alert_red']
        points_text = f"Total: {self.points_spent}/{self.total_points}"
        points_surface = self.font_small.render(points_text, True, points_color)
        self.screen.blit(points_surface, (375, 600))
        
        # Draw buttons
        self.back_button.draw(self.screen, self.font_small)
        self.create_button.draw(self.screen, self.font_small)
        
        # Right panel - Preview and info
        preview_title = self.font_medium.render("PREVIEW", True, LCARS_COLORS['purple'])
        self.screen.blit(preview_title, (620, 120))
        
        # Character name
        display_name = self.name_input.text if self.name_input.text else "Unnamed Officer"
        name_surface = self.font_medium.render(display_name, True, LCARS_COLORS['text_white'])
        self.screen.blit(name_surface, (620, 170))
        
        # Species
        species = self.species_radio.options[self.species_radio.selected_index]
        species_surface = self.font_small.render(f"Species: {species}", True, 
                                                LCARS_COLORS['text_gray'])
        self.screen.blit(species_surface, (620, 210))
        
        # Species description
        description = self._get_species_description()
        desc_surface = self.font_small.render(description, True, LCARS_COLORS['text_dim'])
        self.screen.blit(desc_surface, (620, 240))
        
        # Attributes summary
        attr_y = 300
        attr_title = self.font_small.render("ATTRIBUTE SUMMARY:", True, 
                                           LCARS_COLORS['light_blue'])
        self.screen.blit(attr_title, (620, attr_y))
        
        attr_y += 40
        for attr_name, slider in self.sliders.items():
            # Draw attribute bar
            bar_width = 200
            bar_height = 20
            bar_x = 620
            bar_y = attr_y
            
            # Background bar
            bar_rect = pygame.Rect(bar_x + 150, bar_y, bar_width, bar_height)
            pygame.draw.rect(self.screen, LCARS_COLORS['bg_dark'], bar_rect, 
                           border_radius=5)
            
            # Filled bar
            fill_width = int((slider.value / 80) * bar_width)
            fill_rect = pygame.Rect(bar_x + 150, bar_y, fill_width, bar_height)
            
            # Color based on value
            if slider.value >= 70:
                bar_color = LCARS_COLORS['green']
            elif slider.value >= 50:
                bar_color = LCARS_COLORS['orange']
            else:
                bar_color = LCARS_COLORS['red']
                
            pygame.draw.rect(self.screen, bar_color, fill_rect, border_radius=5)
            
            # Attribute name and value
            attr_text = f"{attr_name.capitalize()}:"
            text_surface = self.font_small.render(attr_text, True, 
                                                 LCARS_COLORS['text_white'])
            self.screen.blit(text_surface, (bar_x, bar_y))
            
            value_surface = self.font_small.render(str(slider.value), True, 
                                                   LCARS_COLORS['text_white'])
            self.screen.blit(value_surface, (bar_x + 380, bar_y))
            
            attr_y += 40
            
        # Tips
        tips_y = 520
        tips_title = self.font_small.render("TIPS:", True, LCARS_COLORS['yellow'])
        self.screen.blit(tips_title, (620, tips_y))
        
        tips = [
            "• Tactical: Combat effectiveness",
            "• Science: Anomaly investigation",
            "• Engineering: Ship repairs & power",
            "• Diplomacy: Negotiations & morale",
            "• Command: Leadership & tactics",
        ]
        
        tips_y += 30
        for tip in tips:
            tip_surface = pygame.font.Font(None, 18).render(tip, True, 
                                                           LCARS_COLORS['text_dim'])
            self.screen.blit(tip_surface, (620, tips_y))
            tips_y += 22
        
        pygame.display.flip()
