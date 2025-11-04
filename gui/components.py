"""
UI Components for LCARS Interface
Reusable buttons, panels, and widgets with theme support
"""
import pygame
from gui.lcars_theme import LCARS_COLORS, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS, get_current_theme, get_accent_color

def get_corner_radius():
    """Get appropriate corner radius based on current theme"""
    theme = get_current_theme()
    if theme == 'lcars_v2':
        return 5  # More angular for V2
    return BUTTON_CORNER_RADIUS  # Rounded for V1

class Button:
    """LCARS-style button with rounded ends"""
    
    def __init__(self, x, y, width, height, text, color='orange', text_color='black', 
                 callback=None, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = LCARS_COLORS[color]
        self.text_color = LCARS_COLORS[text_color]
        self.callback = callback
        self.font_size = font_size
        self.hovered = False
        self.pressed = False
        
    def draw(self, screen, font):
        """Draw the button with LCARS styling"""
        # Change color on hover
        color = self.color
        if self.hovered:
            # Lighten color on hover
            color = tuple(min(255, c + 30) for c in self.color)
        if self.pressed:
            # Darken color on press
            color = tuple(max(0, c - 30) for c in self.color)
            
        # Get corner radius based on theme
        corner_radius = get_corner_radius()
        
        # Draw rounded rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=corner_radius)
        
        # Draw text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
            self.pressed = False
            
    def update_text(self, new_text):
        """Update button text"""
        self.text = new_text


class Panel:
    """LCARS-style panel for displaying information"""
    
    def __init__(self, x, y, width, height, color='bg_medium', border_color=None, corner_radius=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = LCARS_COLORS[color]
        self.border_color = LCARS_COLORS[border_color] if border_color else None
        self.corner_radius = corner_radius
        
    def draw(self, screen):
        """Draw the panel"""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, width=3, 
                           border_radius=self.corner_radius)


class TextInput:
    """LCARS-style text input field"""
    
    def __init__(self, x, y, width, height, placeholder="", max_length=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, screen, font):
        """Draw the text input field"""
        # Background
        color = LCARS_COLORS['bg_dark'] if self.active else LCARS_COLORS['bg_medium']
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # Border
        border_color = LCARS_COLORS['orange'] if self.active else LCARS_COLORS['text_dim']
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=10)
        
        # Text or placeholder
        display_text = self.text if self.text else self.placeholder
        text_color = LCARS_COLORS['text_white'] if self.text else LCARS_COLORS['text_dim']
        text_surface = font.render(display_text, True, text_color)
        
        # Add cursor if active
        if self.active and self.cursor_visible and self.text:
            display_text += "|"
            text_surface = font.render(display_text, True, text_color)
        
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """Handle keyboard and mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < self.max_length:
                # Only accept printable characters
                if event.unicode.isprintable():
                    self.text += event.unicode
                    
    def update(self, dt):
        """Update cursor blink"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0


class Slider:
    """LCARS-style slider for numeric input"""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, label=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
        self.track_rect = pygame.Rect(x, y, width, 10)
        self.handle_radius = 12
        self.handle_x = self._value_to_x(initial_val)
        
    def _value_to_x(self, value):
        """Convert value to x position"""
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.x + int(ratio * self.width)
        
    def _x_to_value(self, x):
        """Convert x position to value"""
        ratio = (x - self.x) / self.width
        ratio = max(0, min(1, ratio))
        return int(self.min_val + ratio * (self.max_val - self.min_val))
        
    def draw(self, screen, font):
        """Draw the slider"""
        # Draw track
        pygame.draw.rect(screen, LCARS_COLORS['bg_dark'], self.track_rect, 
                        border_radius=5)
        pygame.draw.rect(screen, LCARS_COLORS['orange'], self.track_rect, 
                        width=2, border_radius=5)
        
        # Draw filled portion
        filled_rect = pygame.Rect(self.x, self.y, self.handle_x - self.x, 10)
        pygame.draw.rect(screen, LCARS_COLORS['orange'], filled_rect, border_radius=5)
        
        # Draw handle
        handle_color = LCARS_COLORS['light_blue'] if self.dragging else LCARS_COLORS['orange']
        pygame.draw.circle(screen, handle_color, (self.handle_x, self.y + 5), 
                          self.handle_radius)
        
        # Draw label and value
        if self.label:
            label_surface = font.render(f"{self.label}: {self.value}", True, 
                                       LCARS_COLORS['text_white'])
            screen.blit(label_surface, (self.x, self.y - 25))
            
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            distance = ((mouse_pos[0] - self.handle_x) ** 2 + 
                       (mouse_pos[1] - (self.y + 5)) ** 2) ** 0.5
            if distance <= self.handle_radius:
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_x = max(self.x, min(self.x + self.width, event.pos[0]))
                self.value = self._x_to_value(self.handle_x)


