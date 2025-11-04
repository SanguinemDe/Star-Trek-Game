"""
Star Trek: Federation Command
Main Game Entry Point

A tactical starship command simulator featuring:
- Character creation with multiple species and backgrounds
- Galaxy exploration with procedurally generated star systems
- Hex-based tactical combat with 8-phase turn structure
- Ship management with Mark I-XV equipment progression
- Crew management and development
- Mission system with dynamic objectives

Launch the GUI version of the game and navigate through menus
to create your captain and command your starship.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the GUI version of the game with error handling"""
    try:
        from gui_main import StarTrekGUI
        import pygame
        
        print("=" * 60)
        print("STAR TREK: FEDERATION COMMAND")
        print("=" * 60)
        print("\nLaunching GUI interface...")
        print("Press ESC or use menu options to navigate")
        print("=" * 60)
        
        app = StarTrekGUI()
        app.run()
        
    except ImportError as e:
        print("\n" + "=" * 60)
        print("ERROR: Missing dependencies!")
        print("=" * 60)
        print(f"\n{str(e)}\n")
        print("Please install required packages:")
        print("  pip install pygame")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        sys.exit(1)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR: Failed to launch game!")
        print("=" * 60)
        print(f"\n{str(e)}\n")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
