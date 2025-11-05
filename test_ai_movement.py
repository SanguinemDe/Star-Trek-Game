"""Quick test to diagnose AI movement issues"""

from game.ship_ai import ShipAI
from gui.hex_grid import HexGrid
from game.ships.federation import create_miranda_class

# Create test ships
ship = create_miranda_class('TestShip', 'NX-1234')
ship.hex_q = 0
ship.hex_r = 0
ship.facing = 0
ship.position = (400, 400)
ship.faction = 'player'

target = create_miranda_class('Target', 'NX-9999')
target.hex_q = 5
target.hex_r = 0
target.position = (600, 400)
target.faction = 'enemy'

# Create hex grid and AI
grid = HexGrid(40)
ai = ShipAI(ship, grid)
ai.set_target(target)

# Check attributes
print("=== ATTRIBUTE CHECK ===")
print(f"Ship has hex_q: {hasattr(ship, 'hex_q')} = {getattr(ship, 'hex_q', 'MISSING')}")
print(f"Ship has hex_r: {hasattr(ship, 'hex_r')} = {getattr(ship, 'hex_r', 'MISSING')}")
print(f"Ship has facing: {hasattr(ship, 'facing')} = {getattr(ship, 'facing', 'MISSING')}")
print(f"Ship has hull: {hasattr(ship, 'hull')} = {getattr(ship, 'hull', 'MISSING')}")
print(f"Ship has max_hull: {hasattr(ship, 'max_hull')} = {getattr(ship, 'max_hull', 'MISSING')}")
print(f"Ship has position: {hasattr(ship, 'position')} = {getattr(ship, 'position', 'MISSING')}")
print(f"Target has hex_q: {hasattr(target, 'hex_q')} = {getattr(target, 'hex_q', 'MISSING')}")
print(f"Target has hex_r: {hasattr(target, 'hex_r')} = {getattr(target, 'hex_r', 'MISSING')}")
print(f"Target has position: {hasattr(target, 'position')} = {getattr(target, 'position', 'MISSING')}")

print("\n=== TACTICAL SITUATION ===")
distance = grid.distance(ship.hex_q, ship.hex_r, target.hex_q, target.hex_r)
print(f"Distance: {distance} hexes")
print(f"Preferred range: {ai.preferred_range} hexes")
print(f"Range diff: {distance - ai.preferred_range}")

target_arc = ship.get_target_arc(target.hex_q, target.hex_r)
print(f"Target arc: {target_arc}")

weapons_in_arc = ai._check_weapons_in_arc(target_arc)
print(f"Weapons in arc: {weapons_in_arc}")

print(f"Hull: {ship.hull}/{ship.max_hull} = {ship.hull/ship.max_hull:.1%}")

print("\n=== MOVEMENT DECISION ===")
print(f"Calling decide_movement(5)...")
try:
    moves = ai.decide_movement(5)
    print(f"Result: {moves}")
    print(f"Move count: {len(moves)}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
