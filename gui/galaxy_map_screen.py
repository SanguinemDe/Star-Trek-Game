"""
Galaxy Map Screen
Interactive hex-based star map with LCARS interface
"""
import pygame
from gui.lcars_theme import LCARS_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_LARGE, FONT_MEDIUM, FONT_SMALL
from gui.components import Button, Panel
from gui.hex_map import HexMap
from gui.galaxy_data import create_star_trek_galaxy, get_faction_boundaries


class GalaxyMapScreen:
    """Galaxy map screen with hex navigation"""
    
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Get actual screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Hex map with zoom support
        self.hex_map = HexMap(hex_size=25)
        self.zoom_level = 1.0
        self.min_zoom = 0.3
        self.max_zoom = 3.0
        
        # Center on Sol system initially
        map_width = self.screen_width - 640
        map_height = self.screen_height - 70
        self.hex_map.offset_x = map_width // 2
        self.hex_map.offset_y = map_height // 2
        
        # Load galaxy
        self.systems = create_star_trek_galaxy()
        self.boundaries = get_faction_boundaries()
        
        # Add systems to hex map
        for system in self.systems:
            self.hex_map.add_system(system.q, system.r, system.name, system)
        
        # Selected system
        self.selected_system = None
        self.current_system = self.hex_map.get_system_at(0, 0)['data']  # Start at Sol
        
        # Camera control
        self.dragging = False
        self.drag_start = (0, 0)
        
        # State
        self.next_screen = None
        
        # UI Elements
        self._create_ui()
        
    def _create_ui(self):
        """Create UI panels and buttons"""
        # Top panel
        self.top_panel = Panel(0, 0, self.screen_width, 60, color='bg_dark', 
                              border_color='orange')
        
        # Left info panel
        self.info_panel = Panel(10, 70, 300, self.screen_height - 80, color='bg_medium', 
                               border_color='blue')
        
        # Right control panel
        self.control_panel = Panel(self.screen_width - 310, 70, 300, self.screen_height - 80, 
                                  color='bg_medium', border_color='purple')
        
        # Buttons
        button_x = self.screen_width - 290
        button_y = 100
        button_spacing = 60
        
        self.scan_button = Button(button_x, button_y, 270, 50, 
                                  "SCAN SYSTEM", color='blue', callback=self.scan_system)
        self.navigate_button = Button(button_x, button_y + button_spacing, 270, 50, 
                                     "SET COURSE", color='orange', callback=self.set_course)
        self.dock_button = Button(button_x, button_y + button_spacing * 2, 270, 50, 
                                  "DOCK", color='green', callback=self.dock)
        self.ship_button = Button(button_x, button_y + button_spacing * 3, 270, 50, 
                                  "SHIP STATUS", color='purple', callback=self.ship_status)
        self.menu_button = Button(button_x, button_y + button_spacing * 4, 270, 50, 
                                  "MAIN MENU", color='red', callback=self.main_menu)
        
        self.buttons = [self.scan_button, self.navigate_button, self.dock_button, 
                       self.ship_button, self.menu_button]
        
    def scan_system(self):
        """Scan the selected system"""
        if self.selected_system:
            self.selected_system.explored = True
            print(f"Scanning {self.selected_system.name}...")
            
    def set_course(self):
        """Navigate to selected system"""
        if self.selected_system and self.current_system:
            distance = self.hex_map.hex_distance(
                self.current_system.q, self.current_system.r,
                self.selected_system.q, self.selected_system.r
            )
            print(f"Setting course to {self.selected_system.name} ({distance} LY)")
            # TODO: Implement travel mechanics
            
    def dock(self):
        """Dock at station"""
        if self.selected_system and self.selected_system.system_type == 'station':
            print(f"Docking at {self.selected_system.name}...")
            # TODO: Implement docking
            
    def ship_status(self):
        """Show ship status"""
        print("Ship status...")
        # TODO: Implement ship status screen
        
    def main_menu(self):
        """Return to main menu"""
        self.next_screen = "main_menu"
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main_menu()
                # Arrow keys for panning
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.hex_map.pan(0, 50)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.hex_map.pan(0, -50)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.hex_map.pan(50, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.hex_map.pan(-50, 0)
                # Zoom controls
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    old_zoom = self.zoom_level
                    self.zoom_level = min(self.max_zoom, self.zoom_level * 1.2)
                    if self.zoom_level != old_zoom:
                        self.hex_map.hex_size = int(25 * self.zoom_level)
                elif event.key == pygame.K_MINUS:
                    old_zoom = self.zoom_level
                    self.zoom_level = max(self.min_zoom, self.zoom_level / 1.2)
                    if self.zoom_level != old_zoom:
                        self.hex_map.hex_size = int(25 * self.zoom_level)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking on map area
                    if 320 < event.pos[0] < self.screen_width - 320:
                        # Adjust coordinates for map surface
                        map_x = event.pos[0] - 320
                        map_y = event.pos[1] - 70
                        
                        # Check for system selection
                        hex_coords = self.hex_map.pixel_to_hex(map_x, map_y)
                        system_data = self.hex_map.get_system_at(hex_coords[0], hex_coords[1])
                        if system_data:
                            self.selected_system = system_data['data']
                        else:
                            # Start dragging
                            self.dragging = True
                            self.drag_start = event.pos
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    dx = event.pos[0] - self.drag_start[0]
                    dy = event.pos[1] - self.drag_start[1]
                    self.hex_map.pan(dx, dy)
                    self.drag_start = event.pos
                    
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom with mouse wheel
                old_zoom = self.zoom_level
                if event.y > 0:  # Scroll up - zoom in
                    self.zoom_level = min(self.max_zoom, self.zoom_level * 1.1)
                elif event.y < 0:  # Scroll down - zoom out
                    self.zoom_level = max(self.min_zoom, self.zoom_level / 1.1)
                
                # Adjust hex size based on zoom
                if self.zoom_level != old_zoom:
                    self.hex_map.hex_size = int(25 * self.zoom_level)
            
            # Pass to buttons
            for button in self.buttons:
                button.handle_event(event)
                
    def update(self, dt):
        """Update screen state"""
        pass
        
    def draw(self):
        """Draw the galaxy map"""
        # Background
        self.screen.fill(LCARS_COLORS['black'])
        
        # Calculate map area dimensions
        map_width = self.screen_width - 640
        map_height = self.screen_height - 70
        
        # Draw hex grid on map area
        map_surface = pygame.Surface((map_width, map_height))
        map_surface.fill(LCARS_COLORS['black'])
        
        # Draw grid
        self.hex_map.draw_grid(map_surface, map_width, map_height, radius=30)
        
        # Draw systems
        for system in self.systems:
            system.draw(map_surface, self.hex_map, self.font_tiny)
            
            # Highlight selected system
            if system == self.selected_system:
                x, y = self.hex_map.hex_to_pixel(system.q, system.r)
                pygame.draw.circle(map_surface, LCARS_COLORS['orange'], 
                                 (int(x), int(y)), 15, width=2)
            
            # Highlight current system
            if system == self.current_system:
                x, y = self.hex_map.hex_to_pixel(system.q, system.r)
                pygame.draw.circle(map_surface, LCARS_COLORS['green'], 
                                 (int(x), int(y)), 20, width=3)
        
        # Blit map surface
        self.screen.blit(map_surface, (320, 70))
        
        # Draw UI panels
        self.top_panel.draw(self.screen)
        self.info_panel.draw(self.screen)
        self.control_panel.draw(self.screen)
        
        # Header
        title = self.font_large.render("GALAXY MAP", True, LCARS_COLORS['orange'])
        self.screen.blit(title, (self.screen_width // 2 - 100, 15))
        
        # Zoom indicator
        zoom_text = self.font_tiny.render(f"Zoom: {self.zoom_level:.1f}x", True, LCARS_COLORS['text_gray'])
        self.screen.blit(zoom_text, (self.screen_width - 150, 20))
        
        # Left panel - System Info
        info_y = 90
        
        if self.current_system:
            current_label = self.font_medium.render("CURRENT LOCATION", True, 
                                                    LCARS_COLORS['green'])
            self.screen.blit(current_label, (30, info_y))
            info_y += 40
            
            name = self.font_small.render(self.current_system.name, True, 
                                         LCARS_COLORS['text_white'])
            self.screen.blit(name, (30, info_y))
            info_y += 30
            
            faction = self.font_small.render(f"Faction: {self.current_system.faction or 'Unknown'}", 
                                            True, LCARS_COLORS['text_gray'])
            self.screen.blit(faction, (30, info_y))
            info_y += 60
        
        if self.selected_system:
            selected_label = self.font_medium.render("SELECTED SYSTEM", True, 
                                                     LCARS_COLORS['orange'])
            self.screen.blit(selected_label, (30, info_y))
            info_y += 40
            
            name = self.font_small.render(self.selected_system.name, True, 
                                         LCARS_COLORS['text_white'])
            self.screen.blit(name, (30, info_y))
            info_y += 30
            
            faction = self.font_small.render(f"Faction: {self.selected_system.faction or 'Unknown'}", 
                                            True, LCARS_COLORS['text_gray'])
            self.screen.blit(faction, (30, info_y))
            info_y += 25
            
            system_type = self.font_small.render(f"Type: {self.selected_system.system_type.title()}", 
                                                 True, LCARS_COLORS['text_gray'])
            self.screen.blit(system_type, (30, info_y))
            info_y += 30
            
            if self.current_system:
                distance = self.hex_map.hex_distance(
                    self.current_system.q, self.current_system.r,
                    self.selected_system.q, self.selected_system.r
                )
                dist_text = self.font_small.render(f"Distance: {distance} LY", True, 
                                                   LCARS_COLORS['light_blue'])
                self.screen.blit(dist_text, (30, info_y))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.font_small)
        
        # Controls help
        help_y = self.screen_height - 120
        help_text = [
            "CONTROLS:",
            "Arrow/WASD: Pan map",
            "Mouse Wheel: Zoom",
            "+/- Keys: Zoom",
            "Left Click: Select",
            "Drag: Pan map",
        ]
        for i, text in enumerate(help_text):
            surface = self.font_tiny.render(text, True, LCARS_COLORS['text_dim'])
            self.screen.blit(surface, (30, help_y + i * 20))
        
        pygame.display.flip()
