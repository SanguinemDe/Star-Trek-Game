"""Test AI range management behavior in various scenarios"""
import pygame
from game.ships.federation import create_constitution_class
from gui.hex_grid import HexGrid
from game.ship_ai import ShipAI, AIPersonality

pygame.init()

# Create mock ship and target
ship = create_constitution_class("Test Ship", "NCC-1701")
target = create_constitution_class("Target Ship", "NCC-1702")

# Create hex grid
hex_grid = HexGrid(hex_size=40, offset_x=400, offset_y=400)

# Test scenarios: (ship_distance, preferred_range, description)
test_scenarios = [
    (2, 6, "WAY TOO CLOSE (2 hexes, want 6)"),
    (4, 6, "Too close (4 hexes, want 6)"),
    (5, 6, "Slightly too close (5 hexes, want 6)"),
    (6, 6, "OPTIMAL RANGE (6 hexes, want 6)"),
    (7, 6, "Slightly too far (7 hexes, want 6)"),
    (9, 6, "Too far (9 hexes, want 6)"),
    (12, 6, "WAY TOO FAR (12 hexes, want 6)"),
]

print("\n" + "="*80)
print("AI RANGE MANAGEMENT TEST")
print("="*80)

for distance, preferred_range, description in test_scenarios:
    print(f"\n{'='*80}")
    print(f"SCENARIO: {description}")
    print(f"{'='*80}")
    
    # Position ships at specific distance
    ship.hex_q = 0
    ship.hex_r = 0
    ship.facing = 0  # Facing right
    ship.position = hex_grid.axial_to_pixel(ship.hex_q, ship.hex_r)
    ship.hull = ship.max_hull  # Full health
    
    target.hex_q = distance
    target.hex_r = 0
    target.facing = 3  # Facing left
    target.position = hex_grid.axial_to_pixel(target.hex_q, target.hex_r)
    
    # Create AI with specific preferred range
    ai = ShipAI(ship, hex_grid)
    ai.set_target(target)
    AIPersonality.apply_to_ai(ai, 'aggressive')
    ai.preferred_range = preferred_range  # Override after applying personality
    
    # Verify distance
    actual_distance = hex_grid.distance(ship.hex_q, ship.hex_r, target.hex_q, target.hex_r)
    range_diff = actual_distance - preferred_range
    
    print(f"Current distance: {actual_distance}")
    print(f"Preferred range: {preferred_range}")
    print(f"Range difference: {range_diff:+d}")
    
    # Get movement decision
    movement_points = 5
    moves = ai.decide_movement(movement_points)
    
    print(f"\nAI Decision with {movement_points} MP:")
    if len(moves) == 0:
        print("  ⚠️  NO MOVES (AI doing nothing!)")
    else:
        print(f"  Moves: {moves}")
        
        # Analyze moves
        forward_count = moves.count('forward')
        backward_count = moves.count('backward')
        turn_count = moves.count('turn_left') + moves.count('turn_right')
        
        print(f"  Forward: {forward_count}, Backward: {backward_count}, Turns: {turn_count}")
        
        # Check if behavior makes sense
        if range_diff < -1 and backward_count == 0:
            print("  [ERROR] Too close but not backing away!")
        elif range_diff < -1 and backward_count > 0:
            print(f"  [OK] CORRECT: Backing away {backward_count} hexes")
        elif range_diff > 1 and forward_count == 0:
            print("  [WARN] Too far but not closing in!")
        elif range_diff > 1 and forward_count > 0:
            print(f"  [OK] CORRECT: Closing in {forward_count} hexes")
        else:
            print("  [OK] At optimal range, tactical maneuvering")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
