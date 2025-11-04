"""
Combat Test Arena - Hex-Based Tactical Combat System

This module implements a complete tactical combat system featuring:

COMBAT PHASES (8-phase turn structure):
  1. Initiative - Determines action order (currently disabled for testing)
  2. Movement - WASD controls for hex-based movement and rotation
  3. Targeting - Click to select up to 3 targets (primary/secondary/tertiary)
  4. Firing - Automatic weapon firing at selected targets with accuracy penalties
  5. Damage - Shield arc-based damage application and hull damage
  6. Power - Power distribution and shield regeneration (placeholder)
  7. Repair - Damage control and system repairs (placeholder)
  8. Housekeeping - Cooldown reduction and status updates

HEX GRID SYSTEM:
  - Pointy-top hex orientation with axial coordinates (q, r)
  - Movement cost: 1 point per hex, 1 point per 60° turn
  - Turning rules: Must move before turning, one turn per hex moved
  - Smooth animation with cubic ease-in-out interpolation

COMBAT MECHANICS:
  - Range bands: Point Blank (0-3), Close (4-5), Med (6-8), Long (9-11), Extreme (12-13)
  - Weapon arcs: fore/aft/port/starboard based on ship facing
  - Shield arcs: Damage applied to correct facing based on attack angle
  - Multi-targeting: Primary (100%), Secondary (75%), Tertiary (50%) accuracy
  - AI opponents with personalities: Aggressive, Defensive, Balanced, Sniper

UI FEATURES:
  - Tabbed panel system: STATUS, WEAPONS, POWER, DAMAGE tabs
  - Real-time combat log with color-coded messages
  - Visual range indicators and targeting lines
  - Ship sprite rotation and smooth movement animation

CONTROLS:
  - WASD: Movement (W=forward, S=backward, A=turn left, D=turn right)
  - Mouse: Click ships to target, click tabs to switch
  - SPACE: Fire weapons (during firing phase)
  - ENTER: End turn/advance phase
  - R: Reset arena
  - ESC: Return to main menu
"""

import pygame
import math
from gui.lcars_theme import LCARS_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, get_font, get_accent_color, get_warning_color
from gui.components import Panel, Button, TabbedPanel
from gui.hex_grid import HexGrid
from game.ship_ai import ShipAI, AIPersonality


class WeaponBeamEffect:
    """Visual effect for energy weapon beam (phasers, disruptors, etc.)"""
    
    def __init__(self, start_pos, end_pos, beam_components, impact_sprite, weapon_type='phaser', randomize_impact=True):
        """
        Initialize an energy weapon beam effect
        
        Args:
            start_pos: (x, y) tuple for beam start
            end_pos: (x, y) tuple for beam end (impact point)
            beam_components: Dict with 'head', 'mid', 'tail' sprites
            impact_sprite: Sprite sheet for impact animation
            weapon_type: Type of weapon ('phaser', 'disruptor', etc.)
            randomize_impact: If True, adds random offset to impact point
        """
        self.start_pos = start_pos
        self.weapon_type = weapon_type
        
        # Add random variation to impact point so multiple beams don't hit same spot
        if randomize_impact:
            import random
            offset_x = random.randint(-25, 25)
            offset_y = random.randint(-25, 25)
            self.end_pos = (end_pos[0] + offset_x, end_pos[1] + offset_y)
        else:
            self.end_pos = end_pos
            
        self.beam_components = beam_components
        self.impact_sprite = impact_sprite
        
        # Get weapon-specific color for beam tinting
        self.beam_color = self._get_beam_color()
        
        # Animation timing (in milliseconds)
        self.lifetime = 0.0  # Milliseconds elapsed
        self.beam_duration = 800.0  # How long beam stays visible (ms)
        self.impact_duration = 600.0  # How long impact animation plays (ms)
        self.total_duration = self.beam_duration + self.impact_duration
        
        # Calculate beam angle
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        self.angle = math.degrees(math.atan2(dy, dx))
        self.distance = math.sqrt(dx*dx + dy*dy)
        
        # Impact animation - auto-detect frame count from sprite sheet
        if impact_sprite:
            sheet_width = impact_sprite.get_width()
            sheet_height = impact_sprite.get_height()
            # Assume frames are square-ish, so divide longer dimension by shorter
            if sheet_width > sheet_height:
                # Horizontal layout: 640x64 = 10 frames of 64x64 each
                self.impact_frame_count = sheet_width // sheet_height
            else:
                # Vertical layout
                self.impact_frame_count = sheet_height // sheet_width
        else:
            self.impact_frame_count = 8  # Default fallback
            
        self.impact_frame = 0
        self.impact_frame_time = self.impact_duration / self.impact_frame_count
        
    def update(self, dt):
        """Update effect animation
        
        Args:
            dt: Delta time in milliseconds
        """
        self.lifetime += dt
        
        # Update impact frame if in impact phase
        if self.lifetime > self.beam_duration:
            impact_time = self.lifetime - self.beam_duration
            self.impact_frame = int(impact_time / self.impact_frame_time)
            if self.impact_frame >= self.impact_frame_count:
                self.impact_frame = self.impact_frame_count - 1
        
        return self.lifetime < self.total_duration  # Return True if still active
    
    def _get_beam_color(self):
        """Get the color for this weapon type's beam"""
        color_map = {
            'phaser': (255, 150, 50),      # Orange
            'disruptor': (50, 255, 50),    # Green
            'plasma': (100, 255, 100),     # Light green
            'polaron': (150, 50, 255),     # Purple
            'tetryon': (50, 150, 255)      # Blue
        }
        return color_map.get(self.weapon_type, (255, 150, 50))
    
    def draw(self, surface):
        """Draw the energy weapon beam effect"""
        if not self.beam_components:
            # Fallback to simple line if no sprites loaded (use weapon-specific color)
            pygame.draw.line(surface, self.beam_color, self.start_pos, self.end_pos, 3)
            if self.lifetime > self.beam_duration:
                # Simple circle for impact
                pygame.draw.circle(surface, self.beam_color, self.end_pos, 15, 3)
            return
        
        # Draw beam (during beam phase)
        if self.lifetime < self.beam_duration:
            self._draw_beam(surface)
        
        # Draw impact (during impact phase)
        if self.lifetime > self.beam_duration and self.impact_sprite:
            self._draw_impact(surface)
    
    def _draw_beam(self, surface):
        """Draw the phaser beam using head/mid/tail components"""
        head = self.beam_components.get('head')
        mid = self.beam_components.get('mid')
        tail = self.beam_components.get('tail')
        
        if not all([head, mid, tail]):
            return
        
        # Calculate fade based on lifetime (fade out in last 200ms of beam)
        fade_start = self.beam_duration - 200.0
        if self.lifetime > fade_start:
            alpha = int(255 * (1.0 - (self.lifetime - fade_start) / 200.0))
            alpha = max(0, min(255, alpha))
        else:
            alpha = 255
        
        # Scale down beam components for a sleeker, thinner look (30% of original)
        beam_scale = 0.3
        scaled_head = pygame.transform.smoothscale(
            head, 
            (int(head.get_width() * beam_scale), int(head.get_height() * beam_scale))
        )
        scaled_mid = pygame.transform.smoothscale(
            mid, 
            (int(mid.get_width() * beam_scale), int(mid.get_height() * beam_scale))
        )
        scaled_tail = pygame.transform.smoothscale(
            tail, 
            (int(tail.get_width() * beam_scale), int(tail.get_height() * beam_scale))
        )
        
        # Apply alpha to components
        scaled_head.set_alpha(alpha)
        scaled_mid.set_alpha(alpha)
        scaled_tail.set_alpha(alpha)
        
        # Rotate sprites to match beam angle
        rotated_head = pygame.transform.rotate(scaled_head, -self.angle)
        rotated_mid = pygame.transform.rotate(scaled_mid, -self.angle)
        rotated_tail = pygame.transform.rotate(scaled_tail, -self.angle)
        
        # Calculate positions along beam
        # Head at start
        head_rect = rotated_head.get_rect(center=self.start_pos)
        surface.blit(rotated_head, head_rect)
        
        # Mid sections to fill distance
        mid_width = scaled_mid.get_width()
        num_mids = max(1, int(self.distance / (mid_width * 0.8)))  # Slight overlap for continuous beam
        
        for i in range(num_mids):
            t = (i + 1) / (num_mids + 1)
            mid_x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
            mid_y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
            mid_rect = rotated_mid.get_rect(center=(mid_x, mid_y))
            surface.blit(rotated_mid, mid_rect)
        
        # Tail at end
        tail_rect = rotated_tail.get_rect(center=self.end_pos)
        surface.blit(rotated_tail, tail_rect)
    
    def _draw_impact(self, surface):
        """Draw the impact explosion sprite"""
        if not self.impact_sprite:
            return
        
        # Get sprite sheet dimensions
        sheet_width = self.impact_sprite.get_width()
        sheet_height = self.impact_sprite.get_height()
        
        # Determine if sprite sheet is horizontal or vertical
        is_horizontal = sheet_width > sheet_height
        
        if is_horizontal:
            # Horizontal sprite sheet (frames arranged left to right)
            frame_width = sheet_width // self.impact_frame_count
            frame_height = sheet_height
            current_frame = min(self.impact_frame, self.impact_frame_count - 1)
            source_rect = pygame.Rect(current_frame * frame_width, 0, frame_width, frame_height)
        else:
            # Vertical sprite sheet (frames arranged top to bottom)
            frame_width = sheet_width
            frame_height = sheet_height // self.impact_frame_count
            current_frame = min(self.impact_frame, self.impact_frame_count - 1)
            source_rect = pygame.Rect(0, current_frame * frame_height, frame_width, frame_height)
        
        # Debug first time
        if not hasattr(self, '_debug_printed'):
            orientation = "horizontal" if is_horizontal else "vertical"
            print(f"Impact sprite: {sheet_width}x{sheet_height} ({orientation}), frame {current_frame}: {source_rect}")
            self._debug_printed = True
        
        # Extract just this frame using subsurface
        try:
            frame_image = self.impact_sprite.subsurface(source_rect).copy()
        except ValueError as e:
            print(f"Subsurface error: {e}, source_rect: {source_rect}")
            # If subsurface fails, fall back to manual extraction
            frame_image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_image.blit(self.impact_sprite, (0, 0), source_rect)
        
        # Scale the impact to a reasonable size
        scaled_size = (50, 50)  # Slightly smaller for better look
        scaled_frame = pygame.transform.smoothscale(frame_image, scaled_size)
        
        # Draw centered on impact point
        frame_rect = scaled_frame.get_rect(center=self.end_pos)
        surface.blit(scaled_frame, frame_rect)


