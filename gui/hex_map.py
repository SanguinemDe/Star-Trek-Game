"""
Hex Map System for Star Trek Galaxy
Hexagonal grid-based navigation with accurate Star Trek locations
"""
import math
import pygame
from gui.lcars_theme import LCARS_COLORS

class HexMap:
    """Hexagonal map grid system"""
    
    def __init__(self, hex_size=30):
        self.hex_size = hex_size  # Radius of hexagon in pixels
        self.hexes = {}  # Dictionary of hex coordinates to system data
        self.offset_x = 0  # Camera offset for panning
        self.offset_y = 0
        self.zoom = 1.0
        
    def hex_to_pixel(self, q, r):
        """Convert hex coordinates (axial) to pixel coordinates"""
        x = self.hex_size * (3/2 * q)
        y = self.hex_size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
        return (x + self.offset_x, y + self.offset_y)
        
    def pixel_to_hex(self, x, y):
        """Convert pixel coordinates to hex coordinates (axial)"""
        # Adjust for camera offset
        x = (x - self.offset_x) / self.hex_size
        y = (y - self.offset_y) / self.hex_size
        
        # Axial coordinates
        q = (2/3 * x)
        r = (-1/3 * x + math.sqrt(3)/3 * y)
        
        return self.hex_round(q, r)
        
    def hex_round(self, q, r):
        """Round fractional hex coordinates to nearest hex"""
        s = -q - r
        
        rq = round(q)
        rr = round(r)
        rs = round(s)
        
        q_diff = abs(rq - q)
        r_diff = abs(rr - r)
        s_diff = abs(rs - s)
        
        if q_diff > r_diff and q_diff > s_diff:
            rq = -rr - rs
        elif r_diff > s_diff:
            rr = -rq - rs
            
        return (int(rq), int(rr))
        
    def draw_hex(self, screen, q, r, color, filled=False):
        """Draw a single hexagon"""
        center_x, center_y = self.hex_to_pixel(q, r)
        points = []
        
        for i in range(6):
            angle = math.pi / 3 * i
            point_x = center_x + self.hex_size * math.cos(angle)
            point_y = center_y + self.hex_size * math.sin(angle)
            points.append((point_x, point_y))
            
        if filled:
            pygame.draw.polygon(screen, color, points)
        else:
            pygame.draw.polygon(screen, color, points, width=1)
            
    def draw_grid(self, screen, width, height, radius=20):
        """Draw hex grid on screen"""
        # Calculate how many hexes we need to cover the screen
        # Each hex has a width of hex_size * sqrt(3) and height of hex_size * 2
        hex_width = self.hex_size * 1.732  # sqrt(3)
        hex_height = self.hex_size * 1.5
        
        # Calculate radius needed to fill screen (add extra padding)
        radius_q = int(width / hex_width) + 5
        radius_r = int(height / hex_height) + 5
        max_radius = max(radius_q, radius_r)
        
        # Calculate visible hex range based on camera position and screen size
        center_hex = self.pixel_to_hex(width // 2, height // 2)
        
        for q in range(center_hex[0] - max_radius, center_hex[0] + max_radius):
            for r in range(center_hex[1] - max_radius, center_hex[1] + max_radius):
                x, y = self.hex_to_pixel(q, r)
                
                # Only draw if on screen (with some margin)
                if -self.hex_size * 2 <= x <= width + self.hex_size * 2 and \
                   -self.hex_size * 2 <= y <= height + self.hex_size * 2:
                    self.draw_hex(screen, q, r, LCARS_COLORS['text_dim'])
                    
    def hex_distance(self, q1, r1, q2, r2):
        """Calculate distance between two hexes in light years (1 hex = 1 LY)"""
        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2
        
    def add_system(self, q, r, name, data):
        """Add a star system to the map"""
        self.hexes[(q, r)] = {
            'name': name,
            'data': data,
            'q': q,
            'r': r
        }
        
    def get_system_at(self, q, r):
        """Get system at hex coordinates"""
        return self.hexes.get((q, r))
        
    def pan(self, dx, dy):
        """Pan the camera"""
        self.offset_x += dx
        self.offset_y += dy


class StarSystem:
    """Star system on hex map"""
    
    def __init__(self, name, q, r, faction=None, system_type='normal', importance='minor'):
        self.name = name
        self.q = q  # Hex coordinate
        self.r = r  # Hex coordinate
        self.faction = faction  # Federation, Klingon, Romulan, etc.
        self.system_type = system_type  # normal, homeworld, station, outpost
        self.importance = importance  # major, minor, unknown
        self.explored = False
        
    def get_color(self):
        """Get color based on faction and type"""
        if self.system_type == 'homeworld':
            return LCARS_COLORS['orange']
        elif self.system_type == 'station':
            return LCARS_COLORS['light_blue']
        elif self.faction == 'Federation':
            return LCARS_COLORS['blue']
        elif self.faction == 'Klingon':
            return LCARS_COLORS['red']
        elif self.faction == 'Romulan':
            return LCARS_COLORS['green']
        elif self.faction == 'Cardassian':
            return LCARS_COLORS['yellow']
        else:
            return LCARS_COLORS['text_gray']
            
    def draw(self, screen, hex_map, font):
        """Draw the system on the map"""
        x, y = hex_map.hex_to_pixel(self.q, self.r)
        color = self.get_color()
        
        # Draw star
        if self.system_type == 'homeworld':
            pygame.draw.circle(screen, color, (int(x), int(y)), 8)
            pygame.draw.circle(screen, LCARS_COLORS['text_white'], (int(x), int(y)), 8, width=2)
        elif self.system_type == 'station':
            # Draw square for stations
            rect = pygame.Rect(int(x) - 6, int(y) - 6, 12, 12)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, LCARS_COLORS['text_white'], rect, width=2)
        else:
            # Normal star
            pygame.draw.circle(screen, color, (int(x), int(y)), 4)
            
        # Draw name if important or explored
        if self.importance == 'major' or self.explored:
            text_surface = font.render(self.name, True, LCARS_COLORS['text_white'])
            text_rect = text_surface.get_rect(center=(int(x), int(y) - 15))
            screen.blit(text_surface, text_rect)
