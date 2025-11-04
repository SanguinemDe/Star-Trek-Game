"""
LCARS Color Scheme and Constants
Star Trek LCARS (Library Computer Access/Retrieval System) styling
Supports multiple theme variants
"""

# ═══════════════════════════════════════════════════════════════════
# LCARS V1 - Classic Theme (TNG Era)
# ═══════════════════════════════════════════════════════════════════
LCARS_V1_COLORS = {
    # Primary colors
    'orange': (255, 153, 0),      # LCARS Orange (main highlight)
    'red': (204, 102, 102),       # LCARS Red (alerts)
    'pink': (204, 153, 204),      # LCARS Pink/Mauve
    'purple': (153, 102, 204),    # LCARS Purple
    'blue': (153, 153, 204),      # LCARS Blue
    'light_blue': (153, 204, 255),# LCARS Light Blue
    'peach': (255, 204, 153),     # LCARS Peach
    
    # Background colors
    'black': (0, 0, 0),
    'bg_dark': (20, 20, 30),      # Dark background
    'bg_medium': (40, 40, 50),    # Medium background
    
    # Text colors
    'text_white': (255, 255, 255),
    'text_gray': (180, 180, 200),
    'text_dim': (120, 120, 140),
    
    # Status colors
    'green': (153, 204, 102),     # Success/Active
    'yellow': (255, 255, 102),    # Warning
    'alert_red': (255, 51, 51),   # Critical Alert
}

# ═══════════════════════════════════════════════════════════════════
# LCARS V2 - Modern Theme (Discovery/Picard Era)
# Inspired by modern Trek interfaces with cooler tones and sharper design
# ═══════════════════════════════════════════════════════════════════
LCARS_V2_COLORS = {
    # Primary colors - cooler, more cyan-focused palette
    'orange': (255, 138, 51),     # Warmer orange/amber
    'red': (255, 71, 87),         # Brighter, more saturated red
    'pink': (180, 140, 200),      # Cooler purple-pink
    'purple': (120, 100, 220),    # Deeper, cooler purple
    'blue': (100, 149, 237),      # Cornflower blue (more vivid)
    'light_blue': (102, 204, 255),# Bright cyan-blue
    'peach': (255, 160, 100),     # Warm amber
    
    # Background colors - darker, more modern
    'black': (0, 0, 0),
    'bg_dark': (10, 15, 25),      # Very dark blue-black
    'bg_medium': (25, 35, 50),    # Dark blue-gray
    
    # Text colors - brighter for contrast
    'text_white': (240, 248, 255),# Slightly blue-white
    'text_gray': (150, 170, 200), # Blue-tinted gray
    'text_dim': (100, 115, 140),  # Dimmer blue-gray
    
    # Status colors
    'green': (100, 230, 150),     # Bright mint green
    'yellow': (255, 220, 80),     # Bright golden yellow
    'alert_red': (255, 60, 60),   # Vivid red
}

# ═══════════════════════════════════════════════════════════════════
# Theme Management
# ═══════════════════════════════════════════════════════════════════
AVAILABLE_THEMES = ['lcars_v1', 'lcars_v2']
_current_theme = 'lcars_v1'

# Active color palette (defaults to V1)
LCARS_COLORS = LCARS_V1_COLORS.copy()

def get_current_theme():
    """Get the name of the current theme"""
    return _current_theme

def set_theme(theme_name):
    """
    Change the active LCARS theme
    
    Args:
        theme_name: 'lcars_v1' or 'lcars_v2'
    """
    global _current_theme, LCARS_COLORS
    
    if theme_name not in AVAILABLE_THEMES:
        print(f"Warning: Unknown theme '{theme_name}', using lcars_v1")
        theme_name = 'lcars_v1'
    
    _current_theme = theme_name
    
    if theme_name == 'lcars_v1':
        LCARS_COLORS.update(LCARS_V1_COLORS)
    elif theme_name == 'lcars_v2':
        LCARS_COLORS.update(LCARS_V2_COLORS)
    
    print(f"LCARS theme set to: {theme_name.upper()}")

def get_accent_color():
    """
    Get the primary accent color for the current theme
    Returns the most appropriate highlight color for UI elements
    """
    theme = get_current_theme()
    if theme == 'lcars_v2':
        return LCARS_COLORS['light_blue']  # Cool cyan for V2
    return LCARS_COLORS['orange']  # Warm orange for V1

def get_warning_color():
    """Get the warning/medium alert color for the current theme"""
    theme = get_current_theme()
    if theme == 'lcars_v2':
        return LCARS_COLORS['purple']  # Purple for V2
    return LCARS_COLORS['orange']  # Orange for V1

def load_theme_preference():
    """Load saved theme preference from settings"""
    import json
    import os
    
    try:
        if os.path.exists('settings/options.json'):
            with open('settings/options.json', 'r') as f:
                settings = json.load(f)
                theme = settings.get('theme', 'lcars_v1')
                set_theme(theme)
                return theme
    except Exception as e:
        print(f"Could not load theme preference: {e}")
    
    return 'lcars_v1'

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Font sizes
FONT_LARGE = 48
FONT_MEDIUM = 32
FONT_SMALL = 24
FONT_TINY = 18

# UI Element dimensions
BUTTON_HEIGHT = 50
BUTTON_CORNER_RADIUS = 25
PANEL_CORNER_RADIUS = 20

# ═══════════════════════════════════════════════════════════════════
# Font Management
# ═══════════════════════════════════════════════════════════════════
def get_font(size, bold=False):
    """
    Get a sci-fi themed font for LCARS interface
    Falls back to system fonts if custom font not available
    
    Args:
        size: Font size in pixels
        bold: Whether to use bold variant
    
    Returns:
        pygame.font.Font object
    """
    import pygame
    import os
    
    # Try custom sci-fi fonts first
    font_paths = [
        'assets/fonts/Antonio-Bold.ttf',
        'assets/fonts/Antonio-Regular.ttf',
        'assets/fonts/Orbitron-Bold.ttf',
        'assets/fonts/Orbitron-Regular.ttf',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                pass
    
    # Fallback to system fonts with sci-fi feel
    sci_fi_fonts = [
        'Consolas',      # Monospace, clean
        'Courier New',   # Monospace, readable
        'Arial Narrow',  # Condensed, modern
        'Impact',        # Bold, geometric
        'Arial',         # Clean fallback
    ]
    
    for font_name in sci_fi_fonts:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            if font:
                return font
        except:
            pass
    
    # Ultimate fallback
    return pygame.font.Font(None, size)
