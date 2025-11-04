"""
Hexagonal Grid System for Combat
Pointy-top hexagons for tactical combat
"""

import math
import pygame


class HexGrid:
    """Hexagonal grid system with axial coordinates"""
    
    def __init__(self, hex_size=50, offset_x=0, offset_y=0):
        """
        Initialize hex grid
        
        Args:
            hex_size: Radius of hexagon (center to corner)
            offset_x: X offset for drawing
            offset_y: Y offset for drawing
        """
        self.hex_size = hex_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Hex dimensions (pointy-top orientation)
        self.width = math.sqrt(3) * hex_size
        self.height = 2 * hex_size
        self.vert_spacing = self.height * 3/4  # Vertical distance between hex centers
        
    def axial_to_pixel(self, q, r):
        """
        Convert axial hex coordinates to pixel coordinates
        
        Args:
            q: Column coordinate
            r: Row coordinate
            
        Returns:
            (x, y) pixel coordinates of hex center
        """
        x = self.hex_size * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
        y = self.hex_size * (3/2 * r)
        return (x + self.offset_x, y + self.offset_y)
    
    def pixel_to_axial(self, x, y):
        """
        Convert pixel coordinates to axial hex coordinates
        
        Args:
            x: Pixel x coordinate
            y: Pixel y coordinate
            
        Returns:
            (q, r) axial hex coordinates
        """
        # Adjust for offset
        x -= self.offset_x
        y -= self.offset_y
        
        # Convert to fractional axial coordinates
        q = (math.sqrt(3)/3 * x - 1/3 * y) / self.hex_size
        r = (2/3 * y) / self.hex_size
        
        # Round to nearest hex
        return self.axial_round(q, r)
    
    def axial_round(self, q, r):
        """
        Round fractional axial coordinates to nearest hex
        
        Args:
            q: Fractional q coordinate
            r: Fractional r coordinate
            
        Returns:
            (q, r) rounded integer coordinates
        """
        # Convert axial to cube coordinates
        x = q
        z = r
        y = -x - z
        
        # Round cube coordinates
        rx = round(x)
        ry = round(y)
        rz = round(z)
        
        # Find which coordinate has largest rounding error
        x_diff = abs(rx - x)
        y_diff = abs(ry - y)
        z_diff = abs(rz - z)
        
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
            
        # Convert back to axial
        return (int(rx), int(rz))
    
    def distance(self, q1, r1, q2, r2):
        """
        Calculate hex distance between two hexes
        
        Args:
            q1, r1: First hex coordinates
            q2, r2: Second hex coordinates
            
        Returns:
            Integer distance in hexes
        """
        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2
    
    def get_hex_corners(self, q, r):
        """
        Get pixel coordinates of hex corners (pointy-top)
        
        Args:
            q, r: Axial hex coordinates
            
        Returns:
            List of 6 (x, y) tuples for corners
        """
        center_x, center_y = self.axial_to_pixel(q, r)
        corners = []
        
        for i in range(6):
            angle_deg = 60 * i - 30  # Pointy-top starts at -30°
            angle_rad = math.pi / 180 * angle_deg
            x = center_x + self.hex_size * math.cos(angle_rad)
            y = center_y + self.hex_size * math.sin(angle_rad)
            corners.append((int(x), int(y)))
            
        return corners
    
    def draw_hex(self, surface, q, r, color, width=1):
        """
        Draw a single hexagon
        
        Args:
            surface: Pygame surface to draw on
            q, r: Hex coordinates
            color: RGB color tuple
            width: Line width (0 for filled)
        """
        corners = self.get_hex_corners(q, r)
        pygame.draw.polygon(surface, color, corners, width)
    
    def draw_grid(self, surface, min_q, max_q, min_r, max_r, color, width=1):
        """
        Draw a grid of hexagons
        
        Args:
            surface: Pygame surface to draw on
            min_q, max_q: Q coordinate range
            min_r, max_r: R coordinate range
            color: RGB color tuple
            width: Line width
        """
        for q in range(min_q, max_q + 1):
            for r in range(min_r, max_r + 1):
                self.draw_hex(surface, q, r, color, width)
    
    def get_hex_at_pixel(self, x, y):
        """
        Get hex coordinates at pixel position
        
        Args:
            x, y: Pixel coordinates
            
        Returns:
            (q, r) hex coordinates
        """
        return self.pixel_to_axial(x, y)
    
    def get_neighbors(self, q, r):
        """
        Get coordinates of 6 neighboring hexes
        
        Args:
            q, r: Center hex coordinates
            
        Returns:
            List of 6 (q, r) tuples for neighbors
        """
        # Axial direction vectors for 6 neighbors
        directions = [
            (+1, 0), (+1, -1), (0, -1),
            (-1, 0), (-1, +1), (0, +1)
        ]
        return [(q + dq, r + dr) for dq, dr in directions]
    
    def line_between(self, q1, r1, q2, r2):
        """
        Get line of hexes between two hexes (for line of sight, movement, etc)
        
        Args:
            q1, r1: Start hex
            q2, r2: End hex
            
        Returns:
            List of (q, r) tuples along the line
        """
        distance = self.distance(q1, r1, q2, r2)
        if distance == 0:
            return [(q1, r1)]
        
        results = []
        for i in range(distance + 1):
            t = i / distance
            q = q1 + (q2 - q1) * t
            r = r1 + (r2 - r1) * t
            results.append(self.axial_round(q, r))
        
        return results
    
    def get_ring(self, q, r, radius):
        """
        Get hexes in a ring at specified radius
        
        Args:
            q, r: Center hex
            radius: Ring radius
            
        Returns:
            List of (q, r) tuples in ring
        """
        if radius == 0:
            return [(q, r)]
        
        results = []
        # Start at a hex 'radius' steps away
        hex_q, hex_r = q - radius, r + radius
        
        # Six directions for ring traversal
        directions = [
            (+1, 0), (+1, -1), (0, -1),
            (-1, 0), (-1, +1), (0, +1)
        ]
        
        for direction in range(6):
            for step in range(radius):
                results.append((hex_q, hex_r))
                dq, dr = directions[direction]
                hex_q += dq
                hex_r += dr
        
        return results
    
    def get_spiral(self, q, r, radius):
        """
        Get hexes in a spiral from center outward
        
        Args:
            q, r: Center hex
            radius: Spiral radius
            
        Returns:
            List of (q, r) tuples in spiral order
        """
        results = [(q, r)]
        for k in range(1, radius + 1):
            results.extend(self.get_ring(q, r, k))
        return results