class RadioButtonList:
    """LCARS-style radio button list"""
    
    def __init__(self, x, y, width, height, options, initial_index=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height  # Height per option
        self.options = options
        self.selected_index = initial_index
        self.option_rects = []
        
    def draw(self, screen, font):
        """Draw the radio button list"""
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            option_y = self.y + i * (self.height + 5)
            option_rect = pygame.Rect(self.x, option_y, self.width, self.height)
            self.option_rects.append(option_rect)
            
            # Background color
            if i == self.selected_index:
                color = LCARS_COLORS['orange']
                text_color = LCARS_COLORS['black']
            else:
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    color = LCARS_COLORS['light_blue']
                    text_color = LCARS_COLORS['black']
                else:
                    color = LCARS_COLORS['blue']
                    text_color = LCARS_COLORS['text_white']
            
            # Draw button
            pygame.draw.rect(screen, color, option_rect, border_radius=10)
            
            # Draw radio circle
            circle_x = self.x + 15
            circle_y = option_y + self.height // 2
            pygame.draw.circle(screen, LCARS_COLORS['bg_dark'], (circle_x, circle_y), 8)
            pygame.draw.circle(screen, text_color, (circle_x, circle_y), 8, width=2)
            
            # Fill circle if selected
            if i == self.selected_index:
                pygame.draw.circle(screen, LCARS_COLORS['black'], (circle_x, circle_y), 5)
            
            # Draw option text
            text_surface = font.render(option, True, text_color)
            text_rect = text_surface.get_rect(midleft=(self.x + 35, option_y + self.height // 2))
            screen.blit(text_surface, text_rect)
            
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    return True
        return False


class DropdownMenu:
    """LCARS-style dropdown menu"""
    
    def __init__(self, x, y, width, height, options, initial_index=0, max_visible=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = initial_index
        self.expanded = False
        self.option_rects = []
        self.max_visible = max_visible
        self.scroll_offset = 0
        
    def draw(self, screen, font):
        """Draw the dropdown menu"""
        # Main button
        color = LCARS_COLORS['orange'] if not self.expanded else LCARS_COLORS['light_blue']
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # Selected option text
        text = self.options[self.selected_index]
        text_surface = font.render(text, True, LCARS_COLORS['black'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Arrow indicator
        arrow = "▼" if not self.expanded else "▲"
        arrow_surface = font.render(arrow, True, LCARS_COLORS['black'])
        arrow_rect = arrow_surface.get_rect(midright=(self.rect.right - 10, self.rect.centery))
        screen.blit(arrow_surface, arrow_rect)
        
        # Expanded options
        if self.expanded:
            # Calculate visible range
            visible_options = min(self.max_visible, len(self.options))
            dropdown_height = visible_options * (self.rect.height + 5)
            
            # Background panel for dropdown
            dropdown_bg = pygame.Rect(self.rect.x, self.rect.bottom + 5, 
                                     self.rect.width, dropdown_height)
            pygame.draw.rect(screen, LCARS_COLORS['bg_dark'], dropdown_bg, border_radius=10)
            pygame.draw.rect(screen, LCARS_COLORS['orange'], dropdown_bg, width=2, border_radius=10)
            
            # Draw visible options
            self.option_rects = []
            start_idx = self.scroll_offset
            end_idx = min(start_idx + visible_options, len(self.options))
            
            for i in range(start_idx, end_idx):
                option = self.options[i]
                display_idx = i - start_idx
                option_y = self.rect.bottom + 5 + display_idx * (self.rect.height + 5)
                option_rect = pygame.Rect(self.rect.x, option_y, self.rect.width, 
                                         self.rect.height)
                self.option_rects.append((i, option_rect))
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                color = LCARS_COLORS['light_blue'] if option_rect.collidepoint(mouse_pos) else LCARS_COLORS['blue']
                pygame.draw.rect(screen, color, option_rect, border_radius=10)
                
                # Option text
                text_surface = font.render(option, True, LCARS_COLORS['text_white'])
                text_rect = text_surface.get_rect(center=option_rect.center)
                screen.blit(text_surface, text_rect)
            
            # Draw scroll indicators if needed
            if len(self.options) > self.max_visible:
                # Up arrow
                if self.scroll_offset > 0:
                    arrow_up = "▲"
                    arrow_surface = font.render(arrow_up, True, LCARS_COLORS['orange'])
                    arrow_rect = arrow_surface.get_rect(center=(self.rect.right - 20, self.rect.bottom + 15))
                    screen.blit(arrow_surface, arrow_rect)
                
                # Down arrow
                if self.scroll_offset + self.max_visible < len(self.options):
                    arrow_down = "▼"
                    arrow_surface = font.render(arrow_down, True, LCARS_COLORS['orange'])
                    arrow_rect = arrow_surface.get_rect(center=(self.rect.right - 20, self.rect.bottom + dropdown_height - 10))
                    screen.blit(arrow_surface, arrow_rect)
                
    def handle_event(self, event):
        """Handle mouse and keyboard events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check main button
            if self.rect.collidepoint(mouse_pos):
                self.expanded = not self.expanded
                self.scroll_offset = 0  # Reset scroll when opening
                return True
                
            # Check options if expanded
            if self.expanded:
                for option_idx, option_rect in self.option_rects:
                    if option_rect.collidepoint(mouse_pos):
                        self.selected_index = option_idx
                        self.expanded = False
                        return True
                        
                # Click outside closes dropdown
                self.expanded = False
                return True
                
        elif event.type == pygame.MOUSEWHEEL and self.expanded:
            # Handle mouse wheel scrolling when dropdown is expanded
            if event.y > 0:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.y < 0:  # Scroll down
                max_scroll = max(0, len(self.options) - self.max_visible)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                return True
                
        elif event.type == pygame.KEYDOWN and self.expanded:
            # Handle keyboard navigation
            if event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.key == pygame.K_DOWN:
                max_scroll = max(0, len(self.options) - self.max_visible)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                return True
            elif event.key == pygame.K_ESCAPE:
                self.expanded = False
                return True
        
        return False


class TabbedPanel:
    """Panel with tabs for different content sections"""
    
    def __init__(self, x, y, width, height, tabs):
        """
        Create a tabbed panel
        
        Args:
            x, y: Position of panel
            width, height: Size of panel
            tabs: List of tab names (strings)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tabs = tabs
        self.active_tab = 0  # Index of active tab
        self.tab_height = 35  # Height of tab bar
        self.content_y = y + self.tab_height  # Y position where content starts
        self.content_height = height - self.tab_height
        
        # Calculate tab widths
        self.tab_width = width // len(tabs)
        
    def draw_tabs(self, screen, font):
        """Draw the tab bar"""
        accent_color = get_accent_color()
        
        for i, tab_name in enumerate(self.tabs):
            tab_x = self.x + (i * self.tab_width)
            tab_rect = pygame.Rect(tab_x, self.y, self.tab_width, self.tab_height)
            
            # Active tab is highlighted
            if i == self.active_tab:
                color = accent_color
                text_color = LCARS_COLORS['black']
            else:
                color = LCARS_COLORS['bg_medium']
                text_color = LCARS_COLORS['text_gray']
            
            # Draw tab background
            pygame.draw.rect(screen, color, tab_rect)
            
            # Draw tab border
            pygame.draw.rect(screen, accent_color, tab_rect, 2)
            
            # Draw tab text
            text_surface = font.render(tab_name.upper(), True, text_color)
            text_rect = text_surface.get_rect(center=tab_rect.center)
            screen.blit(text_surface, text_rect)
    
    def draw_background(self, screen):
        """Draw the panel background"""
        accent_color = get_accent_color()
        content_rect = pygame.Rect(self.x, self.content_y, self.width, self.content_height)
        pygame.draw.rect(screen, LCARS_COLORS['bg_dark'], content_rect)
        pygame.draw.rect(screen, accent_color, content_rect, 2)
    
    def handle_click(self, mouse_pos):
        """Handle mouse click on tabs"""
        mx, my = mouse_pos
        
        # Check if click is in tab area
        if self.y <= my < self.y + self.tab_height:
            if self.x <= mx < self.x + self.width:
                # Determine which tab was clicked
                tab_index = (mx - self.x) // self.tab_width
                if 0 <= tab_index < len(self.tabs):
                    self.active_tab = tab_index
                    return True
        return False
    
    def get_content_rect(self):
        """Get the rectangle for content area"""
        return pygame.Rect(self.x, self.content_y, self.width, self.content_height)
