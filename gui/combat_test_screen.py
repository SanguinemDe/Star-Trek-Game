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
from game.rng import game_rng
from game.logger import get_logger

logger = get_logger(__name__)


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
            offset_x = game_rng.roll_damage(-25, 25)
            offset_y = game_rng.roll_damage(-25, 25)
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


class CombatConfigScreen:
    """Pre-combat configuration screen for ship selection"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Fonts
        self.font_large = get_font(32, bold=True)
        self.font_medium = get_font(20, bold=True)
        self.font_small = get_font(16)
        self.font_tiny = get_font(14)
        
        # Get list of combat-ready ships (have sprites)
        self.available_ships = self._get_combat_ready_ships()
        
        # Selection state
        self.selected_player_ship = self.available_ships[0] if self.available_ships else None
        self.enemy_ships = []  # List of (ship_class, count)
        self.selected_enemy_ship = self.available_ships[0] if self.available_ships else None
        self.enemy_count = 1
        
        # UI state
        self.player_ship_scroll = 0
        self.enemy_ship_scroll = 0
        self.max_scroll_items = 8  # How many ships visible at once
        
        # Buttons
        self.start_button = pygame.Rect(
            self.screen_width // 2 - 100,
            self.screen_height - 100,
            200, 50
        )
        
        self.add_enemy_button = pygame.Rect(
            self.screen_width - 380,
            self.screen_height // 2 + 100,
            150, 40
        )
        
        # Scroll buttons
        self.player_scroll_up = pygame.Rect(self.screen_width // 4 + 150, 200, 30, 30)
        self.player_scroll_down = pygame.Rect(self.screen_width // 4 + 150, 600, 30, 30)
        self.enemy_scroll_up = pygame.Rect(self.screen_width * 3 // 4 + 150, 200, 30, 30)
        self.enemy_scroll_down = pygame.Rect(self.screen_width * 3 // 4 + 150, 600, 30, 30)
        
    def _get_combat_ready_ships(self):
        """
        Scan assets folder and return list of ship classes that have sprites
        Returns list of tuples: (ship_class_name, create_function_name)
        """
        import os
        import glob
        
        # Scan for available sprites
        sprite_path = "assets/Ships/Federation"
        available_sprites = set()
        
        if os.path.exists(sprite_path):
            for filepath in glob.glob(os.path.join(sprite_path, "*Class.png")):
                filename = os.path.basename(filepath)
                # Extract class name (e.g., "MirandaClass.png" -> "Miranda")
                class_name = filename.replace("Class.png", "")
                available_sprites.add(class_name)
        
        print(f"✓ Found {len(available_sprites)} ship sprites: {', '.join(sorted(available_sprites))}")
        
        # Get all Federation ship creation functions
        from game.ships import federation
        combat_ready = []
        
        for attr_name in dir(federation):
            if attr_name.startswith('create_') and attr_name.endswith('_class'):
                # Extract ship class name from function name
                # e.g., "create_miranda_class" -> "Miranda"
                # e.g., "create_excelsior_ii_class" -> "Excelsior2"
                class_name_parts = attr_name.replace('create_', '').replace('_class', '').split('_')
                
                # Convert parts to proper case, handle "ii" -> "2" conversion
                converted_parts = []
                for part in class_name_parts:
                    if part.lower() == 'ii':
                        converted_parts.append('2')
                    elif part.lower() == 'iii':
                        converted_parts.append('3')
                    else:
                        converted_parts.append(part.capitalize())
                
                class_name = ''.join(converted_parts)
                
                # Check if sprite exists for this ship
                if class_name in available_sprites:
                    combat_ready.append({
                        'class_name': class_name,
                        'function_name': attr_name,
                        'display_name': class_name + '-class'
                    })
        
        # Sort alphabetically
        combat_ready.sort(key=lambda x: x['display_name'])
        
        print(f"✓ {len(combat_ready)} ships are combat-ready (have sprites)")
        
        return combat_ready
    
    def run(self):
        """Run the configuration screen, returns combat config or None if cancelled"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        result = self._handle_click(event.pos)
                        if result == "start":
                            return self._build_config()
                        elif result == "cancel":
                            return None
                
                if event.type == pygame.MOUSEWHEEL:
                    # Handle scroll in ship lists
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x < self.screen_width // 2:  # Player side
                        self.player_ship_scroll = max(0, min(
                            len(self.available_ships) - self.max_scroll_items,
                            self.player_ship_scroll - event.y
                        ))
                    else:  # Enemy side
                        self.enemy_ship_scroll = max(0, min(
                            len(self.available_ships) - self.max_scroll_items,
                            self.enemy_ship_scroll - event.y
                        ))
            
            self._draw()
            pygame.display.flip()
            clock.tick(60)
        
        return None
    
    def _handle_click(self, pos):
        """Handle mouse clicks"""
        x, y = pos
        
        # Start button
        if self.start_button.collidepoint(pos):
            if self.selected_player_ship and self.enemy_ships:
                return "start"
        
        # Add enemy button
        if self.add_enemy_button.collidepoint(pos):
            if self.selected_enemy_ship:
                # Check if this ship type already exists in enemy list
                existing = None
                for i, (ship_class, count) in enumerate(self.enemy_ships):
                    if ship_class == self.selected_enemy_ship['class_name']:
                        existing = i
                        break
                
                if existing is not None:
                    # Increment count
                    ship_class, count = self.enemy_ships[existing]
                    self.enemy_ships[existing] = (ship_class, count + self.enemy_count)
                else:
                    # Add new entry
                    self.enemy_ships.append((self.selected_enemy_ship['class_name'], self.enemy_count))
        
        # Scroll buttons
        if self.player_scroll_up.collidepoint(pos):
            self.player_ship_scroll = max(0, self.player_ship_scroll - 1)
        if self.player_scroll_down.collidepoint(pos):
            self.player_ship_scroll = min(
                len(self.available_ships) - self.max_scroll_items,
                self.player_ship_scroll + 1
            )
        if self.enemy_scroll_up.collidepoint(pos):
            self.enemy_ship_scroll = max(0, self.enemy_ship_scroll - 1)
        if self.enemy_scroll_down.collidepoint(pos):
            self.enemy_ship_scroll = min(
                len(self.available_ships) - self.max_scroll_items,
                self.enemy_ship_scroll + 1
            )
        
        # Player ship selection (left side)
        if x < self.screen_width // 2 and 230 < y < 630:
            list_y = 230
            for i in range(self.max_scroll_items):
                idx = self.player_ship_scroll + i
                if idx >= len(self.available_ships):
                    break
                
                ship_rect = pygame.Rect(self.screen_width // 4 - 150, list_y, 300, 45)
                if ship_rect.collidepoint(pos):
                    self.selected_player_ship = self.available_ships[idx]
                    break
                list_y += 50
        
        # Enemy ship selection (right side)
        elif x > self.screen_width // 2 and 230 < y < 630:
            list_y = 230
            for i in range(self.max_scroll_items):
                idx = self.enemy_ship_scroll + i
                if idx >= len(self.available_ships):
                    break
                
                ship_rect = pygame.Rect(self.screen_width * 3 // 4 - 150, list_y, 300, 45)
                if ship_rect.collidepoint(pos):
                    self.selected_enemy_ship = self.available_ships[idx]
                    break
                list_y += 50
        
        # Enemy list - click to remove
        if x > self.screen_width // 2:
            enemy_list_y = self.screen_height // 2 + 150
            for i, (ship_class, count) in enumerate(self.enemy_ships):
                entry_rect = pygame.Rect(
                    self.screen_width * 3 // 4 - 150,
                    enemy_list_y + i * 30,
                    300, 25
                )
                if entry_rect.collidepoint(pos):
                    # Right click to remove, left click to decrement
                    self.enemy_ships.pop(i)
                    break
        
        # Count adjustment buttons
        count_x = self.screen_width * 3 // 4
        count_y = self.screen_height // 2 + 60
        minus_btn = pygame.Rect(count_x - 60, count_y, 30, 30)
        plus_btn = pygame.Rect(count_x + 30, count_y, 30, 30)
        
        if minus_btn.collidepoint(pos):
            self.enemy_count = max(1, self.enemy_count - 1)
        if plus_btn.collidepoint(pos):
            self.enemy_count = min(10, self.enemy_count + 1)
        
        return None
    
    def _build_config(self):
        """Build and return combat configuration"""
        return {
            'player_ship': self.selected_player_ship,
            'enemy_ships': self.enemy_ships.copy()
        }
    
    def _draw(self):
        """Draw the configuration screen"""
        self.screen.fill(LCARS_COLORS['bg_dark'])
        
        # Title
        title = self.font_large.render("COMBAT CONFIGURATION", True, get_accent_color())
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Divider line
        pygame.draw.line(
            self.screen,
            get_accent_color(),
            (100, 100),
            (self.screen_width - 100, 100),
            3
        )
        
        # Draw player ship selection (LEFT SIDE)
        self._draw_player_selection()
        
        # Draw enemy configuration (RIGHT SIDE)
        self._draw_enemy_configuration()
        
        # Draw start button
        self._draw_start_button()
    
    def _draw_player_selection(self):
        """Draw player ship selection panel"""
        x = self.screen_width // 4
        y = 150
        
        # Title
        title = self.font_medium.render("SELECT YOUR SHIP", True, LCARS_COLORS['light_blue'])
        title_rect = title.get_rect(center=(x, y))
        self.screen.blit(title, title_rect)
        
        # Scroll buttons
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], self.player_scroll_up)
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], self.player_scroll_down)
        up_text = self.font_small.render("▲", True, LCARS_COLORS['text_white'])
        down_text = self.font_small.render("▼", True, LCARS_COLORS['text_white'])
        self.screen.blit(up_text, up_text.get_rect(center=self.player_scroll_up.center))
        self.screen.blit(down_text, down_text.get_rect(center=self.player_scroll_down.center))
        
        # Ship list
        list_y = 230
        for i in range(self.max_scroll_items):
            idx = self.player_ship_scroll + i
            if idx >= len(self.available_ships):
                break
            
            ship = self.available_ships[idx]
            is_selected = ship == self.selected_player_ship
            
            # Background
            ship_rect = pygame.Rect(x - 150, list_y, 300, 45)
            color = LCARS_COLORS['orange'] if is_selected else LCARS_COLORS['bg_medium']
            pygame.draw.rect(self.screen, color, ship_rect)
            pygame.draw.rect(self.screen, LCARS_COLORS['blue'], ship_rect, 2)
            
            # Ship name
            name = self.font_small.render(ship['display_name'], True, LCARS_COLORS['text_white'])
            name_rect = name.get_rect(center=ship_rect.center)
            self.screen.blit(name, name_rect)
            
            list_y += 50
    
    def _draw_enemy_configuration(self):
        """Draw enemy ship configuration panel"""
        x = self.screen_width * 3 // 4
        y = 150
        
        # Title
        title = self.font_medium.render("CONFIGURE ENEMY FORCES", True, LCARS_COLORS['alert_red'])
        title_rect = title.get_rect(center=(x, y))
        self.screen.blit(title, title_rect)
        
        # Scroll buttons
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], self.enemy_scroll_up)
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], self.enemy_scroll_down)
        up_text = self.font_small.render("▲", True, LCARS_COLORS['text_white'])
        down_text = self.font_small.render("▼", True, LCARS_COLORS['text_white'])
        self.screen.blit(up_text, up_text.get_rect(center=self.enemy_scroll_up.center))
        self.screen.blit(down_text, down_text.get_rect(center=self.enemy_scroll_down.center))
        
        # Ship selection list
        list_y = 230
        for i in range(self.max_scroll_items):
            idx = self.enemy_ship_scroll + i
            if idx >= len(self.available_ships):
                break
            
            ship = self.available_ships[idx]
            is_selected = ship == self.selected_enemy_ship
            
            # Background
            ship_rect = pygame.Rect(x - 150, list_y, 300, 45)
            color = LCARS_COLORS['orange'] if is_selected else LCARS_COLORS['bg_medium']
            pygame.draw.rect(self.screen, color, ship_rect)
            pygame.draw.rect(self.screen, LCARS_COLORS['blue'], ship_rect, 2)
            
            # Ship name
            name = self.font_small.render(ship['display_name'], True, LCARS_COLORS['text_white'])
            name_rect = name.get_rect(center=ship_rect.center)
            self.screen.blit(name, name_rect)
            
            list_y += 50
        
        # Count selector
        count_y = self.screen_height // 2 + 60
        count_label = self.font_small.render("Quantity:", True, LCARS_COLORS['text_white'])
        self.screen.blit(count_label, (x - 100, count_y))
        
        # Minus button
        minus_btn = pygame.Rect(x - 60, count_y, 30, 30)
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], minus_btn)
        minus_text = self.font_medium.render("-", True, LCARS_COLORS['text_white'])
        self.screen.blit(minus_text, minus_text.get_rect(center=minus_btn.center))
        
        # Count display
        count_text = self.font_medium.render(str(self.enemy_count), True, LCARS_COLORS['light_blue'])
        count_rect = count_text.get_rect(center=(x, count_y + 15))
        self.screen.blit(count_text, count_rect)
        
        # Plus button
        plus_btn = pygame.Rect(x + 30, count_y, 30, 30)
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], plus_btn)
        plus_text = self.font_medium.render("+", True, LCARS_COLORS['text_white'])
        self.screen.blit(plus_text, plus_text.get_rect(center=plus_btn.center))
        
        # Add button
        pygame.draw.rect(self.screen, LCARS_COLORS['green'], self.add_enemy_button)
        pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], self.add_enemy_button, 2)
        add_text = self.font_small.render("ADD TO FLEET", True, LCARS_COLORS['bg_dark'])
        add_rect = add_text.get_rect(center=self.add_enemy_button.center)
        self.screen.blit(add_text, add_rect)
        
        # Enemy fleet list
        fleet_y = self.screen_height // 2 + 150
        fleet_label = self.font_small.render("ENEMY FLEET:", True, LCARS_COLORS['alert_red'])
        self.screen.blit(fleet_label, (x - 150, fleet_y - 30))
        
        if not self.enemy_ships:
            empty_text = self.font_tiny.render("(No ships added)", True, LCARS_COLORS['text_gray'])
            self.screen.blit(empty_text, (x - 150, fleet_y))
        else:
            for i, (ship_class, count) in enumerate(self.enemy_ships):
                entry_rect = pygame.Rect(x - 150, fleet_y + i * 30, 300, 25)
                pygame.draw.rect(self.screen, LCARS_COLORS['bg_medium'], entry_rect)
                pygame.draw.rect(self.screen, LCARS_COLORS['alert_red'], entry_rect, 1)
                
                entry_text = self.font_tiny.render(
                    f"{count}× {ship_class}-class",
                    True,
                    LCARS_COLORS['text_white']
                )
                self.screen.blit(entry_text, (x - 140, fleet_y + i * 30 + 5))
    
    def _draw_start_button(self):
        """Draw the start combat button"""
        # Check if valid configuration
        can_start = self.selected_player_ship is not None and len(self.enemy_ships) > 0
        
        color = LCARS_COLORS['green'] if can_start else LCARS_COLORS['bg_medium']
        pygame.draw.rect(self.screen, color, self.start_button)
        pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], self.start_button, 3)
        
        text = self.font_medium.render("BEGIN COMBAT", True, LCARS_COLORS['bg_dark'] if can_start else LCARS_COLORS['text_gray'])
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)
        
        # Instructions
        if can_start:
            instructions = self.font_tiny.render("Click ship name to remove from enemy fleet", True, LCARS_COLORS['text_gray'])
        else:
            instructions = self.font_tiny.render("Select your ship and add enemy ships to fleet", True, LCARS_COLORS['alert_red'])
        
        inst_rect = instructions.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(instructions, inst_rect)