class TorpedoProjectileEffect:
    """Visual effect for torpedo projectile (photon, quantum, etc.)"""
    
    def __init__(self, start_pos, end_pos, torpedo_sprite, impact_sprite, torpedo_type='photon'):
        """
        Initialize a torpedo projectile effect
        
        Args:
            start_pos: (x, y) tuple for launch point
            end_pos: (x, y) tuple for impact point
            torpedo_sprite: Sprite sheet for torpedo animation
            impact_sprite: Sprite sheet for explosion animation
            torpedo_type: Type of torpedo ('photon', 'quantum', etc.)
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.torpedo_sprite = torpedo_sprite
        self.impact_sprite = impact_sprite
        self.torpedo_type = torpedo_type
        
        # Calculate trajectory
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        self.angle = math.degrees(math.atan2(dy, dx))
        self.distance = math.sqrt(dx*dx + dy*dy)
        
        # Animation timing (in milliseconds)
        self.lifetime = 0.0
        # Torpedoes travel slower than beams but still reasonably fast
        self.travel_time = 500.0  # 0.5 seconds to reach target (fast!)
        self.impact_duration = 800.0  # 0.8 seconds for explosion
        self.total_duration = self.travel_time + self.impact_duration
        
        # Current position during flight
        self.current_pos = list(start_pos)
        self.has_impacted = False
        
        # Torpedo animation - auto-detect frame count
        if torpedo_sprite:
            sheet_width = torpedo_sprite.get_width()
            sheet_height = torpedo_sprite.get_height()
            if sheet_width > sheet_height:
                self.torpedo_frame_count = sheet_width // sheet_height
            else:
                self.torpedo_frame_count = sheet_height // sheet_width
        else:
            self.torpedo_frame_count = 8
            
        self.torpedo_frame = 0
        self.torpedo_frame_time = 100.0  # Change frame every 100ms for animation
        
        # Impact animation - auto-detect frame count
        if impact_sprite:
            sheet_width = impact_sprite.get_width()
            sheet_height = impact_sprite.get_height()
            if sheet_width > sheet_height:
                self.impact_frame_count = sheet_width // sheet_height
            else:
                self.impact_frame_count = sheet_height // sheet_width
        else:
            self.impact_frame_count = 10
            
        self.impact_frame = 0
        self.impact_frame_time = self.impact_duration / self.impact_frame_count
    
    def update(self, dt):
        """Update torpedo animation and position
        
        Args:
            dt: Delta time in milliseconds
        """
        self.lifetime += dt
        
        if self.lifetime < self.travel_time:
            # Torpedo is traveling
            progress = self.lifetime / self.travel_time
            
            # Interpolate position
            self.current_pos[0] = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
            self.current_pos[1] = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
            
            # Update torpedo animation frame
            self.torpedo_frame = int(self.lifetime / self.torpedo_frame_time) % self.torpedo_frame_count
            
        elif not self.has_impacted:
            # Just reached target
            self.has_impacted = True
            self.current_pos = list(self.end_pos)
            
        else:
            # Explosion phase
            impact_time = self.lifetime - self.travel_time
            self.impact_frame = int(impact_time / self.impact_frame_time)
            if self.impact_frame >= self.impact_frame_count:
                self.impact_frame = self.impact_frame_count - 1
        
        return self.lifetime < self.total_duration
    
    def draw(self, surface):
        """Draw the torpedo projectile or explosion"""
        if self.lifetime < self.travel_time:
            # Draw torpedo in flight
            self._draw_torpedo(surface)
        elif self.has_impacted:
            # Draw explosion
            self._draw_explosion(surface)
    
    def _draw_torpedo(self, surface):
        """Draw the animated torpedo sprite"""
        if not self.torpedo_sprite:
            # Fallback: draw colored circle
            color = self._get_torpedo_color()
            pygame.draw.circle(surface, color, (int(self.current_pos[0]), int(self.current_pos[1])), 5)
            return
        
        # Get sprite sheet dimensions
        sheet_width = self.torpedo_sprite.get_width()
        sheet_height = self.torpedo_sprite.get_height()
        
        # Determine layout
        is_horizontal = sheet_width > sheet_height
        
        if is_horizontal:
            frame_width = sheet_width // self.torpedo_frame_count
            frame_height = sheet_height
            source_rect = pygame.Rect(self.torpedo_frame * frame_width, 0, frame_width, frame_height)
        else:
            frame_width = sheet_width
            frame_height = sheet_height // self.torpedo_frame_count
            source_rect = pygame.Rect(0, self.torpedo_frame * frame_height, frame_width, frame_height)
        
        # Extract current frame
        try:
            frame_image = self.torpedo_sprite.subsurface(source_rect).copy()
        except ValueError:
            frame_image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_image.blit(self.torpedo_sprite, (0, 0), source_rect)
        
        # Scale torpedo to reasonable size (40x40)
        scaled_size = (40, 40)
        scaled_frame = pygame.transform.smoothscale(frame_image, scaled_size)
        
        # Rotate to match trajectory angle
        rotated_frame = pygame.transform.rotate(scaled_frame, -self.angle)
        
        # Draw at current position
        frame_rect = rotated_frame.get_rect(center=(int(self.current_pos[0]), int(self.current_pos[1])))
        surface.blit(rotated_frame, frame_rect)
    
    def _draw_explosion(self, surface):
        """Draw the explosion sprite"""
        if not self.impact_sprite:
            # Fallback: draw expanding circle
            color = self._get_torpedo_color()
            radius = 10 + int((self.impact_frame / self.impact_frame_count) * 30)
            pygame.draw.circle(surface, color, self.end_pos, radius, 3)
            return
        
        # Get sprite sheet dimensions
        sheet_width = self.impact_sprite.get_width()
        sheet_height = self.impact_sprite.get_height()
        
        is_horizontal = sheet_width > sheet_height
        
        if is_horizontal:
            frame_width = sheet_width // self.impact_frame_count
            frame_height = sheet_height
            source_rect = pygame.Rect(self.impact_frame * frame_width, 0, frame_width, frame_height)
        else:
            frame_width = sheet_width
            frame_height = sheet_height // self.impact_frame_count
            source_rect = pygame.Rect(0, self.impact_frame * frame_height, frame_width, frame_height)
        
        # Extract frame
        try:
            frame_image = self.impact_sprite.subsurface(source_rect).copy()
        except ValueError:
            frame_image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_image.blit(self.impact_sprite, (0, 0), source_rect)
        
        # Scale explosion (larger than phaser hit - 70x70)
        scaled_size = (70, 70)
        scaled_frame = pygame.transform.smoothscale(frame_image, scaled_size)
        
        # Draw centered on impact point
        frame_rect = scaled_frame.get_rect(center=self.end_pos)
        surface.blit(scaled_frame, frame_rect)
    
    def _get_torpedo_color(self):
        """Get fallback color for torpedo type"""
        color_map = {
            'photon': (255, 100, 100),    # Red
            'quantum': (100, 200, 255),   # Blue
            'plasma': (100, 255, 100),    # Green
            'tricobalt': (255, 255, 100), # Yellow
            'tetryon': (200, 100, 255)    # Purple
        }
        return color_map.get(self.torpedo_type, (255, 100, 100))


class CombatTestScreen:
    """Combat testing arena with two Odyssey-class ships"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Fonts - use sci-fi themed fonts
        self.font_large = get_font(48, bold=True)
        self.font_medium = get_font(32, bold=True)
        self.font_small = get_font(24)
        
        # Combat state (initialize before creating ships)
        self.combat_log = []
        self.turn_number = 1
        self.player_turn = True
        
        # Combat phase system
        self.combat_phase = "initiative"  # initiative, movement, targeting, firing, damage, power, repair, housekeeping
        self.phase_order = [
            "initiative",
            "movement", 
            "targeting",
            "firing",
            "damage",
            "power",
            "repair",
            "housekeeping"
        ]
        self.initiative_order = []  # List of ships in initiative order
        self.current_ship_index = 0  # Which ship is acting in current phase
        self.actions_completed = {
            "movement": False,
            "targeting": False,
            "firing": False,
            "power": False,
            "repair": False
        }
        
        # Movement tracking
        self.movement_points_remaining = 0
        self.movement_points_used = 0
        self.has_moved_this_turn = False  # Track if ship has moved forward/backward
        self.turns_this_activation = 0  # Track turns made this activation
        
        # Targeting system
        self.ship_targets = {}  # Dict: ship -> {'primary': ship, 'secondary': ship, 'tertiary': ship}
        self.target_selection_mode = None  # 'primary', 'secondary', or 'tertiary'
        self.all_ships = []  # List of all ships in combat (for targeting)
        
        # Animation system
        self.animating_ship = None  # Which ship is currently animating
        self.animation_start_pos = None  # Starting position for animation
        self.animation_end_pos = None  # Ending position for animation
        self.animation_start_facing = None  # Starting facing for rotation
        self.animation_end_facing = None  # Ending facing for rotation
        self.animation_progress = 0.0  # 0.0 to 1.0
        self.animation_speed = 1.5  # Speed multiplier (lower = slower/smoother)
        self.animation_callback = None  # Function to call when animation completes
        self.pending_ai_moves = []  # Queue of AI moves to execute
        
        # Weapon effects system
        self.active_weapon_effects = []  # List of active weapon effects
        self.phaser_beam_components = {}  # Loaded phaser beam sprites
        self.impact_effects = {}  # Loaded impact effect sprites
        self.torpedo_sprites = {}  # Loaded torpedo sprite sheets
        
        # Arena dimensions (combat space) - define before UI
        self.arena_x = 50
        self.arena_y = 100
        self.arena_width = self.screen_width - 450  # Leave room for side panel
        self.arena_height = self.screen_height - 250  # Leave room for bottom panel
        
        # Hex grid setup
        self.hex_size = 40  # Size of hexagons
        # Center the grid in the arena
        grid_offset_x = self.arena_x + self.arena_width // 2
        grid_offset_y = self.arena_y + self.arena_height // 2
        self.hex_grid = HexGrid(
            hex_size=self.hex_size,
            offset_x=grid_offset_x,
            offset_y=grid_offset_y
        )
        
        # Load ship sprite
        self._load_ship_sprite()
        
        # Load weapon effects
        self._load_weapon_effects()
        
        # Create test ships
        self._create_test_ships()
        
        # Set ship references
        self.selected_ship = self.player_ship
        self.target_ship = self.enemy_ship
        
        # UI elements
        self._create_ui()
        
        self.next_screen = None
        
    def _create_test_ships(self):
        """Create two Odyssey-class ships for testing"""
        from game.ships import get_federation_ship
        
        # Player ship (Odyssey-class)
        self.player_ship = get_federation_ship(
            "Odyssey",
            "Enterprise",
            "NCC-1701-F"
        )
        # Position in hex coordinates (q, r)
        self.player_ship.hex_q = -5
        self.player_ship.hex_r = 0
        self.player_ship.facing = 0  # Facing right (0-5, each step is 60°)
        # Convert hex to pixel for display
        self.player_ship.position = self.hex_grid.axial_to_pixel(
            self.player_ship.hex_q, 
            self.player_ship.hex_r
        )
        
        # Enemy ship (Odyssey-class target)
        self.enemy_ship = get_federation_ship(
            "Odyssey",
            "Target Drone",
            "NX-99999"
        )
        # Position in hex coordinates (q, r)
        self.enemy_ship.hex_q = 10
        self.enemy_ship.hex_r = 0
        self.enemy_ship.facing = 3  # Facing left (180 degrees)
        # Convert hex to pixel for display
        self.enemy_ship.position = self.hex_grid.axial_to_pixel(
            self.enemy_ship.hex_q,
            self.enemy_ship.hex_r
        )
        
        # Don't clutter combat log with initialization - info shown in UI
        self.add_to_log("Combat ready - press SPACE to fire, ENTER to advance")
        
        # Create AI controller for enemy ship
        self.enemy_ai = ShipAI(self.enemy_ship, self.hex_grid)
        self.enemy_ai.set_target(self.player_ship)
        # Apply a personality (can change for testing)
        AIPersonality.apply_to_ai(self.enemy_ai, 'balanced')
        
        # Initialize all ships list and targeting
        self.all_ships = [self.player_ship, self.enemy_ship]
        self.ship_targets = {
            self.player_ship: {'primary': None, 'secondary': None, 'tertiary': None},
            self.enemy_ship: {'primary': None, 'secondary': None, 'tertiary': None}
        }
        
        # Start combat with initiative roll
        self.start_new_turn()
        
    def _load_ship_sprite(self):
        """Load the ship sprite image"""
        import os
        sprite_path = "assets/Ships/Federation/OdysseyClass.png"
        
        try:
            # Check if file exists
            if not os.path.exists(sprite_path):
                raise FileNotFoundError(f"File not found: {sprite_path}")
            
            # Try to load user's ship image
            self.ship_sprite = pygame.image.load(sprite_path).convert_alpha()
            
            # Scale to fit within hex (slightly larger for visibility)
            sprite_size = int(self.hex_size * 2.0)  # 2x hex size for better visibility
            
            # Get original size to maintain aspect ratio
            original_rect = self.ship_sprite.get_rect()
            aspect_ratio = original_rect.width / original_rect.height
            
            if aspect_ratio > 1:  # Wider than tall
                new_width = sprite_size
                new_height = int(sprite_size / aspect_ratio)
            else:  # Taller than wide
                new_height = sprite_size
                new_width = int(sprite_size * aspect_ratio)
            
            self.ship_sprite = pygame.transform.scale(
                self.ship_sprite, 
                (new_width, new_height)
            )
            
            print(f"✓ Loaded ship sprite from {sprite_path}")
            print(f"  Original size: {original_rect.width}x{original_rect.height}")
            print(f"  Scaled to: {new_width}x{new_height} (hex size: {self.hex_size})")
            
        except Exception as e:
            print(f"⚠ Could not load OdysseyClass.png: {e}")
            print(f"  Current directory: {os.getcwd()}")
            print("  Using placeholder. Save your image as assets/Ships/Federation/OdysseyClass.png")
            
            # Create a placeholder if image not found
            sprite_size = int(self.hex_size * 1.5)
            self.ship_sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            
            # Draw a simple ship shape
            center = sprite_size // 2
            # Saucer section
            pygame.draw.circle(self.ship_sprite, LCARS_COLORS['light_blue'], 
                             (center, center - 10), 15)
            # Engineering hull
            pygame.draw.rect(self.ship_sprite, LCARS_COLORS['light_blue'],
                           (center - 5, center, 10, 25))
            # Nacelles
            pygame.draw.rect(self.ship_sprite, LCARS_COLORS['blue'],
                           (center - 20, center + 10, 8, 20))
            pygame.draw.rect(self.ship_sprite, LCARS_COLORS['blue'],
                           (center + 12, center + 10, 8, 20))
    
    def _load_weapon_effects(self):
        """Load weapon effect sprites"""
        import os
        
        try:
            # Load phaser beam components
            phaser_path = "assets/sfx/arrays/phaser"
            self.phaser_beam_components = {
                'head': pygame.image.load(os.path.join(phaser_path, "phaser_head.png")).convert_alpha(),
                'mid': pygame.image.load(os.path.join(phaser_path, "phaser_mid.png")).convert_alpha(),
                'tail': pygame.image.load(os.path.join(phaser_path, "phaser_tail.png")).convert_alpha()
            }
            print("✓ Loaded phaser beam components")
            
            # Load impact effect
            impact_path = "assets/sfx/explosions"
            self.impact_effects['phaser_hit'] = pygame.image.load(
                os.path.join(impact_path, "phaser_hit_sheet.png")
            ).convert_alpha()
            print("✓ Loaded phaser impact effect")
            
            # Load torpedo sprite sheets
            torpedo_path = "assets/sfx/torpedoes"
            torpedo_types = ['photon', 'quantum', 'plasma', 'tricobalt', 'tetryon']
            
            for torp_type in torpedo_types:
                try:
                    filename = f"{torp_type}_sheet.png"
                    self.torpedo_sprites[torp_type] = pygame.image.load(
                        os.path.join(torpedo_path, filename)
                    ).convert_alpha()
                    print(f"✓ Loaded {torp_type} torpedo sprite")
                except Exception as torp_error:
                    print(f"⚠ Could not load {torp_type} torpedo: {torp_error}")
            
        except Exception as e:
            print(f"⚠ Could not load weapon effects: {e}")
            print(f"  Current directory: {os.getcwd()}")
            # Create placeholder effects if needed
            self.phaser_beam_components = {}
            self.impact_effects = {}
            self.torpedo_sprites = {}
            
    def _create_ui(self):
        """Create UI elements"""
        # Panels
        self.arena_panel = Panel(
            self.arena_x - 10, 
            self.arena_y - 10, 
            self.arena_width + 20, 
            self.arena_height + 20,
            color='bg_dark', 
            border_color='blue'
        )
        
        # Right side tabbed panel for ship status
        panel_x = self.screen_width - 380
        from gui.components import TabbedPanel
        self.status_panel = TabbedPanel(
            panel_x, 170, 360, 530,
            tabs=['STATUS', 'WEAPONS', 'POWER', 'DAMAGE']
        )
        
        # Bottom panel for combat log (match arena width)
        self.log_panel = Panel(
            self.arena_x, self.screen_height - 130, 
            self.arena_width, 110,  # Use arena_width instead of screen_width - 400
            color='bg_medium',
            border_color='orange'
        )
        
        # Action buttons
        button_x = panel_x + 20
        button_y = 720
        button_spacing = 60
        
        self.fire_button = Button(
            button_x, button_y, 320, 50,
            "FIRE WEAPONS", color='alert_red',
            callback=self.fire_weapons
        )
        
        self.end_turn_button = Button(
            button_x, button_y + button_spacing, 320, 50,
            "NEXT PHASE", color='green',
            callback=self.end_turn
        )
        
        self.reset_button = Button(
            button_x, button_y + button_spacing * 2, 320, 50,
            "RESET ARENA", color='purple',
            callback=self.reset_arena
        )
        
        self.exit_button = Button(
            button_x, button_y + button_spacing * 3, 320, 50,
            "EXIT TO MENU", color='orange',
            callback=self.exit_to_menu
        )
        
        self.buttons = [
            self.fire_button,
            self.end_turn_button,
            self.reset_button,
            self.exit_button
        ]
        
    def add_to_log(self, message):
        """Add message to combat log"""
        self.combat_log.append(message)
        # Keep only last 2 messages to prevent overlap
        if len(self.combat_log) > 2:
            self.combat_log.pop(0)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMBAT PHASE SYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    def start_new_turn(self):
        """Start a new combat turn with initiative phase"""
        self.turn_number += 1
        self.combat_phase = "initiative"
        self.current_ship_index = 0
        self.actions_completed = {k: False for k in self.actions_completed}
        
        # Roll initiative
        self.roll_initiative()
        
        # Don't clutter combat log with turn info - it's shown in top right
        
        # Auto-advance to movement phase
        self.advance_phase()
    
    def roll_initiative(self):
        """Determine turn order based on command skill"""
        # TEMPORARILY DISABLED - Player always goes first for testing
        # import random
        # 
        # ships = [self.player_ship, self.enemy_ship]
        # initiative_rolls = []
        # 
        # for ship in ships:
        #     # Base initiative from command crew skill (if present)
        #     base_initiative = 0
        #     if ship.command_crew.get('captain'):
        #         base_initiative = ship.command_crew['captain'].attributes.get('command', 50)
        #     
        #     # Add random d20 roll
        #     roll = random.randint(1, 20)
        #     total = base_initiative + roll
        #     
        #     initiative_rolls.append((ship, total, roll))
        # 
        # # Sort by total (highest first)
        # initiative_rolls.sort(key=lambda x: x[1], reverse=True)
        # self.initiative_order = [ship for ship, total, roll in initiative_rolls]
        
        # TESTING: Player always wins initiative
        self.initiative_order = [self.player_ship, self.enemy_ship]
    
    def advance_phase(self):
        """Move to next combat phase"""
        current_index = self.phase_order.index(self.combat_phase)
        
        # Check if current phase is complete
        if not self.is_phase_complete():
            return  # Phase not done yet
        
        # Move to next phase
        if current_index < len(self.phase_order) - 1:
            self.combat_phase = self.phase_order[current_index + 1]
            self.current_ship_index = 0
            
            # Don't log phase transitions - shown in top right UI
            
            # Initialize movement phase for first ship
            if self.combat_phase == "movement" and len(self.initiative_order) > 0:
                self.start_movement_phase(self.initiative_order[0])
            
            # Initialize targeting phase for first ship
            if self.combat_phase == "targeting" and len(self.initiative_order) > 0:
                first_ship = self.initiative_order[0]
                if first_ship == self.player_ship:
                    self.start_player_targeting()
                else:
                    # AI targeting will be triggered by complete_ship_action
                    pygame.time.set_timer(pygame.USEREVENT + 4, 300)
            
            # Auto-resolve certain phases
            if self.combat_phase == "damage":
                self.resolve_damage_phase()
            elif self.combat_phase == "housekeeping":
                self.resolve_housekeeping_phase()
        else:
            # End of turn, start new turn
            self.start_new_turn()
    
    def is_phase_complete(self):
        """Check if current phase is complete"""
        if self.combat_phase == "initiative":
            return True  # Always complete immediately
        elif self.combat_phase in ["damage", "housekeeping"]:
            return True  # Auto-resolved
        elif self.combat_phase in ["movement", "targeting", "firing", "power", "repair"]:
            # Check if all ships have acted
            return self.current_ship_index >= len(self.initiative_order)
        return True
    
    def resolve_damage_phase(self):
        """Apply pending damage effects"""
        # Future: Apply system damage, hull breaches, crew casualties
        # Don't log auto-resolved phases
        self.advance_phase()
    
    def resolve_housekeeping_phase(self):
        """End-of-turn cleanup"""
        # Advance weapon cooldowns
        for ship in self.initiative_order:
            ship.advance_all_weapon_cooldowns()
        
        # Future: Shield regeneration, power recharge, etc.
        # Don't log housekeeping
        self.advance_phase()
    
    def get_current_acting_ship(self):
        """Get the ship that should act in current phase"""
        if self.current_ship_index < len(self.initiative_order):
            return self.initiative_order[self.current_ship_index]
        return None
    
    def complete_ship_action(self):
        """Mark current ship's action as complete, move to next ship"""
        self.current_ship_index += 1
        
        if self.current_ship_index >= len(self.initiative_order):
            # All ships acted, advance phase
            self.advance_phase()
        else:
            # Initialize movement for next ship if in movement phase
            if self.combat_phase == "movement":
                next_ship = self.get_current_acting_ship()
                self.start_movement_phase(next_ship)
            # Execute AI targeting if it's enemy's turn in targeting phase
            elif self.combat_phase == "targeting":
                next_ship = self.get_current_acting_ship()
                if next_ship == self.enemy_ship:
                    # AI auto-selects targets
                    pygame.time.set_timer(pygame.USEREVENT + 4, 300)
            # Execute AI firing if it's enemy's turn in firing phase
            elif self.combat_phase == "firing":
                next_ship = self.get_current_acting_ship()
                if next_ship == self.enemy_ship:
                    # Delay AI firing slightly for visual clarity
                    pygame.time.set_timer(pygame.USEREVENT + 3, 500)
        # Don't log ship turns - shown in top right UI
    
    # ═══════════════════════════════════════════════════════════════════
    # MOVEMENT SYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    def start_movement_phase(self, ship):
        """Initialize movement points for a ship"""
        # Get impulse speed (movement points available)
        self.movement_points_remaining = ship.impulse_speed
        self.movement_points_used = 0
        self.has_moved_this_turn = False
        self.turns_this_activation = 0
        self.add_to_log(f"{ship.name}: {self.movement_points_remaining} movement points")
        
        # If this is AI ship, execute AI movement
        if ship == self.enemy_ship:
            self.execute_ai_movement()
    
    def can_move(self, ship):
        """Check if ship can perform movement action"""
        return (self.combat_phase == "movement" and 
                self.get_current_acting_ship() == ship and
                self.movement_points_remaining > 0)
    
    def move_forward(self, ship):
        """Move ship forward one hex (costs 1 movement point)"""
        # Check if it's this ship's turn and in movement phase
        if self.combat_phase != "movement":
            return False
        
        current_ship = self.get_current_acting_ship()
        if current_ship != ship:
            self.add_to_log("Not your turn to move!")
            return False
        
        if self.movement_points_remaining < 1:
            self.add_to_log("No movement points left!")
            return False
        
        # Calculate forward hex based on facing
        # Hex facing: 0=E, 1=SE, 2=SW, 3=W, 4=NW, 5=NE
        direction_vectors = [
            (1, 0),   # 0: East
            (0, 1),   # 1: Southeast
            (-1, 1),  # 2: Southwest
            (-1, 0),  # 3: West
            (0, -1),  # 4: Northwest
            (1, -1),  # 5: Northeast
        ]
        
        dq, dr = direction_vectors[ship.facing]
        new_q = ship.hex_q + dq
        new_r = ship.hex_r + dr
        
        # Calculate new pixel position
        old_pos = ship.position
        new_pos = self.hex_grid.axial_to_pixel(new_q, new_r)
        
        # Update hex coordinates immediately
        ship.hex_q = new_q
        ship.hex_r = new_r
        
        # Start animation from old to new position
        self.start_ship_animation(ship, old_pos, new_pos)
        
        self.movement_points_remaining -= 1
        self.movement_points_used += 1
        self.has_moved_this_turn = True  # Mark that ship has moved
        self.turns_this_activation = 0  # Reset turn counter after moving
        self.add_to_log(f"Moved forward ({self.movement_points_remaining} pts left)")
        return True
    
    def move_backward(self, ship):
        """Move ship backward one hex (costs 1 movement point)"""
        # Check if it's this ship's turn and in movement phase
        if self.combat_phase != "movement":
            return False
        
        current_ship = self.get_current_acting_ship()
        if current_ship != ship:
            self.add_to_log("Not your turn to move!")
            return False
        
        if self.movement_points_remaining < 1:
            self.add_to_log("No movement points left!")
            return False
        
        # Move opposite of facing direction
        direction_vectors = [
            (1, 0),   # 0: East
            (0, 1),   # 1: Southeast
            (-1, 1),  # 2: Southwest
            (-1, 0),  # 3: West
            (0, -1),  # 4: Northwest
            (1, -1),  # 5: Northeast
        ]
        
        dq, dr = direction_vectors[ship.facing]
        new_q = ship.hex_q - dq  # Opposite direction
        new_r = ship.hex_r - dr
        
        # Calculate new pixel position
        old_pos = ship.position
        new_pos = self.hex_grid.axial_to_pixel(new_q, new_r)
        
        # Update hex coordinates immediately
        ship.hex_q = new_q
        ship.hex_r = new_r
        
        # Start animation from old to new position
        self.start_ship_animation(ship, old_pos, new_pos)
        
        self.movement_points_remaining -= 1
        self.movement_points_used += 1
        self.has_moved_this_turn = True  # Mark that ship has moved
        self.turns_this_activation = 0  # Reset turn counter after moving
        self.add_to_log(f"Moved backward ({self.movement_points_remaining} pts left)")
        return True
    
    def turn_left(self, ship):
        """Turn ship left (counterclockwise) one facing (costs 1 movement point)"""
        # Check if it's this ship's turn and in movement phase
        if self.combat_phase != "movement":
            return False
        
        current_ship = self.get_current_acting_ship()
        if current_ship != ship:
            self.add_to_log("Not your turn to move!")
            return False
        
        if self.movement_points_remaining < 1:
            self.add_to_log("No movement points left!")
            return False
        
        # TURNING RULES: Must move forward/backward before turning
        if not self.has_moved_this_turn:
            self.add_to_log("Must move before turning!")
            return False
        
        # TURNING RULES: Can only turn once per hex moved
        if self.turns_this_activation >= 1:
            self.add_to_log("Already turned! Move again to turn more.")
            return False
        
        # Store old facing for animation
        old_facing = ship.facing
        
        # Turn counterclockwise (facing 0-5)
        new_facing = (ship.facing - 1) % 6
        ship.facing = new_facing
        
        # Start rotation animation
        self.start_ship_animation(
            ship,
            start_facing=old_facing,
            end_facing=new_facing
        )
        
        self.movement_points_remaining -= 1
        self.movement_points_used += 1
        self.turns_this_activation += 1
        self.add_to_log(f"Turned left ({self.movement_points_remaining} pts left)")
        return True
    
    def turn_right(self, ship):
        """Turn ship right (clockwise) one facing (costs 1 movement point)"""
        # Check if it's this ship's turn and in movement phase
        if self.combat_phase != "movement":
            return False
        
        current_ship = self.get_current_acting_ship()
        if current_ship != ship:
            self.add_to_log("Not your turn to move!")
            return False
        
        if self.movement_points_remaining < 1:
            self.add_to_log("No movement points left!")
            return False
        
        # TURNING RULES: Must move forward/backward before turning
        if not self.has_moved_this_turn:
            self.add_to_log("Must move before turning!")
            return False
        
        # TURNING RULES: Can only turn once per hex moved
        if self.turns_this_activation >= 1:
            self.add_to_log("Already turned! Move again to turn more.")
            return False
        
        # Store old facing for animation
        old_facing = ship.facing
        
        # Turn clockwise (facing 0-5)
        new_facing = (ship.facing + 1) % 6
        ship.facing = new_facing
        
        # Start rotation animation
        self.start_ship_animation(
            ship,
            start_facing=old_facing,
            end_facing=new_facing
        )
        
        self.movement_points_remaining -= 1
        self.movement_points_used += 1
        self.turns_this_activation += 1
        self.add_to_log(f"Turned right ({self.movement_points_remaining} pts left)")
        return True
    
    # ═══════════════════════════════════════════════════════════════════
    # AI EXECUTION
    # ═══════════════════════════════════════════════════════════════════
    
    def execute_ai_movement(self):
        """Execute AI-controlled ship movement"""
        ship = self.enemy_ship
        
        # Get AI movement decisions
        moves = self.enemy_ai.decide_movement(self.movement_points_remaining)
        
        # Queue up moves to execute with animation
        self.pending_ai_moves.clear()
        
        for move_command in moves:
            if move_command == 'forward':
                self.pending_ai_moves.append(lambda s=ship: self.move_forward(s))
            elif move_command == 'backward':
                self.pending_ai_moves.append(lambda s=ship: self.move_backward(s))
            elif move_command == 'turn_left':
                self.pending_ai_moves.append(lambda s=ship: self.turn_left(s))
            elif move_command == 'turn_right':
                self.pending_ai_moves.append(lambda s=ship: self.turn_right(s))
        
        # Add completion callback as final action
        self.pending_ai_moves.append(lambda: pygame.time.set_timer(pygame.USEREVENT + 2, 500))
    
    def execute_ai_firing(self):
        """Execute AI-controlled ship firing"""
        ship = self.enemy_ship
        
        # Get targets from targeting phase
        targets = self.ship_targets.get(ship, {})
        primary = targets.get('primary')
        secondary = targets.get('secondary')
        tertiary = targets.get('tertiary')
        
        # Fire at each target with appropriate accuracy penalties
        if primary:
            self._fire_at_target(ship, primary, 1.0, "PRIMARY")
        
        if secondary:
            self._fire_at_target(ship, secondary, 0.75, "SECONDARY")
        
        if tertiary:
            self._fire_at_target(ship, tertiary, 0.5, "TERTIARY")
        
        # Mark action complete
        self.complete_ship_action()
    
    # ═══════════════════════════════════════════════════════════════════
    # TARGETING SYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    def select_target(self, attacker, target, priority='primary'):
        """
        Select a target for a ship
        
        Args:
            attacker: Ship doing the targeting
            target: Ship being targeted
            priority: 'primary', 'secondary', or 'tertiary'
        """
        if attacker not in self.ship_targets:
            self.ship_targets[attacker] = {'primary': None, 'secondary': None, 'tertiary': None}
        
        self.ship_targets[attacker][priority] = target
        
        priority_text = priority.upper()
        if target:
            self.add_to_log(f"{attacker.name}: {priority_text} target = {target.name}")
        else:
            self.add_to_log(f"{attacker.name}: {priority_text} target cleared")
    
    def get_available_targets(self, attacker):
        """Get list of valid targets for a ship (all ships except self)"""
        return [ship for ship in self.all_ships if ship != attacker and ship.hull > 0]
    
    def execute_ai_targeting(self):
        """AI automatically selects targets"""
        ship = self.enemy_ship
        available_targets = self.get_available_targets(ship)
        
        if len(available_targets) == 0:
            self.add_to_log(f"{ship.name}: No valid targets!")
            self.complete_ship_action()
            return
        
        # AI simple targeting: primary target only (closest enemy)
        # Calculate distances
        target_distances = []
        for target in available_targets:
            dist = self.hex_grid.distance(
                ship.hex_q, ship.hex_r,
                target.hex_q, target.hex_r
            )
            target_distances.append((target, dist))
        
        # Sort by distance
        target_distances.sort(key=lambda x: x[1])
        
        # Select closest as primary
        primary_target = target_distances[0][0]
        self.select_target(ship, primary_target, 'primary')
        
        # If multiple targets available, select secondary
        if len(target_distances) > 1:
            secondary_target = target_distances[1][0]
            self.select_target(ship, secondary_target, 'secondary')
        
        # If 3+ targets, select tertiary
        if len(target_distances) > 2:
            tertiary_target = target_distances[2][0]
            self.select_target(ship, tertiary_target, 'tertiary')
        
        # Complete targeting
        self.complete_ship_action()
    
    def start_player_targeting(self):
        """Start player targeting selection"""
        self.target_selection_mode = 'primary'
        self.add_to_log("Select PRIMARY target (1-3 to cycle priority, CLICK ship, ENTER to skip)")
    
    def cycle_target_priority(self):
        """Cycle through target priority levels"""
        if self.target_selection_mode == 'primary':
            self.target_selection_mode = 'secondary'
            self.add_to_log("Select SECONDARY target (-25% accuracy)")
        elif self.target_selection_mode == 'secondary':
            self.target_selection_mode = 'tertiary'
            self.add_to_log("Select TERTIARY target (-50% accuracy)")
        else:
            self.target_selection_mode = 'primary'
            self.add_to_log("Select PRIMARY target (normal accuracy)")
            
    def fire_weapons(self):
        """Fire all ready weapons at selected targets"""
        # Check if it's firing phase
        if self.combat_phase != "firing":
            self.add_to_log(f"Not firing phase! (Currently: {self.combat_phase})")
            return
        
        # Check if it's player's turn to fire
        current_ship = self.get_current_acting_ship()
        if current_ship != self.player_ship:
            self.add_to_log("Not your turn to fire!")
            return
            
        attacker = self.player_ship
        
        # Get targets from targeting phase
        targets = self.ship_targets.get(attacker, {})
        primary = targets.get('primary')
        secondary = targets.get('secondary')
        tertiary = targets.get('tertiary')
        
        # Fire at each target with appropriate accuracy penalties
        fired_at_any = False
        
        if primary:
            self._fire_at_target(attacker, primary, 1.0, "PRIMARY")
            fired_at_any = True
        
        if secondary:
            self._fire_at_target(attacker, secondary, 0.75, "SECONDARY")
            fired_at_any = True
        
        if tertiary:
            self._fire_at_target(attacker, tertiary, 0.5, "TERTIARY")
            fired_at_any = True
        
        if not fired_at_any:
            self.add_to_log("No targets selected!")
        
        # Check if any target destroyed
        for target in [primary, secondary, tertiary]:
            if target and target.hull <= 0:
                self.add_to_log(f"*** {target.name} DESTROYED! ***")
        
        # Mark action complete
        self.complete_ship_action()
    
    def _fire_at_target(self, attacker, target, accuracy_penalty, target_label):
        """Fire weapons at a specific target with accuracy penalty
        
        Args:
            attacker: Ship firing weapons
            target: Ship being fired at
            accuracy_penalty: Multiplier for accuracy (1.0=normal, 0.75=secondary, 0.5=tertiary)
            target_label: String label for logging
        """
        # Calculate distance in hex coordinates
        distance = self.hex_grid.distance(
            attacker.hex_q, attacker.hex_r,
            target.hex_q, target.hex_r
        )
        
        if target.hull <= 0:
            return  # Don't shoot destroyed targets
        
        # Calculate target arc (for weapon firing arcs)
        target_arc = attacker.get_target_arc(target.hex_q, target.hex_r)
        
        # Calculate which shield facing is being hit on the target
        shield_facing_hit = target.get_shield_facing_hit(attacker.hex_q, attacker.hex_r)
        
        self.add_to_log(f"--- {target_label} {target.name}: {distance} hexes, hitting {shield_facing_hit.upper()} shields ---")
        
        # Fire energy weapons
        crew_bonus = attacker.get_crew_bonus()
        for weapon in attacker.weapon_arrays:
            if weapon.can_fire():
                # Check if weapon is in arc
                if target_arc not in weapon.firing_arcs:
                    continue
                
                # Check if phasers are in range (max 12 hexes)
                if distance > 12:
                    continue
                
                damage = weapon.fire(crew_bonus)
                
                # Apply sensor accuracy modifier
                accuracy_mod = attacker.get_targeting_accuracy(distance)
                if accuracy_mod is None:
                    continue
                
                # Apply multi-target accuracy penalty
                accuracy_mod *= accuracy_penalty
                    
                actual_damage = int(damage * accuracy_mod)
                
                # Create visual effect for energy weapon beam
                if self.phaser_beam_components:
                    # Get ship positions
                    attacker_pos = attacker.position if attacker.position else self.hex_grid.axial_to_pixel(attacker.hex_q, attacker.hex_r)
                    target_pos = target.position if target.position else self.hex_grid.axial_to_pixel(target.hex_q, target.hex_r)
                    
                    # Get weapon's visual effect type
                    weapon_effect_type = weapon.get_visual_effect_type()
                    
                    # Create beam effect using weapon-specific properties
                    beam_effect = WeaponBeamEffect(
                        attacker_pos,
                        target_pos,
                        self.phaser_beam_components,
                        self.impact_effects.get('phaser_hit'),
                        weapon_type=weapon.weapon_type
                    )
                    self.active_weapon_effects.append(beam_effect)
                
                # Energy weapons: 100% absorbed by shields, remainder to hull
                shield_damage = actual_damage
                hull_damage = 0
                
                # Hit the correct shield facing
                if shield_facing_hit in target.shields:
                    target.shields[shield_facing_hit] -= shield_damage
                    
                    # If shields collapse, excess damage bleeds to hull
                    if target.shields[shield_facing_hit] < 0:
                        hull_damage = abs(target.shields[shield_facing_hit])
                        target.shields[shield_facing_hit] = 0
                        target.hull -= hull_damage
                        target.hull = max(0, target.hull)
                
                penalty_text = f" ({int(accuracy_penalty*100)}%)" if accuracy_penalty < 1.0 else ""
                if hull_damage > 0:
                    self.add_to_log(
                        f"{weapon.weapon_type.upper()}: {shield_damage} shield, {hull_damage} hull{penalty_text}"
                    )
                else:
                    self.add_to_log(
                        f"{weapon.weapon_type.upper()}: {shield_damage} to {shield_facing_hit} shields{penalty_text}"
                    )
        
        # Fire torpedoes
        for torpedo in attacker.torpedo_bays:
            if torpedo.can_fire():
                # Check if torpedo is in arc
                if target_arc not in torpedo.firing_arcs:
                    continue
                
                # Check if torpedoes are in range (max 15 hexes)
                if distance > 15:
                    continue
                
                damage = torpedo.fire(crew_bonus)
                
                # Create visual effect for torpedo
                if self.torpedo_sprites.get(torpedo.torpedo_type):
                    # Get ship positions
                    attacker_pos = attacker.position if attacker.position else self.hex_grid.axial_to_pixel(attacker.hex_q, attacker.hex_r)
                    target_pos = target.position if target.position else self.hex_grid.axial_to_pixel(target.hex_q, target.hex_r)
                    
                    # Create torpedo projectile effect
                    torpedo_effect = TorpedoProjectileEffect(
                        attacker_pos,
                        target_pos,
                        self.torpedo_sprites.get(torpedo.torpedo_type),
                        self.impact_effects.get('phaser_hit'),  # Use same explosion for now
                        torpedo_type=torpedo.torpedo_type
                    )
                    self.active_weapon_effects.append(torpedo_effect)
                
                # Apply sensor accuracy
                accuracy_mod = attacker.get_targeting_accuracy(distance)
                if accuracy_mod is None:
                    continue
                
                # Apply multi-target accuracy penalty
                accuracy_mod *= accuracy_penalty
                    
                actual_damage = int(damage * accuracy_mod)
                
                # Torpedoes: 90% blocked by shields, 10% bleeds through to hull
                shield_damage = int(actual_damage * 0.9)
                hull_damage = int(actual_damage * 0.1)
                
                # Hit the correct shield facing
                if shield_facing_hit in target.shields:
                    target.shields[shield_facing_hit] -= shield_damage
                    
                    # If shields collapse, add excess to hull damage
                    if target.shields[shield_facing_hit] < 0:
                        hull_damage += abs(target.shields[shield_facing_hit])
                        target.shields[shield_facing_hit] = 0
                    
                # Apply hull damage
                target.hull -= hull_damage
                target.hull = max(0, target.hull)
                
                penalty_text = f" ({int(accuracy_penalty*100)}%)" if accuracy_penalty < 1.0 else ""
                self.add_to_log(
                    f"TORPEDO: {shield_damage} to {shield_facing_hit} shields, {hull_damage} hull{penalty_text}"
                )
            
    def end_turn(self):
        """Advance to next phase or skip current ship's action"""
        current_ship = self.get_current_acting_ship()
        
        # If it's player's turn, skip their action
        if current_ship == self.player_ship:
            # Don't log pass actions - just skip quietly
            self.complete_ship_action()
        else:
            # Not player's turn, just advance phase
            self.advance_phase()
        
    def reset_arena(self):
        """Reset the combat arena"""
        self._create_test_ships()
        self.turn_number = 0  # Will be 1 after start_new_turn
        self.player_turn = True
        self.combat_log.clear()
        self.combat_phase = "initiative"
        self.current_ship_index = 0
        self.actions_completed = {k: False for k in self.actions_completed}
        
        # Recreate AI controller
        self.enemy_ai = ShipAI(self.enemy_ship, self.hex_grid)
        self.enemy_ai.set_target(self.player_ship)
        AIPersonality.apply_to_ai(self.enemy_ai, 'balanced')
        
        # Clear animation state
        self.animating_ship = None
        self.animation_start_pos = None
        self.animation_end_pos = None
        self.animation_start_facing = None
        self.animation_end_facing = None
        self.animation_progress = 0.0
        self.animation_callback = None
        self.pending_ai_moves.clear()
        
        # Clear ship animation attributes
        if hasattr(self.player_ship, '_anim_facing'):
            delattr(self.player_ship, '_anim_facing')
        if hasattr(self.enemy_ship, '_anim_facing'):
            delattr(self.enemy_ship, '_anim_facing')
        
        self.add_to_log("Arena reset")
        # Start new combat
        self.start_new_turn()
        
    def exit_to_menu(self):
        """Return to main menu"""
        self.next_screen = "main_menu"
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_to_menu()
                elif event.key == pygame.K_SPACE:
                    if self.combat_phase == "firing":
                        self.fire_weapons()
                elif event.key == pygame.K_RETURN:
                    self.end_turn()  # Advances phase or skips action
                elif event.key == pygame.K_r:
                    self.reset_arena()
                # WASD Movement controls (only if not animating)
                elif event.key == pygame.K_w:
                    if self.combat_phase == "movement" and not self.is_animating():
                        self.move_forward(self.player_ship)
                elif event.key == pygame.K_s:
                    if self.combat_phase == "movement" and not self.is_animating():
                        self.move_backward(self.player_ship)
                elif event.key == pygame.K_a:
                    if self.combat_phase == "movement" and not self.is_animating():
                        self.turn_left(self.player_ship)
                elif event.key == pygame.K_d:
                    if self.combat_phase == "movement" and not self.is_animating():
                        self.turn_right(self.player_ship)
                # Targeting controls
                elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    if self.combat_phase == "targeting":
                        self.cycle_target_priority()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if clicked on status panel tab
                    if self.status_panel.handle_click(mouse_pos):
                        continue  # Tab was clicked, don't process other clicks
                    
                    if self.combat_phase == "targeting":
                        current_ship = self.get_current_acting_ship()
                        if current_ship == self.player_ship and self.target_selection_mode:
                            # Check if clicked on a ship
                            for ship in self.get_available_targets(current_ship):
                                ship_pos = ship.position
                                if ship_pos:
                                    dx = mouse_pos[0] - ship_pos[0]
                                    dy = mouse_pos[1] - ship_pos[1]
                                    dist = (dx*dx + dy*dy) ** 0.5
                                    if dist < 50:  # Within 50 pixels
                                        self.select_target(current_ship, ship, self.target_selection_mode)
                                        break
                    
            elif event.type == pygame.USEREVENT + 1:
                # Timer for auto-advancing turn
                self.next_player_turn()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
            
            elif event.type == pygame.USEREVENT + 2:
                # Timer for AI movement completion
                self.complete_ship_action()
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Cancel timer
            
            elif event.type == pygame.USEREVENT + 3:
                # Timer for AI firing
                self.execute_ai_firing()
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)  # Cancel timer
            
            elif event.type == pygame.USEREVENT + 4:
                # Timer for AI targeting
                self.execute_ai_targeting()
                pygame.time.set_timer(pygame.USEREVENT + 4, 0)  # Cancel timer
                
            # Handle button events
            for button in self.buttons:
                button.handle_event(event)
                        
    def update(self, dt):
        """Update combat state"""
        # Update weapon effects
        self.active_weapon_effects = [
            effect for effect in self.active_weapon_effects 
            if effect.update(dt)
        ]
        
        # Update movement animations
        if self.animating_ship is not None:
            self.animation_progress += dt * self.animation_speed
            
            if self.animation_progress >= 1.0:
                # Animation complete
                self.animation_progress = 1.0
                # Snap to final position and facing
                if self.animation_end_pos is not None:
                    self.animating_ship.position = self.animation_end_pos
                if self.animation_end_facing is not None:
                    self.animating_ship.facing = self.animation_end_facing
                    # Clear animation facing
                    if hasattr(self.animating_ship, '_anim_facing'):
                        delattr(self.animating_ship, '_anim_facing')
                
                # Call callback if set
                if self.animation_callback:
                    callback = self.animation_callback
                    self.animation_callback = None
                    callback()
                
                # Clear animation state
                self.animating_ship = None
                self.animation_start_pos = None
                self.animation_end_pos = None
                self.animation_start_facing = None
                self.animation_end_facing = None
                self.animation_progress = 0.0
            else:
                # Interpolate position (smooth ease-in-out)
                t = self.animation_progress
                # Ease-in-out cubic for smooth motion
                t = t * t * (3.0 - 2.0 * t)
                
                # Position interpolation
                if self.animation_start_pos and self.animation_end_pos:
                    start_x, start_y = self.animation_start_pos
                    end_x, end_y = self.animation_end_pos
                    
                    current_x = start_x + (end_x - start_x) * t
                    current_y = start_y + (end_y - start_y) * t
                    
                    self.animating_ship.position = (current_x, current_y)
                
                # Facing interpolation (for smooth rotation)
                if self.animation_start_facing is not None and self.animation_end_facing is not None:
                    # Calculate shortest rotation path
                    start_f = self.animation_start_facing
                    end_f = self.animation_end_facing
                    
                    # Handle wrap-around (e.g., 5 -> 0 should go forward, not backward)
                    diff = end_f - start_f
                    if diff > 3:  # Going around the long way
                        diff -= 6
                    elif diff < -3:
                        diff += 6
                    
                    # Interpolate facing as a float, then store in temp variable
                    current_facing_float = start_f + diff * t
                    
                    # Normalize to 0-5 range
                    while current_facing_float < 0:
                        current_facing_float += 6
                    while current_facing_float >= 6:
                        current_facing_float -= 6
                    
                    # Store as attribute for drawing (will be rounded in _draw_ship)
                    self.animating_ship._anim_facing = current_facing_float
        
        # Process pending AI moves
        elif len(self.pending_ai_moves) > 0 and self.animating_ship is None:
            # Execute next move in queue
            next_move = self.pending_ai_moves.pop(0)
            next_move()  # Execute the move function
    
    def start_ship_animation(self, ship, start_pos=None, end_pos=None, start_facing=None, end_facing=None, callback=None):
        """
        Start a smooth animation for ship movement and/or rotation
        
        Args:
            ship: Ship to animate
            start_pos: (x, y) starting pixel position (optional)
            end_pos: (x, y) ending pixel position (optional)
            start_facing: Starting facing direction 0-5 (optional)
            end_facing: Ending facing direction 0-5 (optional)
            callback: Optional function to call when animation completes
        """
        self.animating_ship = ship
        self.animation_start_pos = start_pos
        self.animation_end_pos = end_pos
        self.animation_start_facing = start_facing
        self.animation_end_facing = end_facing
        self.animation_progress = 0.0
        self.animation_callback = callback
        
        # Initialize animation facing if rotating
        if start_facing is not None:
            ship._anim_facing = float(start_facing)
    
    def is_animating(self):
        """Check if any ship is currently animating"""
        return self.animating_ship is not None
            
    def draw(self):
        """Draw the combat test screen"""
        # Background
        self.screen.fill(LCARS_COLORS['bg_dark'])
        
        # Draw panels
        self.arena_panel.draw(self.screen)
        self.status_panel.draw_background(self.screen)
        self.status_panel.draw_tabs(self.screen, self.font_small)
        self.log_panel.draw(self.screen)
        
        # Header
        title = self.font_large.render("COMBAT TEST ARENA", True, get_accent_color())
        title_rect = title.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Set clipping rect to arena area only
        arena_rect = pygame.Rect(
            self.arena_x, 
            self.arena_y, 
            self.arena_width, 
            self.arena_height
        )
        self.screen.set_clip(arena_rect)
        
        # Draw arena grid (optional - helps visualize range)
        self._draw_arena_grid()
        
        # Draw ships
        self._draw_ship(self.player_ship, LCARS_COLORS['blue'])
        self._draw_ship(self.enemy_ship, LCARS_COLORS['alert_red'])
        
        # Draw targeting lines (only when targets are selected)
        self._draw_targeting_lines()
        
        # Draw weapon effects (beams, impacts, etc.)
        for effect in self.active_weapon_effects:
            effect.draw(self.screen)
        
        # Remove clipping - allow drawing outside arena for UI elements
        self.screen.set_clip(None)
        
        # Draw ship status (right panel)
        self._draw_ship_status()
        
        # Draw combat log (bottom panel)
        self._draw_combat_log()
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.font_medium)
            
        # Draw turn indicator
        turn_text = f"TURN {self.turn_number}"
        turn_surface = self.font_medium.render(turn_text, True, LCARS_COLORS['light_blue'])
        self.screen.blit(turn_surface, (self.screen_width - 380, 60))
        
        # Draw current acting ship and phase
        current_ship = self.get_current_acting_ship()
        if current_ship:
            if current_ship == self.player_ship:
                status_text = "YOUR TURN"
                status_color = LCARS_COLORS['green']
            else:
                status_text = f"{current_ship.name.upper()}'S TURN"
                status_color = LCARS_COLORS['alert_red']
            status_surface = self.font_small.render(status_text, True, status_color)
            self.screen.blit(status_surface, (self.screen_width - 380, 90))
        
        # Draw phase indicator below
        phase_text = f"{self.combat_phase.upper()} PHASE"
        phase_color = get_accent_color()
        phase_surface = self.font_small.render(phase_text, True, phase_color)
        self.screen.blit(phase_surface, (self.screen_width - 380, 115))
        
        # Draw movement points if in movement phase
        if self.combat_phase == "movement" and current_ship == self.player_ship:
            mp_text = f"MOVEMENT: {self.movement_points_remaining}/{self.player_ship.impulse_speed}"
            mp_surface = self.font_small.render(mp_text, True, LCARS_COLORS['green'])
            self.screen.blit(mp_surface, (self.screen_width - 380, 140))
        
        # Draw controls hint - positioned well above combat log
        hint_y = self.screen_height - 160  # Much higher to avoid combat log overlap
        
        # Change hint based on phase
        if self.combat_phase == "movement" and current_ship == self.player_ship:
            hint_text = "WASD: Move/Turn | ENTER: End Movement | R: Reset | ESC: Exit"
        elif self.combat_phase == "targeting" and current_ship == self.player_ship:
            priority_text = f"[{self.target_selection_mode.upper()}]" if self.target_selection_mode else ""
            hint_text = f"CLICK: Select Target {priority_text} | 1-3: Change Priority | ENTER: Done | R: Reset"
        elif self.combat_phase == "firing":
            hint_text = "SPACE: Fire | ENTER: Next Phase | R: Reset | ESC: Exit"
        else:
            hint_text = "ENTER: Next Phase | R: Reset | ESC: Exit"
        
        hint_surface = self.font_small.render(hint_text, True, LCARS_COLORS['text_gray'])
        hint_rect = hint_surface.get_rect(center=(self.screen_width // 2, hint_y))
        self.screen.blit(hint_surface, hint_rect)
        
        pygame.display.flip()
        
    def _draw_arena_grid(self):
        """Draw hexagonal grid in the arena"""
        grid_color = LCARS_COLORS['blue']
        
        # Draw hex grid - larger range to ensure full coverage
        # Calculate how many hexes fit in arena (with extra padding)
        hex_width = self.hex_size * math.sqrt(3)  # Width of hex
        hex_height = self.hex_size * 1.5  # Vertical spacing
        
        hex_cols = int(self.arena_width / hex_width) + 4  # Extra padding
        hex_rows = int(self.arena_height / hex_height) + 4  # Extra padding
        
        # Draw centered grid with wider range
        min_q = -hex_cols // 2 - 2
        max_q = hex_cols // 2 + 2
        min_r = -hex_rows // 2 - 2
        max_r = hex_rows // 2 + 2
        
        # Draw all hexes
        self.hex_grid.draw_grid(
            self.screen,
            min_q, max_q,
            min_r, max_r,
            grid_color,
            1  # Line width
        )
        
        # Highlight ship hexes with thicker, colored borders
        # Player ship hex (blue highlight)
        self.hex_grid.draw_hex(
            self.screen,
            self.player_ship.hex_q,
            self.player_ship.hex_r,
            LCARS_COLORS['light_blue'],
            3  # Thicker border
        )
        
        # Enemy ship hex (red highlight)
        self.hex_grid.draw_hex(
            self.screen,
            self.enemy_ship.hex_q,
            self.enemy_ship.hex_r,
            LCARS_COLORS['alert_red'],
            3  # Thicker border
        )
            
    def _draw_ship(self, ship, color):
        """Draw a ship sprite"""
        # Safety check: if position is None, recalculate from hex coordinates
        if ship.position is None:
            ship.position = self.hex_grid.axial_to_pixel(ship.hex_q, ship.hex_r)
        
        x, y = ship.position
        
        # Use animated facing if available, otherwise use discrete facing
        if hasattr(ship, '_anim_facing') and ship._anim_facing is not None:
            facing_value = ship._anim_facing
        else:
            facing_value = ship.facing
        
        # Rotate sprite based on facing (0-5, 60° increments)
        # Sprite image points UP (north)
        # Facing 0 = East (right), so rotate 90° clockwise from north
        # Pygame rotation is counterclockwise, so we negate
        # facing 0 = 90° (East/Right)
        # facing 1 = 150° (Southeast) 
        # facing 2 = 210° (Southwest)
        # facing 3 = 270° (West/Left)
        # facing 4 = 330° (Northwest)
        # facing 5 = 30° (Northeast)
        angle = 90 + (facing_value * 60)
        rotated_sprite = pygame.transform.rotate(self.ship_sprite, -angle)
        
        # Get rect for centered drawing
        sprite_rect = rotated_sprite.get_rect(center=(x, y))
        
        # Draw sprite
        self.screen.blit(rotated_sprite, sprite_rect)
        
        # Draw ship name below
        name_surface = self.font_small.render(ship.name, True, color)
        name_rect = name_surface.get_rect(center=(x, y + 70))
        self.screen.blit(name_surface, name_rect)
        
        # Draw hull bar
        bar_width = 80
        bar_height = 8
        bar_x = x - bar_width // 2
        bar_y = y + 80
        
        # Background
        pygame.draw.rect(
            self.screen,
            LCARS_COLORS['bg_dark'],
            (bar_x, bar_y, bar_width, bar_height)
        )
        
        # Hull (green to red based on percentage)
        hull_percent = ship.hull / ship.max_hull
        if hull_percent > 0.6:
            hull_color = LCARS_COLORS['green']
        elif hull_percent > 0.3:
            hull_color = get_warning_color()
        else:
            hull_color = LCARS_COLORS['alert_red']
            
        hull_width = int(bar_width * hull_percent)
        pygame.draw.rect(
            self.screen,
            hull_color,
            (bar_x, bar_y, hull_width, bar_height)
        )
        
        # Border
        pygame.draw.rect(
            self.screen,
            color,
            (bar_x, bar_y, bar_width, bar_height),
            1
        )
        
    def _draw_targeting_lines(self):
        """Draw lines to selected targets"""
        # Only draw targeting lines if player has selected targets
        current_ship = self.get_current_acting_ship()
        
        # Draw player's targeting lines
        player_targets = self.ship_targets.get(self.player_ship, {})
        self._draw_targeting_line_for_ship(self.player_ship, player_targets.get('primary'), LCARS_COLORS['green'], "PRIMARY")
        self._draw_targeting_line_for_ship(self.player_ship, player_targets.get('secondary'), get_warning_color(), "SECONDARY")
        self._draw_targeting_line_for_ship(self.player_ship, player_targets.get('tertiary'), LCARS_COLORS['alert_red'], "TERTIARY")
        
        # Draw enemy's targeting lines
        enemy_targets = self.ship_targets.get(self.enemy_ship, {})
        self._draw_targeting_line_for_ship(self.enemy_ship, enemy_targets.get('primary'), LCARS_COLORS['purple'], None)
    
    def _draw_targeting_line_for_ship(self, attacker, target, color, label):
        """Draw a single targeting line"""
        if not target or not attacker.position or not target.position:
            return
        
        p1 = attacker.position
        p2 = target.position
        
        # Draw line between ships
        pygame.draw.line(
            self.screen,
            color,
            p1, p2,
            2
        )
        
        # Calculate distance
        distance = self.hex_grid.distance(
            attacker.hex_q, attacker.hex_r,
            target.hex_q, target.hex_r
        )
        
        # Draw distance text at midpoint (only for primary)
        if label:
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2
            
            dist_text = f"{label}: {distance} hexes"
            dist_surface = self.font_small.render(dist_text, True, color)
            dist_rect = dist_surface.get_rect(center=(mid_x, mid_y))
            self.screen.blit(dist_surface, dist_rect)
            
    def _draw_ship_status(self):
        """Draw ship status content based on active tab"""
        if not self.player_ship or not self.target_ship:
            return
        
        # Get content area from tabbed panel
        content_rect = self.status_panel.get_content_rect()
        content_x = content_rect.x + 10  # Padding from left
        y = content_rect.y + 10  # Padding from top
        
        # Draw appropriate tab content
        if self.status_panel.active_tab == 0:  # STATUS
            self._draw_status_tab(content_x, y)
        elif self.status_panel.active_tab == 1:  # WEAPONS
            self._draw_weapons_tab(content_x, y)
        elif self.status_panel.active_tab == 2:  # POWER
            self._draw_power_tab(content_x, y)
        elif self.status_panel.active_tab == 3:  # DAMAGE
            self._draw_damage_tab(content_x, y)
    
    def _draw_status_tab(self, x, y):
        """Draw STATUS tab - basic ship info"""
        ship = self.player_ship
        
        # Ship name
        ship_name = "USS " + ship.name.upper()
        title = self.font_small.render(ship_name, True, LCARS_COLORS['blue'])
        self.screen.blit(title, (x, y))
        y += 30
        
        # Ship class and registry
        class_text = f"CLASS: {ship.ship_class.upper()}"
        class_surface = self.font_small.render(class_text, True, LCARS_COLORS['purple'])
        self.screen.blit(class_surface, (x, y))
        y += 25
        
        registry_text = f"REGISTRY: {ship.registry}"
        registry_surface = self.font_small.render(registry_text, True, LCARS_COLORS['purple'])
        self.screen.blit(registry_surface, (x, y))
        y += 30
        
        # Hull
        hull_pct = int((ship.hull / ship.max_hull) * 100)
        hull_text = f"HULL: {int(ship.hull)}/{ship.max_hull} ({hull_pct}%)"
        hull_color = LCARS_COLORS['green'] if hull_pct > 75 else get_warning_color() if hull_pct > 50 else LCARS_COLORS['alert_red']
        hull_surface = self.font_small.render(hull_text, True, hull_color)
        self.screen.blit(hull_surface, (x, y))
        y += 30
        
        # Shields header
        shields_title = self.font_medium.render("SHIELDS", True, LCARS_COLORS['light_blue'])
        self.screen.blit(shields_title, (x, y))
        y += 30
        
        # Shields (all arcs)
        for arc in ['fore', 'aft', 'port', 'starboard']:
            shield_val = int(ship.shields[arc])
            shield_max = ship.max_shields[arc]
            shield_pct = int((shield_val / shield_max) * 100) if shield_max > 0 else 0
            
            shield_text = f"{arc.upper()}: {shield_val}/{shield_max} ({shield_pct}%)"
            shield_color = LCARS_COLORS['light_blue'] if shield_pct > 50 else get_warning_color() if shield_pct > 25 else LCARS_COLORS['alert_red']
            shield_surface = self.font_small.render(shield_text, True, shield_color)
            self.screen.blit(shield_surface, (x, y))
            y += 22
        
        y += 15
        
        # Sensor info
        sensor_range = ship.get_effective_sensor_range()
        sensor_text = f"SENSOR RANGE: {sensor_range} hexes"
        sensor_surface = self.font_small.render(sensor_text, True, LCARS_COLORS['purple'])
        self.screen.blit(sensor_surface, (x, y))
        y += 25
        
        # Crew
        crew_text = f"CREW: {ship.crew_count}/{ship.max_crew}"
        crew_surface = self.font_small.render(crew_text, True, LCARS_COLORS['purple'])
        self.screen.blit(crew_surface, (x, y))
        y += 22
        
        crew_skill_text = f"SKILL LEVEL: {ship.crew_skill}"
        crew_skill_surface = self.font_small.render(crew_skill_text, True, LCARS_COLORS['purple'])
        self.screen.blit(crew_skill_surface, (x, y))
    
    def _draw_weapons_tab(self, x, y):
        """Draw WEAPONS tab - weapon arrays and torpedoes"""
        ship = self.player_ship
        
        # Calculate target arc if we have a target
        target_arc = ship.get_target_arc(self.target_ship.hex_q, self.target_ship.hex_r)
        
        # Weapons header
        weapons_title = self.font_medium.render("WEAPON ARRAYS", True, get_accent_color())
        self.screen.blit(weapons_title, (x, y))
        y += 30
        
        # Energy weapons
        for i, weapon in enumerate(ship.weapon_arrays):
            ready = weapon.can_fire()
            in_arc = target_arc in weapon.firing_arcs
            
            # Color: green if ready and in arc, red if not ready, gray if out of arc
            if not in_arc:
                status_color = LCARS_COLORS['text_gray']
                arc_indicator = "[OUT OF ARC]"
            elif ready:
                status_color = LCARS_COLORS['green']
                arc_indicator = "[READY]"
            else:
                status_color = LCARS_COLORS['alert_red']
                arc_indicator = f"[CD: {weapon.cooldown_remaining}]"
            
            weapon_text = f"{weapon.weapon_type.upper()} Mk{weapon.mark}"
            weapon_surface = self.font_small.render(weapon_text, True, status_color)
            self.screen.blit(weapon_surface, (x, y))
            y += 20
            
            # Weapon details
            damage_text = f"  Damage: {weapon.get_damage()}  Arcs: {', '.join(weapon.firing_arcs)}"
            damage_surface = self.font_small.render(damage_text, True, status_color)
            self.screen.blit(damage_surface, (x, y))
            y += 18
            
            # Status
            status_surface = self.font_small.render(f"  {arc_indicator}", True, status_color)
            self.screen.blit(status_surface, (x, y))
            y += 25
        
        y += 10
        
        # Torpedoes header
        torpedoes_title = self.font_medium.render("TORPEDO BAYS", True, get_accent_color())
        self.screen.blit(torpedoes_title, (x, y))
        y += 30
        
        # Torpedoes
        for i, torpedo in enumerate(ship.torpedo_bays):
            ready = torpedo.can_fire()
            in_arc = target_arc in torpedo.firing_arcs
            
            # Color: green if ready and in arc, red if not ready, gray if out of arc
            if not in_arc:
                status_color = LCARS_COLORS['text_gray']
                arc_indicator = "[OUT OF ARC]"
            elif ready:
                status_color = LCARS_COLORS['green']
                arc_indicator = "[READY]"
            else:
                status_color = LCARS_COLORS['alert_red']
                arc_indicator = f"[CD: {torpedo.cooldown_remaining}]"
            
            torp_text = f"{torpedo.torpedo_type.upper()} Mk{torpedo.mark}"
            torp_surface = self.font_small.render(torp_text, True, status_color)
            self.screen.blit(torp_surface, (x, y))
            y += 20
            
            # Torpedo details
            damage_text = f"  Damage: {torpedo.get_damage()}  Arcs: {', '.join(torpedo.firing_arcs)}"
            damage_surface = self.font_small.render(damage_text, True, status_color)
            self.screen.blit(damage_surface, (x, y))
            y += 18
            
            # Status
            status_surface = self.font_small.render(f"  {arc_indicator}", True, status_color)
            self.screen.blit(status_surface, (x, y))
            y += 25
        
        y += 10
        
        # Target arc display
        arc_text = f"TARGET ARC: {target_arc.upper()}"
        arc_surface = self.font_small.render(arc_text, True, get_accent_color())
        self.screen.blit(arc_surface, (x, y))
    
    def _draw_power_tab(self, x, y):
        """Draw POWER tab - power distribution (placeholder for now)"""
        ship = self.player_ship
        
        # Power header
        power_title = self.font_medium.render("POWER SYSTEMS", True, get_accent_color())
        self.screen.blit(power_title, (x, y))
        y += 35
        
        # Placeholder text
        placeholder = self.font_small.render("Power management system", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder, (x, y))
        y += 22
        
        placeholder2 = self.font_small.render("coming soon...", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder2, (x, y))
        y += 35
        
        # Show some basic power info
        power_text = f"WARP CORE OUTPUT: 100%"
        power_surface = self.font_small.render(power_text, True, LCARS_COLORS['light_blue'])
        self.screen.blit(power_surface, (x, y))
        y += 30
        
        # Power distribution sections
        distributions = [
            ("WEAPONS", 25),
            ("SHIELDS", 25),
            ("ENGINES", 25),
            ("AUXILIARY", 25)
        ]
        
        for system, pct in distributions:
            dist_text = f"{system}: {pct}%"
            dist_surface = self.font_small.render(dist_text, True, LCARS_COLORS['purple'])
            self.screen.blit(dist_surface, (x, y))
            y += 22
    
    def _draw_damage_tab(self, x, y):
        """Draw DAMAGE tab - system damage and repairs (placeholder for now)"""
        ship = self.player_ship
        
        # Damage header
        damage_title = self.font_medium.render("DAMAGE CONTROL", True, get_accent_color())
        self.screen.blit(damage_title, (x, y))
        y += 35
        
        # Placeholder text
        placeholder = self.font_small.render("Damage control system", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder, (x, y))
        y += 22
        
        placeholder2 = self.font_small.render("coming soon...", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder2, (x, y))
        y += 35
        
        # Show hull integrity
        hull_pct = int((ship.hull / ship.max_hull) * 100)
        hull_text = f"HULL INTEGRITY: {hull_pct}%"
        hull_color = LCARS_COLORS['green'] if hull_pct > 75 else get_warning_color() if hull_pct > 50 else LCARS_COLORS['alert_red']
        hull_surface = self.font_small.render(hull_text, True, hull_color)
        self.screen.blit(hull_surface, (x, y))
        y += 30
        
        # System status (placeholder)
        systems = [
            ("SHIELD GENERATORS", "Operational", LCARS_COLORS['green']),
            ("WEAPON SYSTEMS", "Operational", LCARS_COLORS['green']),
            ("IMPULSE ENGINES", "Operational", LCARS_COLORS['green']),
            ("SENSORS", "Operational", LCARS_COLORS['green']),
        ]
        
        for system_name, status, color in systems:
            system_text = f"{system_name}: {status}"
            system_surface = self.font_small.render(system_text, True, color)
            self.screen.blit(system_surface, (x, y))
            y += 22
        
    def _draw_combat_log(self):
        """Draw combat log in bottom panel"""
        log_x = 70
        log_y = self.screen_height - 115
        
        # Title
        title = self.font_small.render("COMBAT LOG", True, get_accent_color())
        self.screen.blit(title, (log_x, log_y))
        log_y += 25
        
        # Log messages (last 3)
        for message in self.combat_log:
            msg_surface = self.font_small.render(message, True, LCARS_COLORS['text_white'])
            self.screen.blit(msg_surface, (log_x, log_y))
            log_y += 22