class CombatTestScreen:
    """Combat testing arena with configurable ships"""
    
    def __init__(self, screen, config=None):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Fonts - use sci-fi themed fonts (reduced sizes for better fit)
        self.font_large = get_font(32, bold=True)
        self.font_medium = get_font(20, bold=True)
        self.font_small = get_font(16)
        self.font_tiny = get_font(14)
        
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
        self.phaser_sound = None  # Phaser firing sound
        
        # Combat results tracking
        self.combat_results = {
            'player': {'hits': [], 'misses': [], 'damage_taken': 0, 'shields_lost': 0, 'hull_lost': 0},
            'enemy': {'hits': [], 'misses': [], 'damage_dealt': 0, 'shields_lost': 0, 'hull_lost': 0, 'distance': 0}
        }
        self.show_combat_summary = False
        self.pending_combat_summary = False  # Waiting for weapon effects to finish before showing summary
        
        # Weapon assignment system
        self.show_weapon_assignment = False
        self.weapon_assignments = {}  # Maps weapon index to target priority ('primary', 'secondary', 'tertiary')
        
        # Weapons tab scrolling
        self.weapons_scroll_offset = 0
        self.weapons_max_scroll = 0
        
        # Weapon assignment UI scrolling
        self.weapon_assign_phaser_scroll = 0
        self.weapon_assign_torpedo_scroll = 0
        
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
        
        # Initialize sprite cache (will be populated as ships are drawn)
        self.ship_sprite_cache = {}  # Format: {ship_class: {scale_factor: {facing: surface}}}
        
        # Store configuration
        self.config = config
        
        # Load weapon effects
        self._load_weapon_effects()
        
        # Create ships based on configuration
        self._create_ships_from_config()
        
        # Load sprites for all ships in combat
        for ship in self.all_ships:
            self._load_ship_sprite(ship)
        
        # Set ship references
        self.selected_ship = self.player_ship
        self.target_ship = self.enemy_ship
        
        # UI elements
        self._create_ui()
        
        self.next_screen = None
        
    def _create_ships_from_config(self):
        """Create ships based on configuration or use default"""
        from game.ships import federation, get_federation_ship
        
        # If no config, use default Odyssey vs Odyssey
        if not self.config:
            # Default: Player Odyssey vs Enemy Odyssey
            self.player_ship = get_federation_ship("Odyssey", "Enterprise", "NCC-1701-F")
            self.player_ship.hex_q = -5
            self.player_ship.hex_r = 0
            self.player_ship.facing = 0
            self.player_ship.position = self.hex_grid.axial_to_pixel(
                self.player_ship.hex_q,
                self.player_ship.hex_r
            )
            self.player_ship.faction = "friendly"  # Assign faction
            
            self.enemy_ship = get_federation_ship("Odyssey", "Target Drone", "NX-99999")
            self.enemy_ship.hex_q = 10
            self.enemy_ship.hex_r = 0
            self.enemy_ship.facing = 3
            self.enemy_ship.position = self.hex_grid.axial_to_pixel(
                self.enemy_ship.hex_q,
                self.enemy_ship.hex_r
            )
            self.enemy_ship.faction = "enemy"  # Assign faction
            
            self.all_ships = [self.player_ship, self.enemy_ship]
            self.add_to_log("Combat ready - press SPACE to fire, ENTER to advance")
            return
        
        # Create player ship
        player_config = self.config['player_ship']
        create_func = getattr(federation, player_config['function_name'])
        self.player_ship = create_func("Enterprise", "NCC-1701")
        
        # Position player ship on left
        self.player_ship.hex_q = -5
        self.player_ship.hex_r = 0
        self.player_ship.facing = 0  # Facing right
        self.player_ship.position = self.hex_grid.axial_to_pixel(
            self.player_ship.hex_q,
            self.player_ship.hex_r
        )
        self.player_ship.faction = "friendly"  # Assign faction
        
        # Create enemy ships
        enemy_ships_list = []
        registry_counter = 1000
        
        # Starting positions for enemy formation (closer to center)
        start_q = 5
        start_r = -2
        
        # Debug to file
        with open("combat_debug.txt", "w") as f:
            f.write(f"Enemy ships config: {self.config['enemy_ships']}\n")
        
        for ship_class, count in self.config['enemy_ships']:
            with open("combat_debug.txt", "a") as f:
                f.write(f"Processing {ship_class}, requesting {count} ships\n")
            
            # Find the create function for this ship class
            function_name = None
            for ship_data in CombatConfigScreen(self.screen)._get_combat_ready_ships():
                if ship_data['class_name'] == ship_class:
                    function_name = ship_data['function_name']
                    break
            
            with open("combat_debug.txt", "a") as f:
                f.write(f"Found function_name: {function_name}\n")
            
            if not function_name:
                with open("combat_debug.txt", "a") as f:
                    f.write(f"WARNING: No function found for {ship_class}, skipping!\n")
                continue
            
            create_func = getattr(federation, function_name)
            
            for i in range(count):
                with open("combat_debug.txt", "a") as f:
                    f.write(f"Creating ship {i+1}/{count}\n")
                ship = create_func(f"{ship_class}-{i+1}", f"NCC-{registry_counter}")
                registry_counter += 1
                
                # Position in formation (staggered rows)
                row = len(enemy_ships_list) // 3
                col = len(enemy_ships_list) % 3
                
                ship.hex_q = start_q + col * 2
                ship.hex_r = start_r + row * 2
                ship.facing = 3  # Facing left (toward player)
                ship.position = self.hex_grid.axial_to_pixel(ship.hex_q, ship.hex_r)
                ship.faction = "enemy"  # Assign faction
                
                # Debug: Log ship spawn
                with open("combat_debug.txt", "a") as f:
                    f.write(f"Created {ship.name} at hex ({ship.hex_q}, {ship.hex_r}), pixel {ship.position}\n")
                
                enemy_ships_list.append(ship)
        
        with open("combat_debug.txt", "a") as f:
            f.write(f"\nTotal enemy ships created: {len(enemy_ships_list)}\n")
            f.write(f"Enemy ship names: {[s.name for s in enemy_ships_list]}\n")
        
        # Set enemy_ship to first enemy for compatibility with existing code
        self.enemy_ship = enemy_ships_list[0] if enemy_ships_list else None
        
        # Build complete ship list
        self.all_ships = [self.player_ship] + enemy_ships_list
        with open("combat_debug.txt", "a") as f:
            f.write(f"Total ships in all_ships: {len(self.all_ships)}\n")
            f.write(f"All ship names: {[s.name for s in self.all_ships]}\n")
        
        # Create AI controllers for ALL enemy ships
        self.enemy_ais = []  # List of all enemy AIs
        for enemy in enemy_ships_list:
            ai = ShipAI(enemy, self.hex_grid)
            # AI will select targets intelligently based on factions
            ai.set_target(self.player_ship)  # Initial target
            AIPersonality.apply_to_ai(ai, 'balanced')
            self.enemy_ais.append(ai)
        
        # Keep self.enemy_ai for backward compatibility
        self.enemy_ai = self.enemy_ais[0] if self.enemy_ais else None
        
        # Log combat start
        enemy_desc = ", ".join([f"{count}× {ship_class}" for ship_class, count in self.config['enemy_ships']])
        total_enemies = sum(count for ship_class, count in self.config['enemy_ships'])
        self.add_to_log(f"Combat: {self.player_ship.ship_class} vs {total_enemies} enemy ships")
        self.add_to_log(f"  Enemy forces: {enemy_desc}")
        self.add_to_log("Combat ready - press SPACE to fire, ENTER to advance")
        
        # Initialize targeting for all ships
        self.ship_targets = {}
        for ship in self.all_ships:
            self.ship_targets[ship] = {'primary': None, 'secondary': None, 'tertiary': None}
        
        # Start combat with initiative roll
        self.start_new_turn()
        
    def _load_ship_sprite(self, ship):
        """Load the ship sprite image with pre-rendered rotations for maximum quality"""
        import os
        
        # Skip if already loaded
        if ship.ship_class in self.ship_sprite_cache:
            return
        
        # Determine sprite path based on ship class
        # Format: assets/Ships/Federation/{ClassName}Class.png
        class_name = ship.ship_class.replace('-', '').replace(' ', '')  # Remove hyphens and spaces
        
        # Convert Roman numerals to Arabic numerals for file names
        # e.g., "ExcelsiorII" -> "Excelsior2"
        class_name = class_name.replace('II', '2').replace('III', '3').replace('IV', '4').replace('V', '5')
        
        sprite_path = f"assets/Ships/Federation/{class_name}Class.png"
        
        # Initialize cache for this ship class
        ship_cache = {}
        
        try:
            # Check if file exists
            if not os.path.exists(sprite_path):
                raise FileNotFoundError(f"File not found: {sprite_path}")
            
            # Load original high-res sprite
            original_sprite = pygame.image.load(sprite_path).convert_alpha()
            
            # Store original for reference
            original_rect = original_sprite.get_rect()
            aspect_ratio = original_rect.width / original_rect.height
            
            print(f"✓ Loaded ship sprite from {sprite_path}")
            print(f"  Original size: {original_rect.width}x{original_rect.height}")
            print(f"  Pre-rendering rotations for quality...")
            
            # Pre-render sprites for each size category
            size_scales = {
                'Small': 0.7,
                'Medium': 1.0,
                'Large': 1.3,
                'Very Large': 2.0,
                'Huge': 2.5
            }
            
            # Base size for sprite scaling (slightly larger to fill 7-hex footprint better)
            base_size = int(self.hex_size * 1.9)
            
            for size_name, scale_factor in size_scales.items():
                # Calculate target size for this scale
                target_size = int(base_size * scale_factor)
                
                if aspect_ratio > 1:  # Wider than tall
                    new_width = target_size
                    new_height = int(target_size / aspect_ratio)
                else:  # Taller than wide
                    new_height = target_size
                    new_width = int(target_size * aspect_ratio)
                
                # Scale from original (not from already-scaled) for best quality
                scaled_sprite = pygame.transform.smoothscale(
                    original_sprite,
                    (new_width, new_height)
                )
                
                # Pre-render all 6 rotation angles for this size
                ship_cache[scale_factor] = {}
                for facing in range(6):
                    # Calculate rotation angle
                    angle = 90 + (facing * 60)
                    # Pre-render the rotation
                    rotated = pygame.transform.rotozoom(scaled_sprite, -angle, 1.0)
                    ship_cache[scale_factor][facing] = rotated
            
            # Store in main cache
            self.ship_sprite_cache[ship.ship_class] = ship_cache
            
            print(f"  ✓ Pre-rendered {len(size_scales) * 6} sprite variants for {ship.ship_class}")
            
        except Exception as e:
            print(f"⚠ Could not load {sprite_path}: {e}")
            print(f"  Current directory: {os.getcwd()}")
            
            # Try fallback to Odyssey sprite
            fallback_path = "assets/Ships/Federation/OdysseyClass.png"
            if os.path.exists(fallback_path) and sprite_path != fallback_path:
                print(f"  Attempting fallback to {fallback_path}...")
                try:
                    original_sprite = pygame.image.load(fallback_path).convert_alpha()
                    original_rect = original_sprite.get_rect()
                    aspect_ratio = original_rect.width / original_rect.height
                    
                    size_scales = {
                        'Small': 0.7,
                        'Medium': 1.0,
                        'Large': 1.3,
                        'Very Large': 2.0,
                        'Huge': 2.5
                    }
                    base_size = int(self.hex_size * 1.9)
                    
                    for size_name, scale_factor in size_scales.items():
                        target_size = int(base_size * scale_factor)
                        if aspect_ratio > 1:
                            new_width = target_size
                            new_height = int(target_size / aspect_ratio)
                        else:
                            new_height = target_size
                            new_width = int(target_size * aspect_ratio)
                        
                        scaled_sprite = pygame.transform.smoothscale(original_sprite, (new_width, new_height))
                        ship_cache[scale_factor] = {}
                        for facing in range(6):
                            angle = 90 + (facing * 60)
                            rotated = pygame.transform.rotozoom(scaled_sprite, -angle, 1.0)
                            ship_cache[scale_factor][facing] = rotated
                    
                    self.ship_sprite_cache[ship.ship_class] = ship_cache
                    print(f"  ✓ Using fallback sprite for {ship.ship_class}")
                    return
                except Exception as fallback_error:
                    print(f"  ✗ Fallback also failed: {fallback_error}")
            
            print(f"  Using placeholder. Save your image as {sprite_path}")
            
            # Create a placeholder sprite for all sizes and rotations
            size_scales = {
                'Small': 0.7,
                'Medium': 1.0,
                'Large': 1.3,
                'Very Large': 2.0,
                'Huge': 2.5
            }
            
            base_size = int(self.hex_size * 1.9)
            
            for size_name, scale_factor in size_scales.items():
                ship_cache[scale_factor] = {}
                sprite_size = int(base_size * scale_factor)
                
                for facing in range(6):
                    placeholder = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                    center = sprite_size // 2
                    
                    # Draw a simple ship shape
                    pygame.draw.circle(placeholder, LCARS_COLORS['light_blue'], (center, center - 10), 15)
                    pygame.draw.rect(placeholder, LCARS_COLORS['light_blue'], (center - 5, center, 10, 25))
                    pygame.draw.rect(placeholder, LCARS_COLORS['blue'], (center - 20, center + 10, 8, 20))
                    pygame.draw.rect(placeholder, LCARS_COLORS['blue'], (center + 12, center + 10, 8, 20))
                    
                    # Rotate for facing
                    angle = 90 + (facing * 60)
                    rotated = pygame.transform.rotozoom(placeholder, -angle, 1.0)
                    ship_cache[scale_factor][facing] = rotated
            
            self.ship_sprite_cache[ship.ship_class] = ship_cache
    
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
            
            # Load weapon sounds
            try:
                audio_path = "assets/audio/weapons/arrays"
                self.phaser_sound = pygame.mixer.Sound(os.path.join(audio_path, "phaser_audio.mp3"))
                self.phaser_sound.set_volume(0.3)  # Set to 30% volume so it's not too loud
                print("✓ Loaded phaser audio")
            except Exception as audio_error:
                print(f"⚠ Could not load phaser audio: {audio_error}")
                self.phaser_sound = None
            
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
        
        logger.info(f"=== Turn {self.turn_number} Started ===")
        
        # Update AI targets (check for dead targets, friendly fire, etc.)
        for ai in self.enemy_ais:
            ai.update_target(self.all_ships)
            if ai.target:
                logger.info(f"AI {ai.ship.name} targeting {ai.target.name}")
        
        # Roll initiative
        self.roll_initiative()
        
        # Auto-advance to movement phase
        self.advance_phase()
    
    def roll_initiative(self):
        """Determine turn order based on command skill"""
        # TEMPORARILY DISABLED - Player always goes first for testing
        # import random
        # 
        # initiative_rolls = []
        # 
        # for ship in self.all_ships:
        #     # Base initiative from command crew skill (if present)
        #     base_initiative = 0
        #     if ship.command_crew.get('captain'):
        #         base_initiative = ship.command_crew['captain'].attributes.get('command', 50)
        #     
        #     # Add random d100 roll
        #     roll = random.randint(1, 100)
        #     total = base_initiative + roll
        #     
        #     initiative_rolls.append((ship, total, roll))
        # 
        # # Sort by total (highest first)
        # initiative_rolls.sort(key=lambda x: x[1], reverse=True)
        # self.initiative_order = [ship for ship, total, roll in initiative_rolls]
        
        # TESTING: Player always wins initiative, but include ALL ships
        self.initiative_order = [self.player_ship] + [ship for ship in self.all_ships if ship != self.player_ship]
    
    def advance_phase(self):
        """Move to next combat phase"""
        current_index = self.phase_order.index(self.combat_phase)
        
        # Check if current phase is complete
        if not self.is_phase_complete():
            return  # Phase not done yet
        
        # If leaving firing phase, mark that we want to show combat summary
        # but wait for weapon effects to finish first
        if self.combat_phase == "firing":
            if len(self.active_weapon_effects) > 0:
                # Still have active weapon effects, wait for them to finish
                self.pending_combat_summary = True
                return  # Don't advance yet, wait for effects to finish
            else:
                # No active effects, show summary immediately
                self.show_combat_summary = True
                return  # Don't advance yet, wait for summary dismissal
        
        # Move to next phase
        if current_index < len(self.phase_order) - 1:
            self.combat_phase = self.phase_order[current_index + 1]
            self.current_ship_index = 0
            
            logger.info(f"Combat phase advanced to: {self.combat_phase.upper()}")
            
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
            
            # Initialize firing phase - show weapon assignment if player has multiple targets
            if self.combat_phase == "firing" and len(self.initiative_order) > 0:
                first_ship = self.initiative_order[0]
                if first_ship == self.player_ship:
                    # Check if player has multiple targets
                    targets = self.ship_targets.get(self.player_ship, {})
                    target_count = sum(1 for t in [targets.get('primary'), targets.get('secondary'), targets.get('tertiary')] if t is not None)
                    if target_count > 1:
                        # Show weapon assignment window
                        self.show_weapon_assignment = True
                        self._initialize_weapon_assignments()
            
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
            # Execute AI targeting if it's AI ship's turn in targeting phase
            elif self.combat_phase == "targeting":
                next_ship = self.get_current_acting_ship()
                if next_ship and next_ship != self.player_ship:
                    # AI auto-selects targets
                    pygame.time.set_timer(pygame.USEREVENT + 4, 300)
            # Execute AI firing if it's AI ship's turn in firing phase
            elif self.combat_phase == "firing":
                next_ship = self.get_current_acting_ship()
                if next_ship and next_ship != self.player_ship:
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
        if ship != self.player_ship:
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
        ship = self.get_current_acting_ship()
        if not ship or ship == self.player_ship:
            self.complete_ship_action()
            return
        
        # Find this ship's AI controller
        ship_ai = None
        for ai in self.enemy_ais:
            if ai.ship == ship:
                ship_ai = ai
                break
        
        if not ship_ai:
            self.add_to_log(f"{ship.name}: No AI controller found")
            self.complete_ship_action()
            return
        
        # Ensure AI has updated target
        ship_ai.update_target(self.all_ships)
        
        # Get AI movement decisions
        moves = ship_ai.decide_movement(self.movement_points_remaining)
        
        # If no moves, complete action immediately
        if len(moves) == 0:
            pygame.time.set_timer(pygame.USEREVENT + 2, 500)
            return
        
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
        ship = self.get_current_acting_ship()
        if not ship or ship == self.player_ship:
            self.complete_ship_action()
            return
        
        # Find this ship's AI controller
        ship_ai = None
        for ai in self.enemy_ais:
            if ai.ship == ship:
                ship_ai = ai
                break
        
        # Update target before firing (ensure valid enemy target)
        if ship_ai:
            ship_ai.update_target(self.all_ships)
            target = ship_ai.target
        else:
            # Fallback: get from targeting phase
            targets = self.ship_targets.get(ship, {})
            target = targets.get('primary')
        
        # Fire at target with full accuracy
        if target and target.hull > 0:
            # Verify target is actually an enemy (faction check)
            ship_faction = getattr(ship, 'faction', 'neutral')
            target_faction = getattr(target, 'faction', 'neutral')
            
            if ship_faction != target_faction:  # Only fire at different factions
                self._fire_at_target(ship, target, 1.0, "PRIMARY")
            else:
                self.add_to_log(f"{ship.name}: Refusing to fire at friendly {target.name}")
        
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
        """AI automatically selects targets based on factions"""
        ship = self.get_current_acting_ship()
        if not ship or ship == self.player_ship:
            self.complete_ship_action()
            return
        
        # Find this ship's AI controller
        ship_ai = None
        for ai in self.enemy_ais:
            if ai.ship == ship:
                ship_ai = ai
                break
        
        # Use AI's intelligent target selection
        if ship_ai:
            ship_ai.update_target(self.all_ships)
            target = ship_ai.target
            
            if target:
                # Set as primary target
                self.select_target(ship, target, 'primary')
                
                # Optionally select secondary targets from other valid enemies
                available_enemies = [
                    s for s in self.all_ships 
                    if s != ship and s != target and s.hull > 0
                    and getattr(s, 'faction', 'neutral') != getattr(ship, 'faction', 'neutral')
                ]
                
                if len(available_enemies) > 0:
                    # Pick closest enemy as secondary
                    target_distances = []
                    for enemy in available_enemies:
                        dist = self.hex_grid.distance(
                            ship.hex_q, ship.hex_r,
                            enemy.hex_q, enemy.hex_r
                        )
                        target_distances.append((enemy, dist))
                    
                    target_distances.sort(key=lambda x: x[1])
                    self.select_target(ship, target_distances[0][0], 'secondary')
                    
                    if len(target_distances) > 1:
                        self.select_target(ship, target_distances[1][0], 'tertiary')
            else:
                self.add_to_log(f"{ship.name}: No valid enemy targets!")
        else:
            self.add_to_log(f"{ship.name}: No AI controller found!")
        
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
    
    # ═══════════════════════════════════════════════════════════════════
    # WEAPON ASSIGNMENT SYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    def _initialize_weapon_assignments(self):
        """Initialize weapon assignments with default values (all weapons to primary)"""
        self.weapon_assignments = {}
        
        # Assign all weapon arrays to primary by default
        for i in range(len(self.player_ship.weapon_arrays)):
            self.weapon_assignments[f'array_{i}'] = 'primary'
        
        # Assign all torpedo bays to primary by default
        for i in range(len(self.player_ship.torpedo_bays)):
            self.weapon_assignments[f'torpedo_{i}'] = 'primary'
    
    def _cycle_weapon_target(self, weapon_key):
        """Cycle a weapon's target assignment (only includes targets in arc)"""
        targets = self.ship_targets.get(self.player_ship, {})
        
        # Get the weapon object to check firing arcs
        weapon = None
        weapon_type = None
        if weapon_key.startswith('array_'):
            weapon_index = int(weapon_key.split('_')[1])
            if weapon_index < len(self.player_ship.weapon_arrays):
                weapon = self.player_ship.weapon_arrays[weapon_index]
                weapon_type = 'array'
        elif weapon_key.startswith('torpedo_'):
            weapon_index = int(weapon_key.split('_')[1])
            if weapon_index < len(self.player_ship.torpedo_bays):
                weapon = self.player_ship.torpedo_bays[weapon_index]
                weapon_type = 'torpedo'
        
        if not weapon:
            return
        
        # Build list of targets that are actually in arc for this weapon
        available = []
        for priority in ['primary', 'secondary', 'tertiary']:
            target = targets.get(priority)
            if target:
                # Check if target is in this weapon's arc
                target_arc = self.player_ship.get_target_arc(target.hex_q, target.hex_r)
                if target_arc in weapon.firing_arcs:
                    available.append(priority)
        
        if not available:
            # No targets in arc for this weapon
            self.add_to_log(f"{weapon.weapon_type} Mk{weapon.mark} has no targets in arc!")
            return
        
        current = self.weapon_assignments.get(weapon_key, 'primary')
        
        # Find current index and cycle to next
        if current in available:
            current_index = available.index(current)
            next_index = (current_index + 1) % len(available)
            self.weapon_assignments[weapon_key] = available[next_index]
        else:
            # Default to first available
            self.weapon_assignments[weapon_key] = available[0]
            
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
        
        # Initialize combat results for this firing phase (only on first ship firing)
        if self.current_ship_index == 0:
            self.combat_results = {
                'player': {'hits': [], 'misses': [], 'damage_taken': 0, 'shields_lost': 0, 'hull_lost': 0},
                'enemy': {'hits': [], 'misses': [], 'damage_dealt': 0, 'shields_lost': 0, 'hull_lost': 0, 'distance': 0}
            }
            
        attacker = self.player_ship
        
        # Get targets from targeting phase
        targets = self.ship_targets.get(attacker, {})
        primary = targets.get('primary')
        secondary = targets.get('secondary')
        tertiary = targets.get('tertiary')
        
        # Build target map with accuracy penalties
        target_map = {}
        if primary:
            target_map['primary'] = (primary, 1.0)
        if secondary:
            target_map['secondary'] = (secondary, 0.75)
        if tertiary:
            target_map['tertiary'] = (tertiary, 0.5)
        
        # Fire weapons according to assignments (or all at primary if single target)
        fired_at_any = False
        
        # Fire weapon arrays
        for i, weapon_array in enumerate(attacker.weapon_arrays):
            weapon_key = f'array_{i}'
            assigned_priority = self.weapon_assignments.get(weapon_key, 'primary')
            
            if assigned_priority in target_map:
                target, accuracy = target_map[assigned_priority]
                if target.hull > 0:  # Don't shoot destroyed targets
                    self._fire_weapon_at_target(attacker, weapon_array, target, accuracy, assigned_priority.upper(), i)
                    fired_at_any = True
        
        # Fire torpedoes
        for i, torpedo in enumerate(attacker.torpedo_bays):
            weapon_key = f'torpedo_{i}'
            assigned_priority = self.weapon_assignments.get(weapon_key, 'primary')
            
            if assigned_priority in target_map:
                target, accuracy = target_map[assigned_priority]
                if target.hull > 0:  # Don't shoot destroyed targets
                    self._fire_torpedo_at_target(attacker, torpedo, target, accuracy, assigned_priority.upper(), i)
                    fired_at_any = True
        
        if not fired_at_any:
            self.add_to_log("No weapons fired!")
        
        # Check if any target destroyed
        for target in [primary, secondary, tertiary]:
            if target and target.hull <= 0:
                self.add_to_log(f"*** {target.name} DESTROYED! ***")
        
        # Don't show summary yet - wait until all ships have fired
        # Summary will be shown when advancing from firing phase
        
        # Mark action complete - next ship fires
        self.complete_ship_action()
    
    def _fire_weapon_at_target(self, attacker, weapon, target, accuracy_penalty, target_label, weapon_index):
        """Fire a single weapon array at a target
        
        Args:
            attacker: Ship firing weapon
            weapon: WeaponArray object
            target: Ship being fired at
            accuracy_penalty: Multiplier for accuracy
            target_label: String label for logging
            weapon_index: Index of weapon in ship's array
        """
        if not weapon.can_fire():
            return
        
        # Calculate distance and target arc
        distance = self.hex_grid.distance(
            attacker.hex_q, attacker.hex_r,
            target.hex_q, target.hex_r
        )
        
        # Store distance for combat results
        if attacker == self.player_ship:
            self.combat_results['enemy']['distance'] = distance
        
        target_arc = attacker.get_target_arc(target.hex_q, target.hex_r)
        shield_facing_hit = target.get_shield_facing_hit(attacker.hex_q, attacker.hex_r)
        
        # Check if weapon is in arc
        if target_arc not in weapon.firing_arcs:
            return
        
        # Check if in range (max 12 hexes for energy weapons)
        if distance > 12:
            return
        
        crew_bonus = attacker.get_crew_bonus()
        damage = weapon.fire(crew_bonus)
        
        # Apply sensor accuracy modifier
        accuracy_mod = attacker.get_targeting_accuracy(distance)
        if accuracy_mod is None:
            return
        
        # Apply multi-target accuracy penalty
        accuracy_mod *= accuracy_penalty
        actual_damage = int(damage * accuracy_mod)
        
        # Track hit/miss
        is_hit = actual_damage > 0
        if attacker == self.player_ship:
            if is_hit:
                self.combat_results['enemy']['hits'].append({
                    'weapon': weapon.weapon_type.upper(),
                    'damage': actual_damage
                })
                logger.info(f"{attacker.name} {weapon.weapon_type} HIT {target.name} for {actual_damage} damage")
            else:
                self.combat_results['enemy']['misses'].append(weapon.weapon_type.upper())
                logger.debug(f"{attacker.name} {weapon.weapon_type} MISSED {target.name}")
        else:
            if is_hit:
                self.combat_results['player']['hits'].append({
                    'weapon': weapon.weapon_type.upper(),
                    'damage': actual_damage
                })
            else:
                self.combat_results['player']['misses'].append(weapon.weapon_type.upper())
        
        # Create visual effect
        if self.phaser_beam_components:
            attacker_pos = attacker.position if attacker.position else self.hex_grid.axial_to_pixel(attacker.hex_q, attacker.hex_r)
            target_pos = target.position if target.position else self.hex_grid.axial_to_pixel(target.hex_q, target.hex_r)
            
            beam_effect = WeaponBeamEffect(
                attacker_pos,
                target_pos,
                self.phaser_beam_components,
                self.impact_effects.get('phaser_hit'),
                weapon_type=weapon.weapon_type
            )
            self.active_weapon_effects.append(beam_effect)
            
            # Play phaser sound effect
            if self.phaser_sound:
                self.phaser_sound.play()
        
        # Apply damage using ship's method (includes system damage)
        damage_result = target.take_damage(actual_damage, shield_facing_hit)
        shield_damage = actual_damage - damage_result.get('hull_damage', 0)
        hull_damage = damage_result.get('hull_damage', 0)
        
        # Log system damage if any occurred
        if damage_result.get('system_damage'):
            for sys_dmg in damage_result['system_damage']:
                if sys_dmg['destroyed']:
                    self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system'].upper()} DESTROYED!")
                elif sys_dmg['new_health'] < 30:
                    self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system']} critical ({sys_dmg['new_health']:.0f}%)")
        
        # Check for warp core breach or hull failure
        if damage_result.get('warp_core_breach'):
            if damage_result.get('breach_survived'):
                self.add_to_log(f"  💥 WARP CORE BREACH! Crew evacuated!")
            else:
                self.add_to_log(f"  💥💥💥 CATASTROPHIC WARP CORE BREACH! {target.name} DESTROYED! 💥💥💥")
        elif damage_result.get('disabled'):
            self.add_to_log(f"  *** {target.name} DISABLED - Hull integrity failure! ***")
        
        # Track damage totals
        if attacker == self.player_ship:
            self.combat_results['enemy']['damage_dealt'] += shield_damage + hull_damage
            self.combat_results['enemy']['shields_lost'] += shield_damage
            self.combat_results['enemy']['hull_lost'] += hull_damage
        else:
            self.combat_results['player']['damage_taken'] += shield_damage + hull_damage
            self.combat_results['player']['shields_lost'] += shield_damage
            self.combat_results['player']['hull_lost'] += hull_damage
        
        # Log
        penalty_text = f" ({int(accuracy_penalty*100)}%)" if accuracy_penalty < 1.0 else ""
        if hull_damage > 0:
            self.add_to_log(f"{weapon.weapon_type.upper()} → {target_label}: {shield_damage} shield, {hull_damage} hull{penalty_text}")
        else:
            self.add_to_log(f"{weapon.weapon_type.upper()} → {target_label}: {shield_damage} to {shield_facing_hit} shields{penalty_text}")
    
    def _fire_torpedo_at_target(self, attacker, torpedo, target, accuracy_penalty, target_label, torpedo_index):
        """Fire a single torpedo at a target
        
        Args:
            attacker: Ship firing torpedo
            torpedo: TorpedoBay object
            target: Ship being fired at
            accuracy_penalty: Multiplier for accuracy
            target_label: String label for logging
            torpedo_index: Index of torpedo in ship's bays
        """
        if not torpedo.can_fire():
            return
        
        # Calculate distance and target arc
        distance = self.hex_grid.distance(
            attacker.hex_q, attacker.hex_r,
            target.hex_q, target.hex_r
        )
        
        # Store distance for combat results
        if attacker == self.player_ship:
            self.combat_results['enemy']['distance'] = distance
        
        target_arc = attacker.get_target_arc(target.hex_q, target.hex_r)
        shield_facing_hit = target.get_shield_facing_hit(attacker.hex_q, attacker.hex_r)
        
        # Check if torpedo is in arc
        if target_arc not in torpedo.firing_arcs:
            return
        
        # Check if in range (max 15 hexes for torpedoes)
        if distance > 15:
            return
        
        crew_bonus = attacker.get_crew_bonus()
        damage = torpedo.fire(crew_bonus)
        
        # Create visual effect
        if self.torpedo_sprites.get(torpedo.torpedo_type):
            attacker_pos = attacker.position if attacker.position else self.hex_grid.axial_to_pixel(attacker.hex_q, attacker.hex_r)
            target_pos = target.position if target.position else self.hex_grid.axial_to_pixel(target.hex_q, target.hex_r)
            
            torpedo_effect = TorpedoProjectileEffect(
                attacker_pos,
                target_pos,
                self.torpedo_sprites.get(torpedo.torpedo_type),
                self.impact_effects.get('phaser_hit'),
                torpedo_type=torpedo.torpedo_type
            )
            self.active_weapon_effects.append(torpedo_effect)
        
        # Apply sensor accuracy modifier
        accuracy_mod = attacker.get_targeting_accuracy(distance)
        if accuracy_mod is None:
            return
        
        # Apply multi-target accuracy penalty
        accuracy_mod *= accuracy_penalty
        actual_damage = int(damage * accuracy_mod)
        
        # Track torpedo hit/miss
        is_hit = actual_damage > 0
        if attacker == self.player_ship:
            if is_hit:
                self.combat_results['enemy']['hits'].append({
                    'weapon': f"{torpedo.torpedo_type.upper()} TORPEDO",
                    'damage': actual_damage
                })
            else:
                self.combat_results['enemy']['misses'].append(f"{torpedo.torpedo_type.upper()} TORPEDO")
        else:
            if is_hit:
                self.combat_results['player']['hits'].append({
                    'weapon': f"{torpedo.torpedo_type.upper()} TORPEDO",
                    'damage': actual_damage
                })
            else:
                self.combat_results['player']['misses'].append(f"{torpedo.torpedo_type.upper()} TORPEDO")
        
        # Torpedoes: 90% blocked by shields, 10% bleeds through to hull
        # Apply damage using ship's method (includes system damage)
        damage_result = target.take_damage(actual_damage, shield_facing_hit)
        
        shield_damage = int(actual_damage * 0.9)
        hull_damage = damage_result.get('hull_damage', 0)
        
        # Log system damage if any occurred
        if damage_result.get('system_damage'):
            for sys_dmg in damage_result['system_damage']:
                if sys_dmg['destroyed']:
                    self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system'].upper()} DESTROYED!")
                elif sys_dmg['new_health'] < 30:
                    self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system']} critical ({sys_dmg['new_health']:.0f}%)")
        
        # Check for warp core breach or hull failure
        if damage_result.get('warp_core_breach'):
            if damage_result.get('breach_survived'):
                self.add_to_log(f"  💥 WARP CORE BREACH! Crew evacuated!")
            else:
                self.add_to_log(f"  💥💥💥 CATASTROPHIC WARP CORE BREACH! {target.name} DESTROYED! 💥💥💥")
        elif damage_result.get('disabled'):
            self.add_to_log(f"  *** {target.name} DISABLED - Hull integrity failure! ***")
        
        # Track torpedo damage totals
        if attacker == self.player_ship:
            self.combat_results['enemy']['damage_dealt'] += shield_damage + hull_damage
            self.combat_results['enemy']['shields_lost'] += shield_damage
            self.combat_results['enemy']['hull_lost'] += hull_damage
        else:
            self.combat_results['player']['damage_taken'] += shield_damage + hull_damage
            self.combat_results['player']['shields_lost'] += shield_damage
            self.combat_results['player']['hull_lost'] += hull_damage
        
        # Log
        penalty_text = f" ({int(accuracy_penalty*100)}%)" if accuracy_penalty < 1.0 else ""
        self.add_to_log(f"TORPEDO → {target_label}: {shield_damage} shield, {hull_damage} hull{penalty_text}")
    
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
        
        # Store distance for combat results (used for detail level)
        if attacker == self.player_ship:
            self.combat_results['enemy']['distance'] = distance
        
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
                
                # Track hit/miss (miss if actual_damage is very low due to accuracy)
                is_hit = actual_damage > 0
                if attacker == self.player_ship:
                    if is_hit:
                        self.combat_results['enemy']['hits'].append({
                            'weapon': weapon.weapon_type.upper(),
                            'damage': actual_damage
                        })
                    else:
                        self.combat_results['enemy']['misses'].append(weapon.weapon_type.upper())
                else:  # Enemy hit player
                    if is_hit:
                        self.combat_results['player']['hits'].append({
                            'weapon': weapon.weapon_type.upper(),
                            'damage': actual_damage
                        })
                        logger.info(f"{attacker.name} {weapon.weapon_type} HIT {target.name} for {actual_damage} damage")
                    else:
                        self.combat_results['player']['misses'].append(weapon.weapon_type.upper())
                        logger.debug(f"{attacker.name} {weapon.weapon_type} MISSED {target.name}")
                
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
                    
                    # Play phaser sound effect
                    if self.phaser_sound:
                        self.phaser_sound.play()
                
                # Energy weapons: apply damage using ship's method (includes system damage)
                damage_result = target.take_damage(actual_damage, shield_facing_hit)
                shield_damage = actual_damage - damage_result.get('hull_damage', 0)
                hull_damage = damage_result.get('hull_damage', 0)
                
                # Log system damage if any occurred
                if damage_result.get('system_damage'):
                    for sys_dmg in damage_result['system_damage']:
                        if sys_dmg['destroyed']:
                            self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system'].upper()} DESTROYED!")
                        elif sys_dmg['new_health'] < 30:
                            self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system']} critical ({sys_dmg['new_health']:.0f}%)")
                
                # Check for warp core breach or hull failure
                if damage_result.get('warp_core_breach'):
                    if damage_result.get('breach_survived'):
                        self.add_to_log(f"  💥 WARP CORE BREACH! Crew evacuated!")
                    else:
                        self.add_to_log(f"  💥💥💥 CATASTROPHIC WARP CORE BREACH! {target.name} DESTROYED! 💥💥💥")
                elif damage_result.get('disabled'):
                    self.add_to_log(f"  *** {target.name} DISABLED - Hull integrity failure! ***")
                
                # Track damage totals
                if attacker == self.player_ship:
                    self.combat_results['enemy']['damage_dealt'] += shield_damage + hull_damage
                    self.combat_results['enemy']['shields_lost'] += shield_damage
                    self.combat_results['enemy']['hull_lost'] += hull_damage
                else:
                    self.combat_results['player']['damage_taken'] += shield_damage + hull_damage
                    self.combat_results['player']['shields_lost'] += shield_damage
                    self.combat_results['player']['hull_lost'] += hull_damage
                
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
                
                # Track torpedo hit/miss
                is_hit = actual_damage > 0
                if attacker == self.player_ship:
                    if is_hit:
                        self.combat_results['enemy']['hits'].append({
                            'weapon': f"{torpedo.torpedo_type.upper()} TORPEDO",
                            'damage': actual_damage
                        })
                    else:
                        self.combat_results['enemy']['misses'].append(f"{torpedo.torpedo_type.upper()} TORPEDO")
                else:  # Enemy hit player
                    if is_hit:
                        self.combat_results['player']['hits'].append({
                            'weapon': f"{torpedo.torpedo_type.upper()} TORPEDO",
                            'damage': actual_damage
                        })
                        logger.info(f"{attacker.name} {torpedo.torpedo_type} torpedo HIT {target.name} for {actual_damage} damage")
                    else:
                        self.combat_results['player']['misses'].append(f"{torpedo.torpedo_type.upper()} TORPEDO")
                        logger.debug(f"{attacker.name} {torpedo.torpedo_type} torpedo MISSED {target.name}")
                
                # Torpedoes: apply damage using ship's method (includes system damage)
                damage_result = target.take_damage(actual_damage, shield_facing_hit)
                
                shield_damage = int(actual_damage * 0.9)
                hull_damage = damage_result.get('hull_damage', 0)
                
                # Log system damage if any occurred
                if damage_result.get('system_damage'):
                    for sys_dmg in damage_result['system_damage']:
                        if sys_dmg['destroyed']:
                            self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system'].upper()} DESTROYED!")
                        elif sys_dmg['new_health'] < 30:
                            self.add_to_log(f"  ⚠ {target.name}: {sys_dmg['system']} critical ({sys_dmg['new_health']:.0f}%)")
                
                # Check for warp core breach or hull failure
                if damage_result.get('warp_core_breach'):
                    if damage_result.get('breach_survived'):
                        self.add_to_log(f"  💥 WARP CORE BREACH! Crew evacuated!")
                    else:
                        self.add_to_log(f"  💥💥💥 CATASTROPHIC WARP CORE BREACH! {target.name} DESTROYED! 💥💥💥")
                elif damage_result.get('disabled'):
                    self.add_to_log(f"  *** {target.name} DISABLED - Hull integrity failure! ***")
                
                # Track torpedo damage totals
                if attacker == self.player_ship:
                    self.combat_results['enemy']['damage_dealt'] += shield_damage + hull_damage
                    self.combat_results['enemy']['shields_lost'] += shield_damage
                    self.combat_results['enemy']['hull_lost'] += hull_damage
                else:
                    self.combat_results['player']['damage_taken'] += shield_damage + hull_damage
                    self.combat_results['player']['shields_lost'] += shield_damage
                    self.combat_results['player']['hull_lost'] += hull_damage
                
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
        # Clear animation state first (before recreating ships)
        self.animating_ship = None
        self.animation_start_pos = None
        self.animation_end_pos = None
        self.animation_start_facing = None
        self.animation_end_facing = None
        self.animation_progress = 0.0
        self.animation_callback = None
        self.pending_ai_moves.clear()
        
        # Recreate ships from config
        self._create_ships_from_config()
        
        # Reset combat state
        self.turn_number = 0  # Will be 1 after start_new_turn
        self.player_turn = True
        self.combat_log.clear()
        self.combat_phase = "initiative"
        self.current_ship_index = 0
        self.actions_completed = {k: False for k in self.actions_completed}
        
        # Note: AI controllers are already created by _create_ships_from_config()
        # No need to recreate them here
        
        self.add_to_log("Arena reset")
        # Note: start_new_turn() is already called by _create_ships_from_config()
        
    def exit_to_menu(self):
        """Return to main menu"""
        self.next_screen = "main_menu"
    
    def render_text_fitted(self, text, max_width, color, font=None):
        """
        Render text that fits within max_width, automatically reducing font size if needed.
        Returns the rendered surface.
        """
        if font is None:
            font = self.font_small
        
        # Try rendering with the provided font first
        surface = font.render(text, True, color)
        
        # If it fits, return it
        if surface.get_width() <= max_width:
            return surface
        
        # Otherwise, try progressively smaller fonts
        font_sizes = [16, 14, 12, 10]
        for size in font_sizes:
            smaller_font = get_font(size)
            surface = smaller_font.render(text, True, color)
            if surface.get_width() <= max_width:
                return surface
        
        # If still too wide, truncate with ellipsis
        truncated = text
        while len(truncated) > 3:
            truncated = truncated[:-4] + "..."
            surface = get_font(10).render(truncated, True, color)
            if surface.get_width() <= max_width:
                return surface
        
        # Last resort: just render it anyway
        return surface
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Check if weapon assignment is showing - handle first
                if self.show_weapon_assignment:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.show_weapon_assignment = False
                        # Now fire weapons with the assignments
                        self.fire_weapons()
                    continue  # Don't process other keys while assignment is showing
                
                # Check if combat summary is showing - handle dismissal first
                if self.show_combat_summary:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.show_combat_summary = False
                        # After summary, advance to next phase (damage phase)
                        current_index = self.phase_order.index(self.combat_phase)
                        if current_index < len(self.phase_order) - 1:
                            self.combat_phase = self.phase_order[current_index + 1]
                            self.current_ship_index = 0
                            
                            # Auto-resolve damage and housekeeping phases
                            if self.combat_phase == "damage":
                                self.resolve_damage_phase()
                            elif self.combat_phase == "housekeeping":
                                self.resolve_housekeeping_phase()
                    continue  # Don't process other keys while summary is showing
                
                if event.key == pygame.K_ESCAPE:
                    self.exit_to_menu()
                elif event.key == pygame.K_SPACE:
                    if self.combat_phase == "firing":
                        self.fire_weapons()
                elif event.key == pygame.K_RETURN:
                    # Only allow ending turn during player's turn
                    current_ship = self.get_current_acting_ship()
                    if current_ship == self.player_ship:
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
                # Scroll weapons tab with UP/DOWN arrows
                elif event.key == pygame.K_UP:
                    if self.status_panel.active_tab == 1:  # WEAPONS tab (index 1)
                        self.weapons_scroll_offset = max(0, self.weapons_scroll_offset - 30)
                elif event.key == pygame.K_DOWN:
                    if self.status_panel.active_tab == 1:  # WEAPONS tab (index 1)
                        self.weapons_scroll_offset = min(self.weapons_max_scroll, self.weapons_scroll_offset + 30)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse wheel scrolling for weapons tab
                if event.button == 4:  # Scroll up
                    if self.show_weapon_assignment:
                        # Check which box the mouse is over
                        mouse_pos = pygame.mouse.get_pos()
                        window_width = 800
                        window_x = (self.screen_width - window_width) // 2
                        box_width = (window_width - 60) // 2
                        phaser_box_x = window_x + 20
                        torpedo_box_x = phaser_box_x + box_width + 20
                        box_y = ((self.screen_height - 650) // 2) + 180
                        
                        if phaser_box_x <= mouse_pos[0] < phaser_box_x + box_width and box_y <= mouse_pos[1] < box_y + 380:
                            self.weapon_assign_phaser_scroll = max(0, self.weapon_assign_phaser_scroll - 30)
                        elif torpedo_box_x <= mouse_pos[0] < torpedo_box_x + box_width and box_y <= mouse_pos[1] < box_y + 380:
                            self.weapon_assign_torpedo_scroll = max(0, self.weapon_assign_torpedo_scroll - 30)
                    elif self.status_panel.active_tab == 1:  # WEAPONS tab (index 1)
                        self.weapons_scroll_offset = max(0, self.weapons_scroll_offset - 30)
                    continue
                elif event.button == 5:  # Scroll down
                    if self.show_weapon_assignment:
                        # Check which box the mouse is over
                        mouse_pos = pygame.mouse.get_pos()
                        window_width = 800
                        window_x = (self.screen_width - window_width) // 2
                        box_width = (window_width - 60) // 2
                        phaser_box_x = window_x + 20
                        torpedo_box_x = phaser_box_x + box_width + 20
                        box_y = ((self.screen_height - 650) // 2) + 180
                        
                        if phaser_box_x <= mouse_pos[0] < phaser_box_x + box_width and box_y <= mouse_pos[1] < box_y + 380:
                            # Calculate max scroll for phasers
                            max_scroll = len(self.player_ship.weapon_arrays) * 24 - 335
                            self.weapon_assign_phaser_scroll = min(max(0, max_scroll), self.weapon_assign_phaser_scroll + 30)
                        elif torpedo_box_x <= mouse_pos[0] < torpedo_box_x + box_width and box_y <= mouse_pos[1] < box_y + 380:
                            # Calculate max scroll for torpedoes
                            max_scroll = len(self.player_ship.torpedo_bays) * 24 - 335
                            self.weapon_assign_torpedo_scroll = min(max(0, max_scroll), self.weapon_assign_torpedo_scroll + 30)
                    elif self.status_panel.active_tab == 1:  # WEAPONS tab (index 1)
                        self.weapons_scroll_offset = min(self.weapons_max_scroll, self.weapons_scroll_offset + 30)
                    continue
                
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if combat summary is showing - handle Continue button
                    if self.show_combat_summary:
                        if hasattr(self, '_summary_continue_button') and self._summary_continue_button.collidepoint(mouse_pos):
                            self.show_combat_summary = False
                            # After summary, advance to next phase (damage phase)
                            current_index = self.phase_order.index(self.combat_phase)
                            if current_index < len(self.phase_order) - 1:
                                self.combat_phase = self.phase_order[current_index + 1]
                                self.current_ship_index = 0
                                
                                # Auto-resolve damage and housekeeping phases
                                if self.combat_phase == "damage":
                                    self.resolve_damage_phase()
                                elif self.combat_phase == "housekeeping":
                                    self.resolve_housekeeping_phase()
                        continue  # Don't process other clicks while summary is showing
                    
                    # Check if weapon assignment window is showing
                    if self.show_weapon_assignment:
                        # Check if COMMIT button was clicked
                        if hasattr(self, '_weapon_commit_button') and self._weapon_commit_button.collidepoint(mouse_pos):
                            # Close weapon assignment and fire weapons
                            self.show_weapon_assignment = False
                            self.fire_weapons()
                        elif hasattr(self, '_weapon_click_areas'):
                            for weapon_key, click_rect in self._weapon_click_areas.items():
                                if click_rect.collidepoint(mouse_pos):
                                    self._cycle_weapon_target(weapon_key)
                                    break
                        continue  # Don't process other clicks while assignment is showing
                    
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
        
        # Check if we're waiting to show combat summary after weapon effects finish
        if self.pending_combat_summary and len(self.active_weapon_effects) == 0:
            self.pending_combat_summary = False
            self.show_combat_summary = True
        
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
        
        # Draw initiative tracker at the top
        self._draw_initiative_tracker()
        
        # Header (moved down slightly to accommodate initiative tracker)
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
        
        # Draw multi-hex ship outlines on grid (before ships)
        for ship in self.all_ships:
            color = LCARS_COLORS['blue'] if ship == self.player_ship else LCARS_COLORS['alert_red']
            self._draw_ship_hex_outlines(ship, color)
        
        # Draw ships on top of everything
        for ship in self.all_ships:
            color = LCARS_COLORS['blue'] if ship == self.player_ship else LCARS_COLORS['alert_red']
            # Debug: Track what we're drawing (only log once per second to avoid spam)
            if not hasattr(self, '_last_draw_log') or pygame.time.get_ticks() - self._last_draw_log > 1000:
                print(f"[DEBUG] Drawing {len(self.all_ships)} ships: {[s.name for s in self.all_ships]}")
                self._last_draw_log = pygame.time.get_ticks()
            self._draw_ship(ship, color)
        
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
        turn_surface = self.font_small.render(turn_text, True, LCARS_COLORS['light_blue'])
        self.screen.blit(turn_surface, (self.screen_width - 280, 60))
        
        # Draw current acting ship and phase
        current_ship = self.get_current_acting_ship()
        if current_ship:
            if current_ship == self.player_ship:
                status_text = "YOUR TURN"
                status_color = LCARS_COLORS['green']
            else:
                status_text = f"{current_ship.name.upper()}'S TURN"
                status_color = LCARS_COLORS['alert_red']
            status_surface = self.font_tiny.render(status_text, True, status_color)
            self.screen.blit(status_surface, (self.screen_width - 280, 85))
        
        # Draw phase indicator below
        phase_text = f"{self.combat_phase.upper()} PHASE"
        phase_color = get_accent_color()
        phase_surface = self.font_tiny.render(phase_text, True, phase_color)
        self.screen.blit(phase_surface, (self.screen_width - 280, 105))
        
        # Draw movement points if in movement phase
        if self.combat_phase == "movement" and current_ship == self.player_ship:
            mp_text = f"MOVEMENT: {self.movement_points_remaining}/{self.player_ship.impulse_speed}"
            mp_surface = self.font_tiny.render(mp_text, True, LCARS_COLORS['green'])
            self.screen.blit(mp_surface, (self.screen_width - 280, 125))
        
        # Draw controls hint - positioned well above combat log
        hint_y = self.screen_height - 145  # Much higher to avoid combat log overlap
        
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
        
        hint_surface = self.render_text_fitted(hint_text, self.screen_width - 100, LCARS_COLORS['text_gray'], self.font_tiny)
        hint_rect = hint_surface.get_rect(center=(self.screen_width // 2, hint_y))
        self.screen.blit(hint_surface, hint_rect)
        
        # Draw weapon assignment popup if showing
        if self.show_weapon_assignment:
            self._draw_weapon_assignment()
        
        # Draw combat summary popup if showing
        if self.show_combat_summary:
            self._draw_combat_summary()
        
        pygame.display.flip()
    
    def _draw_initiative_tracker(self):
        """Draw initiative order tracker at the top of the screen"""
        if not self.initiative_order or len(self.initiative_order) == 0:
            return
        
        # Configuration
        tracker_y = 70  # Y position for the tracker
        ship_icon_size = 50  # Size of ship sprite in tracker
        ship_spacing = 120  # Horizontal spacing between ships
        
        # Calculate total width and starting X position (centered)
        total_width = len(self.initiative_order) * ship_spacing
        start_x = (self.screen_width - total_width) // 2 + ship_spacing // 2
        
        # Draw background panel for tracker
        panel_height = 80
        panel_rect = pygame.Rect(start_x - 60, tracker_y - 40, total_width, panel_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_medium'], panel_rect)
        pygame.draw.rect(self.screen, get_accent_color(), panel_rect, 2)
        
        # Get current acting ship
        current_ship = self.get_current_acting_ship()
        
        # Draw each ship in initiative order
        for idx, ship in enumerate(self.initiative_order):
            x = start_x + (idx * ship_spacing)
            y = tracker_y
            
            # Determine faction and colors
            faction = getattr(ship, 'faction', 'neutral')
            if faction == 'friendly':
                glow_color = LCARS_COLORS['blue']
                border_color = LCARS_COLORS['green']
            elif faction == 'enemy':
                glow_color = LCARS_COLORS['alert_red']
                border_color = LCARS_COLORS['alert_red']
            else:
                glow_color = (255, 255, 255)  # White for neutral
                border_color = LCARS_COLORS['light_blue']
            
            # Draw glow effect if this is the active ship
            if ship == current_ship:
                glow_radius = ship_icon_size // 2 + 15
                # Draw multiple circles with decreasing alpha for glow effect
                for i in range(5):
                    alpha = 255 - (i * 40)
                    radius = glow_radius - (i * 3)
                    glow_surface = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (*glow_color, alpha), (radius + 5, radius + 5), radius, 3)
                    glow_rect = glow_surface.get_rect(center=(x, y))
                    self.screen.blit(glow_surface, glow_rect)
            
            # Draw ship sprite (scaled down for tracker)
            try:
                # Get ship sprite with facing 0 (standardized orientation for tracker)
                if ship.ship_class in self.ship_sprite_cache:
                    # Use a small scale factor for the tracker
                    tracker_scale = 0.4  # Even smaller for tracker
                    
                    # Try to get cached sprite at tracker scale
                    if tracker_scale in self.ship_sprite_cache[ship.ship_class]:
                        ship_sprite = self.ship_sprite_cache[ship.ship_class][tracker_scale][0]
                    else:
                        # Scale from existing cached sprite
                        if 1.0 in self.ship_sprite_cache[ship.ship_class]:
                            base_sprite = self.ship_sprite_cache[ship.ship_class][1.0][0]
                        else:
                            # Get any available scale
                            available_scale = list(self.ship_sprite_cache[ship.ship_class].keys())[0]
                            base_sprite = self.ship_sprite_cache[ship.ship_class][available_scale][0]
                        
                        # Scale down to tracker size
                        sprite_width = int(base_sprite.get_width() * tracker_scale)
                        sprite_height = int(base_sprite.get_height() * tracker_scale)
                        ship_sprite = pygame.transform.smoothscale(base_sprite, (sprite_width, sprite_height))
                else:
                    # No sprite cached, create a simple placeholder
                    ship_sprite = pygame.Surface((ship_icon_size, ship_icon_size), pygame.SRCALPHA)
                    pygame.draw.circle(ship_sprite, border_color, (ship_icon_size // 2, ship_icon_size // 2), ship_icon_size // 3)
                
                # Draw the sprite
                sprite_rect = ship_sprite.get_rect(center=(x, y))
                self.screen.blit(ship_sprite, sprite_rect)
                
            except Exception as e:
                # Fallback: draw a simple circle if sprite fails
                pygame.draw.circle(self.screen, border_color, (x, y), ship_icon_size // 3, 2)
            
            # Draw border around ship icon
            if ship == current_ship:
                # Thicker border for active ship
                pygame.draw.circle(self.screen, border_color, (x, y), ship_icon_size // 2 + 5, 4)
            else:
                # Regular border
                pygame.draw.circle(self.screen, border_color, (x, y), ship_icon_size // 2 + 5, 2)
            
            # Draw ship name below icon (truncated if too long)
            name_text = ship.name if len(ship.name) <= 12 else ship.name[:10] + "..."
            name_surface = self.font_tiny.render(name_text, True, border_color)
            name_rect = name_surface.get_rect(center=(x, y + 35))
            self.screen.blit(name_surface, name_rect)
            
            # Draw initiative value if ship has one
            if hasattr(ship, 'initiative'):
                init_text = f"{ship.initiative}"
                init_surface = self.font_tiny.render(init_text, True, LCARS_COLORS['text_gray'])
                init_rect = init_surface.get_rect(center=(x, y + 50))
                self.screen.blit(init_surface, init_rect)
        
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
            
    def _draw_ship(self, ship, color):
        """Draw a ship sprite"""
        # Safety check: if position is None, recalculate from hex coordinates
        if ship.position is None:
            ship.position = self.hex_grid.axial_to_pixel(ship.hex_q, ship.hex_r)
        
        x, y = ship.position
        
        # Check if this is the currently active ship
        current_ship = self.get_current_acting_ship()
        is_active = (ship == current_ship)
        
        # Draw glow effect around active ship
        if is_active:
            # Determine glow color based on faction
            faction = getattr(ship, 'faction', 'neutral')
            if faction == 'friendly':
                glow_color = LCARS_COLORS['blue']  # Blue for friendly
            elif faction == 'enemy':
                glow_color = LCARS_COLORS['alert_red']  # Red for hostile
            else:
                glow_color = (255, 255, 255)  # White for neutral
            
            # Draw animated pulsing glow effect
            # Use time to create pulsing animation
            pulse = (pygame.time.get_ticks() % 2000) / 2000.0  # 0.0 to 1.0 over 2 seconds
            pulse_size = 10 + int(10 * math.sin(pulse * math.pi * 2))  # Oscillate between 10 and 20
            
            # Draw multiple layers of circles for glow effect
            for i in range(6):
                alpha = 200 - (i * 30)  # Decreasing opacity
                radius = 60 + pulse_size - (i * 8)  # Decreasing radius
                
                # Create a surface for the glow circle with alpha
                glow_surface = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*glow_color, alpha), (radius + 10, radius + 10), radius, 4)
                
                glow_rect = glow_surface.get_rect(center=(int(x), int(y)))
                self.screen.blit(glow_surface, glow_rect)
        
        # Use animated facing if available, otherwise use discrete facing
        if hasattr(ship, '_anim_facing') and ship._anim_facing is not None:
            facing_value = ship._anim_facing
        else:
            facing_value = ship.facing
        
        # Determine sprite scale based on ship size
        if ship.size == "Small":
            scale_factor = 0.7
        elif ship.size == "Medium":
            scale_factor = 1.0
        elif ship.size == "Large":
            scale_factor = 1.3
        elif ship.size == "Very Large":
            scale_factor = 2.0
        elif ship.size == "Huge":
            scale_factor = 2.5
        else:
            scale_factor = 1.0  # Default
        
        # Get discrete facing for sprite selection
        discrete_facing = int(facing_value) % 6
        
        # Try to use pre-rendered sprite from cache for maximum quality
        if ship.ship_class in self.ship_sprite_cache and scale_factor in self.ship_sprite_cache[ship.ship_class]:
            # Use pre-rendered sprite - zero quality loss!
            rotated_sprite = self.ship_sprite_cache[ship.ship_class][scale_factor][discrete_facing]
        else:
            # Sprite not loaded yet - load it now
            self._load_ship_sprite(ship)
            
            # Try again after loading
            if ship.ship_class in self.ship_sprite_cache and scale_factor in self.ship_sprite_cache[ship.ship_class]:
                rotated_sprite = self.ship_sprite_cache[ship.ship_class][scale_factor][discrete_facing]
            else:
                # Fallback - create a simple placeholder on the fly
                sprite_size = int(self.hex_size * 1.5 * scale_factor)
                placeholder = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                center = sprite_size // 2
                pygame.draw.circle(placeholder, LCARS_COLORS['light_blue'], (center, center), 20)
                angle = 90 + (discrete_facing * 60)
                rotated_sprite = pygame.transform.rotozoom(placeholder, -angle, 1.0)
        
        # Get rect for centered drawing - ensure integer coordinates for pixel-perfect rendering
        sprite_rect = rotated_sprite.get_rect(center=(int(x), int(y)))
        
        # Draw sprite - blit to integer coordinates for crisp rendering
        self.screen.blit(rotated_sprite, sprite_rect)
        
        # Determine name color based on faction
        faction = getattr(ship, 'faction', 'neutral')
        if faction == 'friendly':
            name_color = LCARS_COLORS['green']  # Green for friendlies
        elif faction == 'enemy':
            name_color = LCARS_COLORS['alert_red']  # Red for enemies
        else:
            name_color = LCARS_COLORS['light_blue']  # Blue for neutrals
        
        # Draw ship name below - use fitted text to prevent overflow
        name_surface = self.render_text_fitted(ship.name, 150, name_color, self.font_tiny)
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
    
    def _draw_ship_hex_outlines(self, ship, color):
        """Draw hex outlines for multi-hex ships on top of the grid"""
        if ship.is_multi_hex():
            occupied_hexes = ship.get_occupied_hexes()
            for hex_q, hex_r in occupied_hexes:
                self.hex_grid.draw_hex(self.screen, hex_q, hex_r, color, 3)
        
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
            dist_surface = self.font_tiny.render(dist_text, True, color)
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
        title = self.font_tiny.render(ship_name, True, LCARS_COLORS['blue'])
        self.screen.blit(title, (x, y))
        y += 22
        
        # Ship class and registry
        class_text = f"CLASS: {ship.ship_class.upper()}"
        class_surface = self.font_tiny.render(class_text, True, LCARS_COLORS['purple'])
        self.screen.blit(class_surface, (x, y))
        y += 20
        
        registry_text = f"REGISTRY: {ship.registry}"
        registry_surface = self.font_tiny.render(registry_text, True, LCARS_COLORS['purple'])
        self.screen.blit(registry_surface, (x, y))
        y += 24
        
        # Hull
        hull_pct = int((ship.hull / ship.max_hull) * 100)
        hull_text = f"HULL: {int(ship.hull)}/{ship.max_hull} ({hull_pct}%)"
        hull_color = LCARS_COLORS['green'] if hull_pct > 75 else get_warning_color() if hull_pct > 50 else LCARS_COLORS['alert_red']
        hull_surface = self.font_tiny.render(hull_text, True, hull_color)
        self.screen.blit(hull_surface, (x, y))
        y += 24
        
        # Shields header
        shields_title = self.font_small.render("SHIELDS", True, LCARS_COLORS['light_blue'])
        self.screen.blit(shields_title, (x, y))
        y += 24
        
        # Shields (all arcs)
        for arc in ['fore', 'aft', 'port', 'starboard']:
            shield_val = int(ship.shields[arc])
            shield_max = ship.max_shields[arc]
            shield_pct = int((shield_val / shield_max) * 100) if shield_max > 0 else 0
            
            shield_text = f"{arc.upper()}: {shield_val}/{shield_max} ({shield_pct}%)"
            shield_color = LCARS_COLORS['light_blue'] if shield_pct > 50 else get_warning_color() if shield_pct > 25 else LCARS_COLORS['alert_red']
            shield_surface = self.font_tiny.render(shield_text, True, shield_color)
            self.screen.blit(shield_surface, (x, y))
            y += 18
        
        y += 15
        
        # Sensor info
        sensor_range = ship.get_effective_sensor_range()
        sensor_text = f"SENSOR RANGE: {sensor_range} hexes"
        sensor_surface = self.font_tiny.render(sensor_text, True, LCARS_COLORS['purple'])
        self.screen.blit(sensor_surface, (x, y))
        y += 20
        
        # Crew
        crew_text = f"CREW: {ship.crew_count}/{ship.max_crew}"
        crew_surface = self.font_tiny.render(crew_text, True, LCARS_COLORS['purple'])
        self.screen.blit(crew_surface, (x, y))
        y += 18
        
        crew_skill_text = f"SKILL LEVEL: {ship.crew_skill}"
        crew_skill_surface = self.font_tiny.render(crew_skill_text, True, LCARS_COLORS['purple'])
        self.screen.blit(crew_skill_surface, (x, y))
    
    def _draw_weapons_tab(self, x, y):
        """Draw WEAPONS tab - weapon arrays and torpedoes"""
        ship = self.player_ship
        
        # Calculate target arc if we have a target
        target_arc = ship.get_target_arc(self.target_ship.hex_q, self.target_ship.hex_r)
        
        # Max width for content (panel width minus padding)
        max_width = 340
        
        # Define scrollable area (leave room for scroll indicator)
        # Panel height is 530, tabs take ~40, we start at y which is ~210
        # Available height from content start to panel bottom: ~490 pixels
        # Leave 25 pixels for scroll indicator
        scroll_area_height = 450  # Height available for scrolling content
        scroll_start_y = y
        
        # Create a surface for scrollable content
        content_surface = pygame.Surface((max_width + 20, 2000), pygame.SRCALPHA)
        content_y = 0
        
        # Weapons header
        weapons_title = self.font_small.render("WEAPON ARRAYS", True, get_accent_color())
        content_surface.blit(weapons_title, (0, content_y))
        content_y += 24
        
        # Energy weapons
        for i, weapon in enumerate(ship.weapon_arrays):
            ready = weapon.can_fire()
            in_arc = target_arc in weapon.firing_arcs
            
            # Color: green if ready and in arc, red if not ready, gray if out of arc
            if not in_arc:
                status_color = LCARS_COLORS['text_gray']
                arc_indicator = "OUT OF ARC"
            elif ready:
                status_color = LCARS_COLORS['green']
                arc_indicator = "READY"
            else:
                status_color = LCARS_COLORS['alert_red']
                arc_indicator = f"CD: {weapon.cooldown_remaining}"
            
            weapon_text = f"{weapon.weapon_type.upper()} Mk{weapon.mark} [{arc_indicator}]"
            weapon_surface = self.render_text_fitted(weapon_text, max_width, status_color, self.font_tiny)
            content_surface.blit(weapon_surface, (0, content_y))
            content_y += 18
            
            # Weapon details - split into two lines if needed
            damage_text = f"  DMG: {weapon.get_damage()}"
            damage_surface = self.font_tiny.render(damage_text, True, status_color)
            content_surface.blit(damage_surface, (0, content_y))
            content_y += 16
            
            # Arcs on separate line
            arcs_text = f"  Arcs: {', '.join(weapon.firing_arcs)}"
            arcs_surface = self.render_text_fitted(arcs_text, max_width, status_color, self.font_tiny)
            content_surface.blit(arcs_surface, (0, content_y))
            content_y += 20
        
        content_y += 8
        
        # Torpedoes header
        torpedoes_title = self.font_small.render("TORPEDO BAYS", True, get_accent_color())
        content_surface.blit(torpedoes_title, (0, content_y))
        content_y += 24
        
        # Torpedoes
        for i, torpedo in enumerate(ship.torpedo_bays):
            ready = torpedo.can_fire()
            in_arc = target_arc in torpedo.firing_arcs
            
            # Color: green if ready and in arc, red if not ready, gray if out of arc
            if not in_arc:
                status_color = LCARS_COLORS['text_gray']
                arc_indicator = "OUT OF ARC"
            elif ready:
                status_color = LCARS_COLORS['green']
                arc_indicator = "READY"
            else:
                status_color = LCARS_COLORS['alert_red']
                arc_indicator = f"CD: {torpedo.cooldown_remaining}"
            
            torp_text = f"{torpedo.torpedo_type.upper()} Mk{torpedo.mark} [{arc_indicator}]"
            torp_surface = self.render_text_fitted(torp_text, max_width, status_color, self.font_tiny)
            content_surface.blit(torp_surface, (0, content_y))
            content_y += 18
            
            # Torpedo details - split into two lines
            damage_text = f"  DMG: {torpedo.get_damage()}"
            damage_surface = self.font_tiny.render(damage_text, True, status_color)
            content_surface.blit(damage_surface, (0, content_y))
            content_y += 16
            
            # Arcs on separate line
            arcs_text = f"  Arcs: {', '.join(torpedo.firing_arcs)}"
            arcs_surface = self.render_text_fitted(arcs_text, max_width, status_color, self.font_tiny)
            content_surface.blit(arcs_surface, (0, content_y))
            content_y += 25
        
        content_y += 10
        
        # Target arc display
        arc_text = f"TARGET ARC: {target_arc.upper()}"
        arc_surface = self.font_small.render(arc_text, True, get_accent_color())
        content_surface.blit(arc_surface, (0, content_y))
        content_y += 20
        
        # Calculate max scroll based on content height
        self.weapons_max_scroll = max(0, content_y - scroll_area_height)
        
        # Clamp scroll offset
        self.weapons_scroll_offset = max(0, min(self.weapons_scroll_offset, self.weapons_max_scroll))
        
        # Blit the visible portion of content to screen
        self.screen.blit(content_surface, (x, scroll_start_y), 
                        area=pygame.Rect(0, self.weapons_scroll_offset, max_width + 20, scroll_area_height))
        
        # Draw scrollbar if content is scrollable
        if self.weapons_max_scroll > 0:
            scrollbar_x = x + max_width + 5
            scrollbar_y = scroll_start_y
            scrollbar_width = 8
            scrollbar_height = scroll_area_height
            
            # Draw scrollbar track (darker background)
            track_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
            pygame.draw.rect(self.screen, LCARS_COLORS['bg_dark'], track_rect)
            pygame.draw.rect(self.screen, LCARS_COLORS['text_gray'], track_rect, 1)
            
            # Calculate scrollbar thumb position and size
            scroll_percent = self.weapons_scroll_offset / self.weapons_max_scroll if self.weapons_max_scroll > 0 else 0
            visible_ratio = scroll_area_height / content_y  # How much content is visible
            thumb_height = max(20, int(scrollbar_height * visible_ratio))  # Minimum 20px
            thumb_y = scrollbar_y + int((scrollbar_height - thumb_height) * scroll_percent)
            
            # Draw scrollbar thumb (orange handle)
            thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)
            pygame.draw.rect(self.screen, LCARS_COLORS['orange'], thumb_rect)
            pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], thumb_rect, 1)
    
    def _draw_power_tab(self, x, y):
        """Draw POWER tab - power distribution (placeholder for now)"""
        ship = self.player_ship
        
        # Power header
        power_title = self.font_small.render("POWER SYSTEMS", True, get_accent_color())
        self.screen.blit(power_title, (x, y))
        y += 28
        
        # Placeholder text
        placeholder = self.font_tiny.render("Power management system", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder, (x, y))
        y += 18
        
        placeholder2 = self.font_tiny.render("coming soon...", True, LCARS_COLORS['text_gray'])
        self.screen.blit(placeholder2, (x, y))
        y += 28
        
        # Show some basic power info
        power_text = f"WARP CORE OUTPUT: 100%"
        power_surface = self.font_tiny.render(power_text, True, LCARS_COLORS['light_blue'])
        self.screen.blit(power_surface, (x, y))
        y += 24
        
        # Power distribution sections
        distributions = [
            ("WEAPONS", 25),
            ("SHIELDS", 25),
            ("ENGINES", 25),
            ("AUXILIARY", 25)
        ]
        
        for system, pct in distributions:
            dist_text = f"{system}: {pct}%"
            dist_surface = self.font_tiny.render(dist_text, True, LCARS_COLORS['purple'])
            self.screen.blit(dist_surface, (x, y))
            y += 18
    
    def _draw_damage_tab(self, x, y):
        """Draw DAMAGE tab - system health bars with color coding"""
        ship = self.player_ship
        
        # Max width for content
        max_width = 340
        
        # Damage header
        damage_title = self.font_small.render("DAMAGE CONTROL", True, get_accent_color())
        self.screen.blit(damage_title, (x, y))
        y += 28
        
        # Show hull integrity with bar
        hull_pct = int((ship.hull / ship.max_hull) * 100)
        hull_text = f"HULL INTEGRITY"
        hull_surface = self.font_tiny.render(hull_text, True, LCARS_COLORS['text_white'])
        self.screen.blit(hull_surface, (x, y))
        y += 16
        
        # Draw hull health bar
        self._draw_health_bar(x, y, hull_pct, 300)
        y += 20
        
        # Divider
        pygame.draw.line(self.screen, LCARS_COLORS['blue'], (x, y), (x + max_width, y), 1)
        y += 12
        
        # System status with health bars
        # Map internal system names to display names
        system_display_names = {
            'warp_core': 'WARP CORE',
            'life_support': 'LIFE SUPPORT',
            'shields': 'SHIELD GENERATORS',
            'weapons': 'WEAPON SYSTEMS',
            'impulse_engines': 'IMPULSE ENGINES',
            'warp_drive': 'WARP DRIVE',
            'sensors': 'SENSORS',
            'engineering': 'ENGINEERING',
            'sick_bay': 'SICK BAY',
            'auxiliary_systems': 'AUXILIARY'
        }
        
        # Draw each system with health bar
        for system_key, display_name in system_display_names.items():
            if system_key in ship.systems:
                health = int(ship.systems[system_key])
                
                # System name
                name_surface = self.font_tiny.render(display_name, True, LCARS_COLORS['text_white'])
                self.screen.blit(name_surface, (x, y))
                y += 14
                
                # Health bar
                self._draw_health_bar(x, y, health, 300)
                y += 16
    
    def _draw_health_bar(self, x, y, health_pct, bar_width):
        """
        Draw a color-coded health bar
        
        Args:
            x, y: Position to draw bar
            health_pct: Health percentage (0-100)
            bar_width: Width of the bar in pixels
        """
        bar_height = 8
        
        # Clamp health between 0-100
        health_pct = max(0, min(100, health_pct))
        
        # Calculate fill width
        fill_width = int((health_pct / 100.0) * bar_width)
        
        # Determine color based on health
        if health_pct > 75:
            bar_color = LCARS_COLORS['green']  # Green for healthy
        elif health_pct > 50:
            bar_color = (200, 200, 0)  # Yellow
        elif health_pct > 25:
            bar_color = LCARS_COLORS['orange']  # Orange
        else:
            bar_color = LCARS_COLORS['alert_red']  # Red for critical
        
        # Draw background (empty part)
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_medium'], bg_rect)
        
        # Draw filled part
        if fill_width > 0:
            fill_rect = pygame.Rect(x, y, fill_width, bar_height)
            pygame.draw.rect(self.screen, bar_color, fill_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, LCARS_COLORS['blue'], bg_rect, 1)
        
    def _draw_combat_log(self):
        """Draw combat log in bottom panel"""
        log_x = 70
        log_y = self.screen_height - 105
        
        # Title
        title = self.font_small.render("COMBAT LOG", True, get_accent_color())
        self.screen.blit(title, (log_x, log_y))
        log_y += 22
        
        # Log messages (last 3) - use fitted text to prevent overflow
        max_log_width = self.screen_width - 140  # Leave margin on both sides
        for message in self.combat_log:
            msg_surface = self.render_text_fitted(message, max_log_width, LCARS_COLORS['text_white'], self.font_tiny)
            self.screen.blit(msg_surface, (log_x, log_y))
            log_y += 18
    
    def _draw_combat_summary(self):
        """Draw combat damage summary popup window"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Calculate window dimensions
        window_width = 800
        window_height = 500
        window_x = (self.screen_width - window_width) // 2
        window_y = (self.screen_height - window_height) // 2
        
        # Draw main panel background
        panel_rect = pygame.Rect(window_x, window_y, window_width, window_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_dark'], panel_rect)
        pygame.draw.rect(self.screen, get_accent_color(), panel_rect, 3)
        
        # Title
        title = self.font_medium.render("FIRING PHASE COMPLETE", True, get_accent_color())
        title_rect = title.get_rect(center=(self.screen_width // 2, window_y + 30))
        self.screen.blit(title, title_rect)
        
        # Divider line
        pygame.draw.line(
            self.screen, 
            get_accent_color(), 
            (window_x + 20, window_y + 60), 
            (window_x + window_width - 20, window_y + 60), 
            2
        )
        
        # Get distance for enemy detail level
        distance = self.combat_results['enemy']['distance']
        
        # Split into two columns
        left_x = window_x + 30
        right_x = window_x + window_width // 2 + 15
        content_y = window_y + 80
        
        # LEFT COLUMN: Player Damage (always full detail)
        self._draw_summary_column(
            left_x, 
            content_y, 
            "DAMAGE TAKEN", 
            self.combat_results['player'], 
            detail_level='full'
        )
        
        # Vertical divider
        pygame.draw.line(
            self.screen,
            LCARS_COLORS['blue'],
            (window_x + window_width // 2, window_y + 100),
            (window_x + window_width // 2, window_y + window_height - 80),
            2
        )
        
        # RIGHT COLUMN: Enemy Damage (range-based detail)
        if distance <= 3:
            detail_level = 'full'
            range_text = "(POINT BLANK)"
        elif distance <= 6:
            detail_level = 'medium'
            range_text = "(CLOSE RANGE)"
        elif distance <= 9:
            detail_level = 'basic'
            range_text = "(MEDIUM RANGE)"
        else:
            detail_level = 'minimal'
            range_text = "(LONG RANGE)"
        
        self._draw_summary_column(
            right_x,
            content_y,
            f"DAMAGE DEALT {range_text}",
            self.combat_results['enemy'],
            detail_level=detail_level
        )
        
        # Continue button
        button_width = 200
        button_height = 40
        button_x = (self.screen_width - button_width) // 2
        button_y = window_y + window_height - 60
        
        # Store button rect for click detection
        self._summary_continue_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Draw button background
        pygame.draw.rect(self.screen, LCARS_COLORS['green'], self._summary_continue_button)
        pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], self._summary_continue_button, 2)
        
        # Draw button text
        button_text = self.font_medium.render("CONTINUE", True, LCARS_COLORS['bg_dark'])
        text_rect = button_text.get_rect(center=self._summary_continue_button.center)
        self.screen.blit(button_text, text_rect)
    
    def _draw_summary_column(self, x, y, title, data, detail_level='full'):
        """Draw a column of the combat summary with appropriate detail level"""
        # Title - use fitted text to ensure it doesn't overflow
        max_col_width = 350
        title_surface = self.render_text_fitted(title, max_col_width, LCARS_COLORS['light_blue'], self.font_small)
        self.screen.blit(title_surface, (x, y))
        y += 30
        
        if detail_level == 'minimal':
            # Only show if damage was dealt
            damage = data.get('damage_dealt', 0) + data.get('damage_taken', 0)
            if damage > 0:
                text = f"Damage Inflicted: {damage}"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['alert_red'])
                self.screen.blit(surface, (x, y))
                y += 20
                text = "Details obscured by range"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['text_gray'])
                self.screen.blit(surface, (x, y))
            else:
                text = "No confirmed hits"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['text_gray'])
                self.screen.blit(surface, (x, y))
            return
        
        if detail_level == 'basic':
            # Show totals only
            damage = data.get('damage_dealt', 0) + data.get('damage_taken', 0)
            shields = data['shields_lost']
            hull = data['hull_lost']
            
            text = f"Total Damage: {damage}"
            color = LCARS_COLORS['alert_red'] if damage > 0 else LCARS_COLORS['text_gray']
            surface = self.font_tiny.render(text, True, color)
            self.screen.blit(surface, (x, y))
            y += 20
            
            text = f"  Shield Damage: {shields}"
            surface = self.font_tiny.render(text, True, LCARS_COLORS['blue'])
            self.screen.blit(surface, (x, y))
            y += 18
            
            text = f"  Hull Damage: {hull}"
            color = LCARS_COLORS['alert_red'] if hull > 0 else LCARS_COLORS['text_gray']
            surface = self.font_tiny.render(text, True, color)
            self.screen.blit(surface, (x, y))
            y += 24
            
            hits = len(data['hits'])
            misses = len(data['misses'])
            text = f"Weapons: {hits} hit, {misses} missed"
            surface = self.font_tiny.render(text, True, LCARS_COLORS['text_white'])
            self.screen.blit(surface, (x, y))
            return
        
        if detail_level == 'medium' or detail_level == 'full':
            # Show detailed breakdown
            damage = data.get('damage_dealt', 0) + data.get('damage_taken', 0)
            shields = data['shields_lost']
            hull = data['hull_lost']
            
            # Total damage
            text = f"Total Damage: {damage}"
            color = LCARS_COLORS['alert_red'] if damage > 0 else LCARS_COLORS['text_gray']
            surface = self.font_tiny.render(text, True, color)
            self.screen.blit(surface, (x, y))
            y += 20
            
            text = f"  Shield Damage: {shields}"
            surface = self.font_tiny.render(text, True, LCARS_COLORS['blue'])
            self.screen.blit(surface, (x, y))
            y += 18
            
            text = f"  Hull Damage: {hull}"
            color = LCARS_COLORS['alert_red'] if hull > 0 else LCARS_COLORS['text_gray']
            surface = self.font_tiny.render(text, True, color)
            self.screen.blit(surface, (x, y))
            y += 26
            
            # Hits section
            if data['hits']:
                text = "HITS:"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['green'])
                self.screen.blit(surface, (x, y))
                y += 20
                
                for hit in data['hits']:
                    if detail_level == 'full':
                        text = f"  {hit['weapon']}: {hit['damage']} dmg"
                    else:
                        text = f"  {hit['weapon']}"
                    surface = self.font_tiny.render(text, True, LCARS_COLORS['text_white'])
                    self.screen.blit(surface, (x, y))
                    y += 18
                
                y += 8
            
            # Misses section
            if data['misses']:
                text = "MISSES:"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['text_gray'])
                self.screen.blit(surface, (x, y))
                y += 20
                
                for miss in data['misses']:
                    text = f"  {miss}"
                    surface = self.font_tiny.render(text, True, LCARS_COLORS['text_gray'])
                    self.screen.blit(surface, (x, y))
                    y += 18
            
            # Show "no weapons fired" if nothing happened
            if not data['hits'] and not data['misses']:
                text = "No weapons fired"
                surface = self.font_tiny.render(text, True, LCARS_COLORS['text_gray'])
                self.screen.blit(surface, (x, y))
    
    def _draw_weapon_assignment(self):
        """Draw weapon assignment popup for multi-target firing with separate phaser/torpedo boxes"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Calculate window dimensions
        window_width = 800
        window_height = 650
        window_x = (self.screen_width - window_width) // 2
        window_y = (self.screen_height - window_height) // 2
        
        # Draw main panel background
        panel_rect = pygame.Rect(window_x, window_y, window_width, window_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_dark'], panel_rect)
        pygame.draw.rect(self.screen, get_accent_color(), panel_rect, 3)
        
        # Title
        title = self.font_medium.render("ASSIGN WEAPONS TO TARGETS", True, get_accent_color())
        title_rect = title.get_rect(center=(self.screen_width // 2, window_y + 30))
        self.screen.blit(title, title_rect)
        
        # Divider line
        pygame.draw.line(
            self.screen,
            get_accent_color(),
            (window_x + 20, window_y + 60),
            (window_x + window_width - 20, window_y + 60),
            2
        )
        
        # Get targets and calculate arcs for each
        targets = self.ship_targets.get(self.player_ship, {})
        target_arcs = {}  # priority -> arc
        
        target_colors = {
            'primary': LCARS_COLORS['green'],
            'secondary': LCARS_COLORS['light_blue'],
            'tertiary': LCARS_COLORS['purple']
        }
        
        for priority in ['primary', 'secondary', 'tertiary']:
            if targets.get(priority):
                target = targets[priority]
                arc = self.player_ship.get_target_arc(target.hex_q, target.hex_r)
                target_arcs[priority] = arc
        
        # Display target legend
        legend_y = window_y + 75
        legend_x = window_x + 30
        
        legend_title = self.font_small.render("TARGETS:", True, LCARS_COLORS['light_blue'])
        self.screen.blit(legend_title, (legend_x, legend_y))
        legend_y += 24
        
        for priority in ['primary', 'secondary', 'tertiary']:
            if targets.get(priority):
                target = targets[priority]
                arc = target_arcs.get(priority, 'UNKNOWN')
                text = f"{priority.upper()}: {target.name} [{arc.upper()}]"
                surface = self.font_tiny.render(text, True, target_colors[priority])
                self.screen.blit(surface, (legend_x + 10, legend_y))
                legend_y += 18
        
        # Clear click areas for this frame
        self._weapon_click_areas = {}
        
        # Define weapon box dimensions
        box_width = (window_width - 60) // 2  # Two boxes side by side
        box_height = 380
        box_y = window_y + 180
        
        # Left box: PHASERS
        phaser_box_x = window_x + 20
        phaser_box_rect = pygame.Rect(phaser_box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_medium'], phaser_box_rect)
        pygame.draw.rect(self.screen, LCARS_COLORS['orange'], phaser_box_rect, 2)
        
        # Phaser title
        phaser_title = self.font_small.render("PHASER ARRAYS", True, LCARS_COLORS['orange'])
        phaser_title_rect = phaser_title.get_rect(centerx=phaser_box_x + box_width // 2, top=box_y + 8)
        self.screen.blit(phaser_title, phaser_title_rect)
        
        # Right box: TORPEDOES
        torpedo_box_x = phaser_box_x + box_width + 20
        torpedo_box_rect = pygame.Rect(torpedo_box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, LCARS_COLORS['bg_medium'], torpedo_box_rect)
        pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], torpedo_box_rect, 2)
        
        # Torpedo title
        torpedo_title = self.font_small.render("TORPEDO BAYS", True, LCARS_COLORS['light_blue'])
        torpedo_title_rect = torpedo_title.get_rect(centerx=torpedo_box_x + box_width // 2, top=box_y + 8)
        self.screen.blit(torpedo_title, torpedo_title_rect)
        
        # Scrollable area setup
        scroll_area_height = box_height - 45  # Leave room for title and padding
        content_start_y = box_y + 35
        
        # Draw phasers (with scrolling if needed)
        phaser_content_height = len(self.player_ship.weapon_arrays) * 24
        if phaser_content_height > scroll_area_height:
            # Need scrolling
            max_scroll = phaser_content_height - scroll_area_height
            self.weapon_assign_phaser_scroll = max(0, min(self.weapon_assign_phaser_scroll, max_scroll))
        else:
            self.weapon_assign_phaser_scroll = 0
        
        # Create clip rect for phaser scrolling
        phaser_clip_rect = pygame.Rect(phaser_box_x + 5, content_start_y, box_width - 10, scroll_area_height)
        
        phaser_y = content_start_y - self.weapon_assign_phaser_scroll
        for i, weapon in enumerate(self.player_ship.weapon_arrays):
            weapon_key = f'array_{i}'
            
            # Find which targets are in arc for this weapon
            valid_targets = []
            for priority in ['primary', 'secondary', 'tertiary']:
                if priority in target_arcs and target_arcs[priority] in weapon.firing_arcs:
                    valid_targets.append(priority)
            
            # Get assigned target (default to first valid, or primary if none)
            assigned = self.weapon_assignments.get(weapon_key, valid_targets[0] if valid_targets else 'primary')
            
            # Determine color and status
            ready = weapon.can_fire()
            in_arc = assigned in valid_targets
            
            if not in_arc:
                color = LCARS_COLORS['text_gray']
                status_text = "OUT OF ARC"
            elif not ready:
                color = LCARS_COLORS['alert_red']
                status_text = f"CD:{weapon.cooldown_remaining}"
            else:
                color = target_colors.get(assigned, LCARS_COLORS['green'])
                status_text = "READY"
            
            # Build text
            weapon_text = f"{weapon.weapon_type.upper()} Mk{weapon.mark}"
            target_text = f"→ {assigned.upper()}" if in_arc else "→ NO TARGET"
            
            # Only draw if in visible area
            if phaser_y >= content_start_y - 24 and phaser_y < content_start_y + scroll_area_height:
                # Draw with clipping
                old_clip = self.screen.get_clip()
                self.screen.set_clip(phaser_clip_rect)
                
                text1 = self.font_tiny.render(weapon_text, True, color)
                text2 = self.font_tiny.render(f"[{status_text}] {target_text}", True, color)
                self.screen.blit(text1, (phaser_box_x + 8, phaser_y))
                self.screen.blit(text2, (phaser_box_x + 8, phaser_y + 12))
                
                self.screen.set_clip(old_clip)
                
                # Store click area (only if weapon has valid targets)
                if valid_targets:
                    click_rect = pygame.Rect(phaser_box_x + 5, phaser_y, box_width - 10, 24)
                    # Only register if visible in scroll area
                    if click_rect.colliderect(phaser_clip_rect):
                        self._weapon_click_areas[weapon_key] = click_rect
            
            phaser_y += 24
        
        # Draw scroll indicator for phasers if needed
        if phaser_content_height > scroll_area_height:
            scroll_bar_height = max(20, (scroll_area_height / phaser_content_height) * scroll_area_height)
            scroll_bar_y = content_start_y + (self.weapon_assign_phaser_scroll / phaser_content_height) * scroll_area_height
            scroll_bar_rect = pygame.Rect(phaser_box_x + box_width - 8, scroll_bar_y, 4, scroll_bar_height)
            pygame.draw.rect(self.screen, LCARS_COLORS['orange'], scroll_bar_rect)
        
        # Draw torpedoes (with scrolling if needed)
        torpedo_content_height = len(self.player_ship.torpedo_bays) * 24
        if torpedo_content_height > scroll_area_height:
            max_scroll = torpedo_content_height - scroll_area_height
            self.weapon_assign_torpedo_scroll = max(0, min(self.weapon_assign_torpedo_scroll, max_scroll))
        else:
            self.weapon_assign_torpedo_scroll = 0
        
        # Create clip rect for torpedo scrolling
        torpedo_clip_rect = pygame.Rect(torpedo_box_x + 5, content_start_y, box_width - 10, scroll_area_height)
        
        torpedo_y = content_start_y - self.weapon_assign_torpedo_scroll
        for i, torpedo in enumerate(self.player_ship.torpedo_bays):
            weapon_key = f'torpedo_{i}'
            
            # Find which targets are in arc for this weapon
            valid_targets = []
            for priority in ['primary', 'secondary', 'tertiary']:
                if priority in target_arcs and target_arcs[priority] in torpedo.firing_arcs:
                    valid_targets.append(priority)
            
            # Get assigned target
            assigned = self.weapon_assignments.get(weapon_key, valid_targets[0] if valid_targets else 'primary')
            
            # Determine color and status
            ready = torpedo.can_fire()
            in_arc = assigned in valid_targets
            
            if not in_arc:
                color = LCARS_COLORS['text_gray']
                status_text = "OUT OF ARC"
            elif not ready:
                color = LCARS_COLORS['alert_red']
                status_text = f"CD:{torpedo.cooldown_remaining}"
            else:
                color = target_colors.get(assigned, LCARS_COLORS['green'])
                status_text = "READY"
            
            # Build text
            weapon_text = f"{torpedo.torpedo_type.upper()} Mk{torpedo.mark}"
            target_text = f"→ {assigned.upper()}" if in_arc else "→ NO TARGET"
            
            # Only draw if in visible area
            if torpedo_y >= content_start_y - 24 and torpedo_y < content_start_y + scroll_area_height:
                # Draw with clipping
                old_clip = self.screen.get_clip()
                self.screen.set_clip(torpedo_clip_rect)
                
                text1 = self.font_tiny.render(weapon_text, True, color)
                text2 = self.font_tiny.render(f"[{status_text}] {target_text}", True, color)
                self.screen.blit(text1, (torpedo_box_x + 8, torpedo_y))
                self.screen.blit(text2, (torpedo_box_x + 8, torpedo_y + 12))
                
                self.screen.set_clip(old_clip)
                
                # Store click area (only if weapon has valid targets)
                if valid_targets:
                    click_rect = pygame.Rect(torpedo_box_x + 5, torpedo_y, box_width - 10, 24)
                    if click_rect.colliderect(torpedo_clip_rect):
                        self._weapon_click_areas[weapon_key] = click_rect
            
            torpedo_y += 24
        
        # Draw scroll indicator for torpedoes if needed
        if torpedo_content_height > scroll_area_height:
            scroll_bar_height = max(20, (scroll_area_height / torpedo_content_height) * scroll_area_height)
            scroll_bar_y = content_start_y + (self.weapon_assign_torpedo_scroll / torpedo_content_height) * scroll_area_height
            scroll_bar_rect = pygame.Rect(torpedo_box_x + box_width - 8, scroll_bar_y, 4, scroll_bar_height)
            pygame.draw.rect(self.screen, LCARS_COLORS['light_blue'], scroll_bar_rect)
        
        # BIG BEAUTIFUL RED COMMIT BUTTON
        button_width = 300
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        button_y = window_y + window_height - 85
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Draw button with gradient effect (simulate depth)
        pygame.draw.rect(self.screen, LCARS_COLORS['alert_red'], button_rect)
        pygame.draw.rect(self.screen, LCARS_COLORS['orange'], button_rect, 4)
        
        # Inner highlight for 3D effect
        highlight_rect = button_rect.inflate(-8, -8)
        pygame.draw.line(self.screen, (255, 100, 100), 
                        (highlight_rect.left, highlight_rect.top),
                        (highlight_rect.right, highlight_rect.top), 2)
        pygame.draw.line(self.screen, (255, 100, 100),
                        (highlight_rect.left, highlight_rect.top),
                        (highlight_rect.left, highlight_rect.bottom), 2)
        
        # Button text
        button_text = self.font_large.render("COMMIT", True, LCARS_COLORS['text_white'])
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        # Store button rect for click detection
        self._weapon_commit_button = button_rect
        
        # Helper text above boxes
        helper_text = "CLICK WEAPON TO CYCLE TARGET | SCROLL TO NAVIGATE"
        helper = self.font_tiny.render(helper_text, True, LCARS_COLORS['text_gray'])
        helper_rect = helper.get_rect(center=(self.screen_width // 2, box_y - 15))
        self.screen.blit(helper, helper_rect)
