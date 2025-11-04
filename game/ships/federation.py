"""
Federation Starship Catalogue
All Federation starship classes and their specifications
Organized by Rank (0-8)
"""

from game.advanced_ship import AdvancedShip, WeaponArray, TorpedoBay


# ═══════════════════════════════════════════════════════════════════
# FEDERATION SHIP TEMPLATES
# 64 ships across 9 ranks (0-8)
# ═══════════════════════════════════════════════════════════════════

def create_miranda_class(name, registry):
    """
    Create a Miranda-class frigate
    
    Starter Equipment:
    - Mk IV Phasers (15+15=30 damage)
    - Mk IV Photon Torpedoes (80+30=110 damage)
    - Mk II Shields
    - Mk II Impulse Engines
    - Mk II Warp Core
    
    upgrade_space of 80 is AVAILABLE space after starter equipment is installed
    """
    ship = AdvancedShip(name, registry, "Miranda", "Frigate", 2270)
    ship.reputation_cost = 5000
    ship.minimum_rank = 1
    ship.size = "Medium"
    ship.cargo_space = 150
    ship.upgrade_space = 80  # Available space for upgrades
    
    # Navigation
    ship.sensor_range = 6
    ship.turn_speed = 1
    ship.impulse_speed = 6
    ship.warp_speed = 7.0
    
    # Defenses
    ship.max_hull = 800
    ship.hull = 800
    ship.armor = 40
    ship.shields = {'fore': 400, 'aft': 300, 'port': 350, 'starboard': 350}
    ship.max_shields = ship.shields.copy()
    
    # Starter Weapons (Mk IV equipment)
    # Mk IV Phasers: 15 base + (4-1)*5 = 30 damage
    # Mk IV Photon: 80 base + (4-1)*10 = 110 damage
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=4, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=4, firing_arcs=['fore'], max_torpedoes=50, upgrade_space_cost=10)
    ]
    
    # Crew
    ship.max_crew = 200
    ship.crew_count = 200
    
    return ship


def create_galaxy_class(name, registry):
    """
    Create a Galaxy-class heavy cruiser
    
    Starter Equipment:
    - Mk XII Phasers (15+55=70 damage)
    - Mk XII Photon Torpedoes (80+110=190 damage)
    - Mk X Shields
    - Mk X Impulse Engines
    - Mk XII Warp Core
    
    upgrade_space of 200 is AVAILABLE space after starter equipment is installed
    """
    ship = AdvancedShip(name, registry, "Galaxy", "Heavy Cruiser", 2363)
    ship.reputation_cost = 50000
    ship.minimum_rank = 8
    ship.size = "Very Large"
    ship.cargo_space = 500
    ship.upgrade_space = 200  # Available space for upgrades
    
    # Navigation
    ship.sensor_range = 10
    ship.turn_speed = 3
    ship.impulse_speed = 4
    ship.warp_speed = 9.6
    
    # Defenses
    ship.max_hull = 5000
    ship.hull = 5000
    ship.armor = 100
    ship.shields = {'fore': 2000, 'aft': 1500, 'port': 1800, 'starboard': 1800}
    ship.max_shields = ship.shields.copy()
    
    # Power
    ship.warp_core_max_power = 500
    ship.power_distribution = {
        'engines': 166,
        'shields': 167,
        'weapons': 167
    }
    
    # Starter Weapons (Mk XII equipment)
    # Mk XII Phasers: 15 base + (12-1)*5 = 70 damage
    # Mk XII Photon: 80 base + (12-1)*10 = 190 damage
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=12, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=12, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=12, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=12, firing_arcs=['fore'], max_torpedoes=200, upgrade_space_cost=10),
        TorpedoBay('photon', mark=12, firing_arcs=['aft'], max_torpedoes=200, upgrade_space_cost=10)
    ]
    
    # Crew
    ship.max_crew = 1000
    ship.crew_count = 1000
    
    return ship


# ═══════════════════════════════════════════════════════════════════
# COMPLETE SHIP CATALOGUE - ALL FEDERATION SHIPS
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# RANK 0: LIEUTENANT COMMANDER - Starting Ships
# ═══════════════════════════════════════════════════════════════════

def create_daedalus_class(name, registry):
    """Daedalus-class Survey Vessel (22nd Century)"""
    ship = AdvancedShip(name, registry, "Daedalus", "Survey Vessel", 2160)
    ship.reputation_cost = 0
    ship.minimum_rank = 0
    ship.size = "Medium"
    ship.cargo_space = 100
    ship.upgrade_space = 60
    
    ship.sensor_range = 6
    ship.turn_speed = 2
    ship.impulse_speed = 4
    ship.warp_speed = 4.0
    
    ship.max_hull = 600
    ship.hull = 600
    ship.armor = 20
    ship.shields = {'fore': 200, 'aft': 200, 'port': 200, 'starboard': 200}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 210
    ship.power_distribution = {'engines': 70, 'shields': 70, 'weapons': 70}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=1, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=1, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('spatial', mark=-2, firing_arcs=['fore'], max_torpedoes=20, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_oberth_class(name, registry):
    """Oberth-class Science Vessel"""
    ship = AdvancedShip(name, registry, "Oberth", "Science Vessel", 2270)
    ship.reputation_cost = 100
    ship.minimum_rank = 0
    ship.size = "Small"
    ship.cargo_space = 50
    ship.upgrade_space = 50
    
    ship.sensor_range = 10
    ship.turn_speed = 1
    ship.impulse_speed = 5
    ship.warp_speed = 7.0
    
    ship.max_hull = 400
    ship.hull = 400
    ship.armor = 15
    ship.shields = {'fore': 250, 'aft': 200, 'port': 200, 'starboard': 200}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 240
    ship.power_distribution = {'engines': 80, 'shields': 80, 'weapons': 80}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=2, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = []  # Science vessel, minimal weapons
    
    ship.max_crew = 80
    ship.crew_count = 80
    return ship


def create_sydney_class(name, registry):
    """Sydney-class Transport"""
    ship = AdvancedShip(name, registry, "Sydney", "Transport", 2270)
    ship.reputation_cost = 50
    ship.minimum_rank = 0
    ship.size = "Medium"
    ship.cargo_space = 300
    ship.upgrade_space = 65
    
    ship.sensor_range = 5
    ship.turn_speed = 2
    ship.impulse_speed = 5
    ship.warp_speed = 7.5
    
    ship.max_hull = 550
    ship.hull = 550
    ship.armor = 25
    ship.shields = {'fore': 280, 'aft': 250, 'port': 250, 'starboard': 250}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 255
    ship.power_distribution = {'engines': 85, 'shields': 85, 'weapons': 85}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=2, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=1, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = []
    
    ship.max_crew = 150
    ship.crew_count = 150
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 1: LIEUTENANT COMMANDER - Early Career
# ═══════════════════════════════════════════════════════════════════

def create_ptolemy_class(name, registry):
    """Ptolemy-class Tug/Transport"""
    ship = AdvancedShip(name, registry, "Ptolemy", "Tug/Transport", 2270)
    ship.reputation_cost = 250
    ship.minimum_rank = 1
    ship.size = "Medium"
    ship.cargo_space = 400
    ship.upgrade_space = 70
    
    ship.sensor_range = 5
    ship.turn_speed = 3
    ship.impulse_speed = 4
    ship.warp_speed = 7.0
    
    ship.max_hull = 650
    ship.hull = 650
    ship.armor = 20
    ship.shields = {'fore': 300, 'aft': 280, 'port': 280, 'starboard': 280}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 330
    ship.power_distribution = {'engines': 110, 'shields': 110, 'weapons': 110}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=2, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = []
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_soyuz_class(name, registry):
    """Soyuz-class Frigate (Miranda variant)"""
    ship = AdvancedShip(name, registry, "Soyuz", "Frigate", 2270)
    ship.reputation_cost = 200
    ship.minimum_rank = 1
    ship.size = "Medium"
    ship.cargo_space = 140
    ship.upgrade_space = 75
    
    ship.sensor_range = 7
    ship.turn_speed = 1
    ship.impulse_speed = 6
    ship.warp_speed = 8.0
    
    ship.max_hull = 750
    ship.hull = 750
    ship.armor = 35
    ship.shields = {'fore': 380, 'aft': 320, 'port': 340, 'starboard': 340}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 285
    ship.power_distribution = {'engines': 95, 'shields': 95, 'weapons': 95}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=3, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=3, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=2, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=3, firing_arcs=['fore'], max_torpedoes=50, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 220
    ship.crew_count = 220
    return ship


def create_constitution_class(name, registry):
    """Constitution-class Heavy Cruiser (Original)"""
    ship = AdvancedShip(name, registry, "Constitution", "Heavy Cruiser", 2245)
    ship.reputation_cost = 300
    ship.minimum_rank = 1
    ship.size = "Large"
    ship.cargo_space = 200
    ship.upgrade_space = 100
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 8.0
    
    ship.max_hull = 1200
    ship.hull = 1200
    ship.armor = 45
    ship.shields = {'fore': 500, 'aft': 400, 'port': 450, 'starboard': 450}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 360
    ship.power_distribution = {'engines': 120, 'shields': 120, 'weapons': 120}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=5, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=5, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10),
        TorpedoBay('photon', mark=3, firing_arcs=['aft'], max_torpedoes=50, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 430
    ship.crew_count = 430
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 2: COMMANDER - Exploration Era
# ═══════════════════════════════════════════════════════════════════

def create_hermes_class(name, registry):
    """Hermes-class Scout"""
    ship = AdvancedShip(name, registry, "Hermes", "Scout", 2250)
    ship.reputation_cost = 350
    ship.minimum_rank = 2
    ship.size = "Medium"
    ship.cargo_space = 100
    ship.upgrade_space = 70
    
    ship.sensor_range = 9
    ship.turn_speed = 0
    ship.impulse_speed = 8
    ship.warp_speed = 8.0
    
    ship.max_hull = 600
    ship.hull = 600
    ship.armor = 25
    ship.shields = {'fore': 340, 'aft': 300, 'port': 320, 'starboard': 320}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 270
    ship.power_distribution = {'engines': 90, 'shields': 90, 'weapons': 90}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=3, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=2, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=1, firing_arcs=['fore'], max_torpedoes=40, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 220
    ship.crew_count = 220
    return ship


def create_saladin_class(name, registry):
    """Saladin-class Destroyer"""
    ship = AdvancedShip(name, registry, "Saladin", "Destroyer", 2250)
    ship.reputation_cost = 400
    ship.minimum_rank = 2
    ship.size = "Medium"
    ship.cargo_space = 110
    ship.upgrade_space = 80
    
    ship.sensor_range = 7
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 8.0
    
    ship.max_hull = 850
    ship.hull = 850
    ship.armor = 45
    ship.shields = {'fore': 420, 'aft': 360, 'port': 390, 'starboard': 390}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=4, firing_arcs=['fore'], max_torpedoes=60, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_constellation_class(name, registry):
    """Constellation-class Star Cruiser"""
    ship = AdvancedShip(name, registry, "Constellation", "Star Cruiser", 2270)
    ship.reputation_cost = 500
    ship.minimum_rank = 2
    ship.size = "Large"
    ship.cargo_space = 220
    ship.upgrade_space = 110
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 8.5
    
    ship.max_hull = 1300
    ship.hull = 1300
    ship.armor = 50
    ship.shields = {'fore': 520, 'aft': 420, 'port': 470, 'starboard': 470}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 375
    ship.power_distribution = {'engines': 125, 'shields': 125, 'weapons': 125}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=5, firing_arcs=['fore'], max_torpedoes=80, upgrade_space_cost=10),
        TorpedoBay('photon', mark=3, firing_arcs=['aft'], max_torpedoes=60, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 535
    ship.crew_count = 535
    return ship


def create_antares_class(name, registry):
    """Antares-class Freighter"""
    ship = AdvancedShip(name, registry, "Antares", "Freighter", 2350)
    ship.reputation_cost = 600
    ship.minimum_rank = 2
    ship.size = "Large"
    ship.cargo_space = 800
    ship.upgrade_space = 70
    
    ship.sensor_range = 6
    ship.turn_speed = 3
    ship.impulse_speed = 4
    ship.warp_speed = 8.0
    
    ship.max_hull = 900
    ship.hull = 900
    ship.armor = 40
    ship.shields = {'fore': 350, 'aft': 300, 'port': 320, 'starboard': 320}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=2, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=2, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = []
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 3: COMMANDER - TNG Era
# ═══════════════════════════════════════════════════════════════════

def create_constitution_refit_class(name, registry):
    """Constitution Refit-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Constitution Refit", "Heavy Cruiser", 2271)
    ship.reputation_cost = 600
    ship.minimum_rank = 3
    ship.size = "Large"
    ship.cargo_space = 210
    ship.upgrade_space = 115
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 8.5
    
    ship.max_hull = 1400
    ship.hull = 1400
    ship.armor = 65
    ship.shields = {'fore': 550, 'aft': 440, 'port': 495, 'starboard': 495}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 390
    ship.power_distribution = {'engines': 130, 'shields': 130, 'weapons': 130}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=5, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=120, upgrade_space_cost=10),
        TorpedoBay('photon', mark=5, firing_arcs=['aft'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 430
    ship.crew_count = 430
    return ship


def create_excelsior_class(name, registry):
    """Excelsior-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Excelsior", "Heavy Cruiser", 2285)
    ship.reputation_cost = 800
    ship.minimum_rank = 3
    ship.size = "Large"
    ship.cargo_space = 280
    ship.upgrade_space = 125
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.0
    
    ship.max_hull = 1500
    ship.hull = 1500
    ship.armor = 70
    ship.shields = {'fore': 600, 'aft': 480, 'port': 540, 'starboard': 540}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10),
        TorpedoBay('photon', mark=5, firing_arcs=['aft'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 750
    ship.crew_count = 750
    return ship


def create_ambassador_class(name, registry):
    """Ambassador-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Ambassador", "Heavy Cruiser", 2340)
    ship.reputation_cost = 1000
    ship.minimum_rank = 3
    ship.size = "Large"
    ship.cargo_space = 300
    ship.upgrade_space = 140
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.3
    
    ship.max_hull = 1600
    ship.hull = 1600
    ship.armor = 75
    ship.shields = {'fore': 650, 'aft': 520, 'port': 585, 'starboard': 585}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 450
    ship.power_distribution = {'engines': 150, 'shields': 150, 'weapons': 150}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=120, upgrade_space_cost=10),
        TorpedoBay('photon', mark=6, firing_arcs=['aft'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 700
    ship.crew_count = 700
    return ship


def create_springfield_class(name, registry):
    """Springfield-class Frigate"""
    ship = AdvancedShip(name, registry, "Springfield", "Frigate", 2350)
    ship.reputation_cost = 850
    ship.minimum_rank = 3
    ship.size = "Medium"
    ship.cargo_space = 120
    ship.upgrade_space = 90
    
    ship.sensor_range = 7
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.2
    
    ship.max_hull = 950
    ship.hull = 950
    ship.armor = 50
    ship.shields = {'fore': 460, 'aft': 400, 'port': 430, 'starboard': 430}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 315
    ship.power_distribution = {'engines': 105, 'shields': 105, 'weapons': 105}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 150
    ship.crew_count = 150
    return ship


def create_cheyenne_class(name, registry):
    """Cheyenne-class Light Cruiser"""
    ship = AdvancedShip(name, registry, "Cheyenne", "Light Cruiser", 2350)
    ship.reputation_cost = 900
    ship.minimum_rank = 3
    ship.size = "Medium"
    ship.cargo_space = 160
    ship.upgrade_space = 100
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.3
    
    ship.max_hull = 1100
    ship.hull = 1100
    ship.armor = 55
    ship.shields = {'fore': 520, 'aft': 460, 'port': 490, 'starboard': 490}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 360
    ship.power_distribution = {'engines': 120, 'shields': 120, 'weapons': 120}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 300
    ship.crew_count = 300
    return ship


def create_challenger_class(name, registry):
    """Challenger-class Cruiser"""
    ship = AdvancedShip(name, registry, "Challenger", "Cruiser", 2350)
    ship.reputation_cost = 950
    ship.minimum_rank = 3
    ship.size = "Medium"
    ship.cargo_space = 170
    ship.upgrade_space = 105
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.3
    
    ship.max_hull = 1150
    ship.hull = 1150
    ship.armor = 55
    ship.shields = {'fore': 540, 'aft': 460, 'port': 500, 'starboard': 500}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 375
    ship.power_distribution = {'engines': 125, 'shields': 125, 'weapons': 125}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 350
    ship.crew_count = 350
    return ship


def create_new_orleans_class(name, registry):
    """New Orleans-class Frigate"""
    ship = AdvancedShip(name, registry, "New Orleans", "Frigate", 2350)
    ship.reputation_cost = 920
    ship.minimum_rank = 3
    ship.size = "Medium"
    ship.cargo_space = 150
    ship.upgrade_space = 95
    
    ship.sensor_range = 9
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.3
    
    ship.max_hull = 1050
    ship.hull = 1050
    ship.armor = 52
    ship.shields = {'fore': 500, 'aft': 440, 'port': 470, 'starboard': 470}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 345
    ship.power_distribution = {'engines': 115, 'shields': 115, 'weapons': 115}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 330
    ship.crew_count = 330
    return ship


def create_freedom_class(name, registry):
    """Freedom-class Escort"""
    ship = AdvancedShip(name, registry, "Freedom", "Escort", 2350)
    ship.reputation_cost = 750
    ship.minimum_rank = 3
    ship.size = "Small"
    ship.cargo_space = 80
    ship.upgrade_space = 85
    
    ship.sensor_range = 7
    ship.turn_speed = 0
    ship.impulse_speed = 8
    ship.warp_speed = 9.2
    
    ship.max_hull = 800
    ship.hull = 800
    ship.armor = 55
    ship.shields = {'fore': 420, 'aft': 380, 'port': 400, 'starboard': 400}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=70, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 100
    ship.crew_count = 100
    return ship


def create_nova_class(name, registry):
    """Nova-class Science Vessel"""
    ship = AdvancedShip(name, registry, "Nova", "Science Vessel", 2368)
    ship.reputation_cost = 900
    ship.minimum_rank = 3
    ship.size = "Small"
    ship.cargo_space = 60
    ship.upgrade_space = 70
    
    ship.sensor_range = 11
    ship.turn_speed = 1
    ship.impulse_speed = 6
    ship.warp_speed = 9.0
    
    ship.max_hull = 700
    ship.hull = 700
    ship.armor = 30
    ship.shields = {'fore': 380, 'aft': 340, 'port': 360, 'starboard': 360}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=4, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=3, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=3, firing_arcs=['fore'], max_torpedoes=50, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 80
    ship.crew_count = 80
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 4: CAPTAIN - Dominion War Era
# ═══════════════════════════════════════════════════════════════════

def create_niagara_class(name, registry):
    """Niagara-class Fast Cruiser"""
    ship = AdvancedShip(name, registry, "Niagara", "Fast Cruiser", 2350)
    ship.reputation_cost = 1100
    ship.minimum_rank = 4
    ship.size = "Large"
    ship.cargo_space = 190
    ship.upgrade_space = 115
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.4
    
    ship.max_hull = 1250
    ship.hull = 1250
    ship.armor = 60
    ship.shields = {'fore': 560, 'aft': 480, 'port': 520, 'starboard': 520}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 390
    ship.power_distribution = {'engines': 130, 'shields': 130, 'weapons': 130}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=110, upgrade_space_cost=10),
        TorpedoBay('photon', mark=6, firing_arcs=['aft'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 400
    ship.crew_count = 400
    return ship


def create_olympic_class(name, registry):
    """Olympic-class Medical Ship"""
    ship = AdvancedShip(name, registry, "Olympic", "Medical Ship", 2360)
    ship.reputation_cost = 1000
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 80
    ship.upgrade_space = 100
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.3
    
    ship.max_hull = 1000
    ship.hull = 1000
    ship.armor = 48
    ship.shields = {'fore': 480, 'aft': 400, 'port': 440, 'starboard': 440}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 360
    ship.power_distribution = {'engines': 120, 'shields': 120, 'weapons': 120}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=1, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=1, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = []  # Medical ship, minimal weapons
    
    # Bonus: Enhanced sick bay system
    ship.systems['sick_bay'] = 150  # 150% effectiveness
    
    ship.max_crew = 350
    ship.crew_count = 350
    return ship


def create_yeager_class(name, registry):
    """Yeager-class Light Cruiser"""
    ship = AdvancedShip(name, registry, "Yeager", "Light Cruiser", 2370)
    ship.reputation_cost = 1100
    ship.minimum_rank = 4
    ship.size = "Small"
    ship.cargo_space = 90
    ship.upgrade_space = 90
    
    ship.sensor_range = 8
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.2
    
    ship.max_hull = 900
    ship.hull = 900
    ship.armor = 50
    ship.shields = {'fore': 440, 'aft': 380, 'port': 410, 'starboard': 410}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 315
    ship.power_distribution = {'engines': 105, 'shields': 105, 'weapons': 105}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 175
    ship.crew_count = 175
    return ship


def create_saber_class(name, registry):
    """Saber-class Light Escort"""
    ship = AdvancedShip(name, registry, "Saber", "Light Escort", 2370)
    ship.reputation_cost = 1200
    ship.minimum_rank = 4
    ship.size = "Small"
    ship.cargo_space = 50
    ship.upgrade_space = 80
    
    ship.sensor_range = 7
    ship.turn_speed = 0
    ship.impulse_speed = 8
    ship.warp_speed = 9.2
    
    ship.max_hull = 850
    ship.hull = 850
    ship.armor = 58
    ship.shields = {'fore': 440, 'aft': 360, 'port': 400, 'starboard': 400}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 40
    ship.crew_count = 40
    return ship


def create_bradbury_class(name, registry):
    """Bradbury-class Survey Ship"""
    ship = AdvancedShip(name, registry, "Bradbury", "Survey Ship", 2360)
    ship.reputation_cost = 1200
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 130
    ship.upgrade_space = 95
    
    ship.sensor_range = 11
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.2
    
    ship.max_hull = 950
    ship.hull = 950
    ship.armor = 35
    ship.shields = {'fore': 460, 'aft': 380, 'port': 420, 'starboard': 420}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 330
    ship.power_distribution = {'engines': 110, 'shields': 110, 'weapons': 110}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=4, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=4, firing_arcs=['fore'], max_torpedoes=70, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_renaissance_class(name, registry):
    """Renaissance-class Cruiser"""
    ship = AdvancedShip(name, registry, "Renaissance", "Cruiser", 2360)
    ship.reputation_cost = 1300
    ship.minimum_rank = 4
    ship.size = "Large"
    ship.cargo_space = 200
    ship.upgrade_space = 120
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.4
    
    ship.max_hull = 1300
    ship.hull = 1300
    ship.armor = 62
    ship.shields = {'fore': 600, 'aft': 500, 'port': 550, 'starboard': 550}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 405
    ship.power_distribution = {'engines': 135, 'shields': 135, 'weapons': 135}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=120, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 420
    ship.crew_count = 420
    return ship


def create_steamrunner_class(name, registry):
    """Steamrunner-class Frigate"""
    ship = AdvancedShip(name, registry, "Steamrunner", "Frigate", 2370)
    ship.reputation_cost = 1300
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 120
    ship.upgrade_space = 100
    
    ship.sensor_range = 8
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.3
    
    ship.max_hull = 1050
    ship.hull = 1050
    ship.armor = 52
    ship.shields = {'fore': 500, 'aft': 420, 'port': 460, 'starboard': 460}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 330
    ship.power_distribution = {'engines': 110, 'shields': 110, 'weapons': 110}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10),
        TorpedoBay('photon', mark=6, firing_arcs=['aft'], max_torpedoes=80, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_norway_class(name, registry):
    """Norway-class Frigate"""
    ship = AdvancedShip(name, registry, "Norway", "Frigate", 2370)
    ship.reputation_cost = 1350
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 130
    ship.upgrade_space = 105
    
    ship.sensor_range = 8
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.3
    
    ship.max_hull = 1100
    ship.hull = 1100
    ship.armor = 54
    ship.shields = {'fore': 520, 'aft': 440, 'port': 480, 'starboard': 480}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 345
    ship.power_distribution = {'engines': 115, 'shields': 115, 'weapons': 115}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=110, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 190
    ship.crew_count = 190
    return ship


def create_nebula_class(name, registry):
    """Nebula-class Science Cruiser"""
    ship = AdvancedShip(name, registry, "Nebula", "Science Cruiser", 2360)
    ship.reputation_cost = 1400
    ship.minimum_rank = 4
    ship.size = "Large"
    ship.cargo_space = 280
    ship.upgrade_space = 150
    
    ship.sensor_range = 12
    ship.turn_speed = 3
    ship.impulse_speed = 5
    ship.warp_speed = 9.5
    
    ship.max_hull = 1800
    ship.hull = 1800
    ship.armor = 60
    ship.shields = {'fore': 700, 'aft': 560, 'port': 630, 'starboard': 630}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 480
    ship.power_distribution = {'engines': 160, 'shields': 160, 'weapons': 160}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=7, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['fore'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=150, upgrade_space_cost=10),
        TorpedoBay('photon', mark=6, firing_arcs=['aft'], max_torpedoes=120, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 750
    ship.crew_count = 750
    return ship


def create_centaur_class(name, registry):
    """Centaur-class Destroyer"""
    ship = AdvancedShip(name, registry, "Centaur", "Destroyer", 2370)
    ship.reputation_cost = 1400
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 140
    ship.upgrade_space = 100
    
    ship.sensor_range = 8
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.3
    
    ship.max_hull = 1050
    ship.hull = 1050
    ship.armor = 63
    ship.shields = {'fore': 500, 'aft': 420, 'port': 460, 'starboard': 460}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 345
    ship.power_distribution = {'engines': 115, 'shields': 115, 'weapons': 115}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 250
    ship.crew_count = 250
    return ship


def create_intrepid_class(name, registry):
    """Intrepid-class Light Explorer"""
    ship = AdvancedShip(name, registry, "Intrepid", "Light Explorer", 2370)
    ship.reputation_cost = 1500
    ship.minimum_rank = 4
    ship.size = "Medium"
    ship.cargo_space = 110
    ship.upgrade_space = 105
    
    ship.sensor_range = 10
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.975
    
    ship.max_hull = 1000
    ship.hull = 1000
    ship.armor = 48
    ship.shields = {'fore': 480, 'aft': 400, 'port': 440, 'starboard': 440}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 360
    ship.power_distribution = {'engines': 120, 'shields': 120, 'weapons': 120}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=5, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=4, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=5, firing_arcs=['fore'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 150
    ship.crew_count = 150
    return ship


def create_akira_class(name, registry):
    """Akira-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Akira", "Heavy Cruiser", 2370)
    ship.reputation_cost = 1700
    ship.minimum_rank = 5
    ship.size = "Large"
    ship.cargo_space = 200
    ship.upgrade_space = 140
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.4
    
    ship.max_hull = 1400
    ship.hull = 1400
    ship.armor = 68
    ship.shields = {'fore': 620, 'aft': 520, 'port': 570, 'starboard': 570}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=11, firing_arcs=['fore'], max_torpedoes=200, upgrade_space_cost=10),
        TorpedoBay('photon', mark=9, firing_arcs=['aft'], max_torpedoes=150, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 500
    ship.crew_count = 500
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 5: FLEET CAPTAIN - Advanced Ships
# ═══════════════════════════════════════════════════════════════════

def create_curry_class(name, registry):
    """Curry-class Cruiser"""
    ship = AdvancedShip(name, registry, "Curry", "Cruiser", 2370)
    ship.reputation_cost = 1500
    ship.minimum_rank = 5
    ship.size = "Large"
    ship.cargo_space = 180
    ship.upgrade_space = 115
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.3
    
    ship.max_hull = 1200
    ship.hull = 1200
    ship.armor = 58
    ship.shields = {'fore': 560, 'aft': 460, 'port': 510, 'starboard': 510}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 375
    ship.power_distribution = {'engines': 125, 'shields': 125, 'weapons': 125}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=110, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 350
    ship.crew_count = 350
    return ship


def create_aquarius_class(name, registry):
    """Aquarius-class Embedded Escort"""
    ship = AdvancedShip(name, registry, "Aquarius", "Embedded Escort", 2385)
    ship.reputation_cost = 1500
    ship.minimum_rank = 5
    ship.size = "Small"
    ship.cargo_space = 30
    ship.upgrade_space = 70
    
    ship.sensor_range = 7
    ship.turn_speed = 0
    ship.impulse_speed = 9
    ship.warp_speed = 9.5
    
    ship.max_hull = 600
    ship.hull = 600
    ship.armor = 50
    ship.shields = {'fore': 380, 'aft': 320, 'port': 350, 'starboard': 350}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 270
    ship.power_distribution = {'engines': 90, 'shields': 90, 'weapons': 90}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=8, firing_arcs=['fore'], max_torpedoes=60, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 40
    ship.crew_count = 40
    return ship


def create_defiant_class(name, registry):
    """Defiant-class Escort Warship"""
    ship = AdvancedShip(name, registry, "Defiant", "Escort Warship", 2370)
    ship.reputation_cost = 1600
    ship.minimum_rank = 5
    ship.size = "Small"
    ship.cargo_space = 40
    ship.upgrade_space = 90
    
    ship.sensor_range = 7
    ship.turn_speed = 0
    ship.impulse_speed = 8
    ship.warp_speed = 9.5
    
    ship.max_hull = 750
    ship.hull = 750
    ship.armor = 60
    ship.shields = {'fore': 480, 'aft': 400, 'port': 440, 'starboard': 440}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 300
    ship.power_distribution = {'engines': 100, 'shields': 100, 'weapons': 100}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=11, firing_arcs=['fore'], max_torpedoes=80, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=9, firing_arcs=['aft'], max_torpedoes=60, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 50
    ship.crew_count = 50
    return ship


def create_california_class(name, registry):
    """California-class Support Ship"""
    ship = AdvancedShip(name, registry, "California", "Support Ship", 2368)
    ship.reputation_cost = 1600
    ship.minimum_rank = 5
    ship.size = "Medium"
    ship.cargo_space = 200
    ship.upgrade_space = 110
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 5
    ship.warp_speed = 9.0
    
    ship.max_hull = 1100
    ship.hull = 1100
    ship.armor = 55
    ship.shields = {'fore': 520, 'aft': 440, 'port': 480, 'starboard': 480}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 375
    ship.power_distribution = {'engines': 125, 'shields': 125, 'weapons': 125}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=5, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    # Bonus: Enhanced engineering
    ship.systems['engineering'] = 120  # 120% effectiveness
    
    ship.max_crew = 350
    ship.crew_count = 350
    return ship


def create_parliament_class(name, registry):
    """Parliament-class Utility Cruiser"""
    ship = AdvancedShip(name, registry, "Parliament", "Utility Cruiser", 2370)
    ship.reputation_cost = 1800
    ship.minimum_rank = 5
    ship.size = "Large"
    ship.cargo_space = 250
    ship.upgrade_space = 120
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.2
    
    ship.max_hull = 1250
    ship.hull = 1250
    ship.armor = 58
    ship.shields = {'fore': 580, 'aft': 480, 'port': 530, 'starboard': 530}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 390
    ship.power_distribution = {'engines': 130, 'shields': 130, 'weapons': 130}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 500
    ship.crew_count = 500
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 6: COMMODORE - Elite Ships
# ═══════════════════════════════════════════════════════════════════

def create_reliant_class(name, registry):
    """Reliant-class Cruiser"""
    ship = AdvancedShip(name, registry, "Reliant", "Cruiser", 2375)
    ship.reputation_cost = 2200
    ship.minimum_rank = 6
    ship.size = "Large"
    ship.cargo_space = 200
    ship.upgrade_space = 125
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.4
    
    ship.max_hull = 1300
    ship.hull = 1300
    ship.armor = 62
    ship.shields = {'fore': 600, 'aft': 500, 'port': 550, 'starboard': 550}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 405
    ship.power_distribution = {'engines': 135, 'shields': 135, 'weapons': 135}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=9, firing_arcs=['fore'], max_torpedoes=130, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 400
    ship.crew_count = 400
    return ship


def create_ross_class(name, registry):
    """Ross-class Cruiser"""
    ship = AdvancedShip(name, registry, "Ross", "Cruiser", 2375)
    ship.reputation_cost = 2300
    ship.minimum_rank = 6
    ship.size = "Large"
    ship.cargo_space = 210
    ship.upgrade_space = 130
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.5
    
    ship.max_hull = 1350
    ship.hull = 1350
    ship.armor = 65
    ship.shields = {'fore': 620, 'aft': 520, 'port': 570, 'starboard': 570}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=9, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=140, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 450
    ship.crew_count = 450
    return ship


def create_inquiry_class(name, registry):
    """Inquiry-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Inquiry", "Heavy Cruiser", 2380)
    ship.reputation_cost = 2400
    ship.minimum_rank = 6
    ship.size = "Large"
    ship.cargo_space = 220
    ship.upgrade_space = 135
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.5
    
    ship.max_hull = 1400
    ship.hull = 1400
    ship.armor = 68
    ship.shields = {'fore': 640, 'aft': 540, 'port': 590, 'starboard': 590}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 435
    ship.power_distribution = {'engines': 145, 'shields': 145, 'weapons': 145}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=150, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=9, firing_arcs=['aft'], max_torpedoes=120, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 550
    ship.crew_count = 550
    return ship


def create_sutherland_class(name, registry):
    """Sutherland-class Science Cruiser (Nebula variant)"""
    ship = AdvancedShip(name, registry, "Sutherland", "Science Cruiser", 2375)
    ship.reputation_cost = 2400
    ship.minimum_rank = 6
    ship.size = "Large"
    ship.cargo_space = 260
    ship.upgrade_space = 145
    
    ship.sensor_range = 13
    ship.turn_speed = 3
    ship.impulse_speed = 5
    ship.warp_speed = 9.5
    
    ship.max_hull = 1550
    ship.hull = 1550
    ship.armor = 50
    ship.shields = {'fore': 660, 'aft': 540, 'port': 600, 'starboard': 600}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 450
    ship.power_distribution = {'engines': 150, 'shields': 150, 'weapons': 150}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=7, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=8, firing_arcs=['fore'], max_torpedoes=160, upgrade_space_cost=10),
        TorpedoBay('photon', mark=6, firing_arcs=['aft'], max_torpedoes=130, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 600
    ship.crew_count = 600
    return ship


def create_sovereign_class(name, registry):
    """Sovereign-class Battlecruiser"""
    ship = AdvancedShip(name, registry, "Sovereign", "Battlecruiser", 2372)
    ship.reputation_cost = 2500
    ship.minimum_rank = 6
    ship.size = "Very Large"
    ship.cargo_space = 350
    ship.upgrade_space = 160
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.7
    
    ship.max_hull = 1800
    ship.hull = 1800
    ship.armor = 120
    ship.shields = {'fore': 800, 'aft': 640, 'port': 720, 'starboard': 720}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 510
    ship.power_distribution = {'engines': 170, 'shields': 170, 'weapons': 170}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=11, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['fore'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=13, firing_arcs=['fore'], max_torpedoes=180, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=11, firing_arcs=['aft'], max_torpedoes=150, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 855
    ship.crew_count = 855
    return ship


def create_obena_class(name, registry):
    """Obena-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Obena", "Heavy Cruiser", 2380)
    ship.reputation_cost = 2500
    ship.minimum_rank = 6
    ship.size = "Large"
    ship.cargo_space = 230
    ship.upgrade_space = 140
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.5
    
    ship.max_hull = 1450
    ship.hull = 1450
    ship.armor = 70
    ship.shields = {'fore': 660, 'aft': 560, 'port': 610, 'starboard': 610}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 450
    ship.power_distribution = {'engines': 150, 'shields': 150, 'weapons': 150}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=11, firing_arcs=['fore'], max_torpedoes=160, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 600
    ship.crew_count = 600
    return ship


def create_dauntless_class(name, registry):
    """Dauntless-class Experimental Science Vessel"""
    ship = AdvancedShip(name, registry, "Dauntless", "Experimental Science Vessel", 2375)
    ship.reputation_cost = 2700
    ship.minimum_rank = 6
    ship.size = "Medium"
    ship.cargo_space = 100
    ship.upgrade_space = 120
    
    ship.sensor_range = 13
    ship.turn_speed = 1
    ship.impulse_speed = 8
    ship.warp_speed = 9.975
    
    ship.max_hull = 1050
    ship.hull = 1050
    ship.armor = 45
    ship.shields = {'fore': 560, 'aft': 480, 'port': 520, 'starboard': 520}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 405
    ship.power_distribution = {'engines': 135, 'shields': 135, 'weapons': 135}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 150
    ship.crew_count = 150
    return ship


def create_prometheus_class(name, registry):
    """Prometheus-class Advanced Escort"""
    ship = AdvancedShip(name, registry, "Prometheus", "Advanced Escort", 2374)
    ship.reputation_cost = 2800
    ship.minimum_rank = 6
    ship.size = "Medium"
    ship.cargo_space = 80
    ship.upgrade_space = 130
    
    ship.sensor_range = 10
    ship.turn_speed = 0
    ship.impulse_speed = 8
    ship.warp_speed = 9.9
    
    ship.max_hull = 1100
    ship.hull = 1100
    ship.armor = 75
    ship.shields = {'fore': 660, 'aft': 560, 'port': 610, 'starboard': 610}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 450
    ship.power_distribution = {'engines': 150, 'shields': 150, 'weapons': 150}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=12, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=12, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=11, firing_arcs=['fore'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=14, firing_arcs=['fore'], max_torpedoes=120, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=12, firing_arcs=['aft'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    # Special: Multi-vector assault mode (future feature)
    ship.special_weapons.append('Multi-Vector Assault Mode')
    
    ship.max_crew = 50
    ship.crew_count = 50
    return ship


def create_protostar_class(name, registry):
    """Protostar-class Experimental Warship"""
    ship = AdvancedShip(name, registry, "Protostar", "Experimental Warship", 2380)
    ship.reputation_cost = 2900
    ship.minimum_rank = 6
    ship.size = "Small"
    ship.cargo_space = 50
    ship.upgrade_space = 110
    
    ship.sensor_range = 9
    ship.turn_speed = 0
    ship.impulse_speed = 9
    ship.warp_speed = 9.9
    
    ship.max_hull = 1000
    ship.hull = 1000
    ship.armor = 78
    ship.shields = {'fore': 540, 'aft': 460, 'port': 500, 'starboard': 500}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=90, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 20
    ship.crew_count = 20
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 7: REAR ADMIRAL - 25th Century Fleet
# ═══════════════════════════════════════════════════════════════════

def create_luna_class(name, registry):
    """Luna-class Deep Space Science Vessel"""
    ship = AdvancedShip(name, registry, "Luna", "Deep Space Science Vessel", 2379)
    ship.reputation_cost = 2600
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 180
    ship.upgrade_space = 130
    
    ship.sensor_range = 14
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.7
    
    ship.max_hull = 1250
    ship.hull = 1250
    ship.armor = 42
    ship.shields = {'fore': 620, 'aft': 520, 'port': 570, 'starboard': 570}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=120, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 350
    ship.crew_count = 350
    return ship


def create_pathfinder_class(name, registry):
    """Pathfinder-class Long Range Science Vessel"""
    ship = AdvancedShip(name, registry, "Pathfinder", "Long Range Science Vessel", 2385)
    ship.reputation_cost = 2800
    ship.minimum_rank = 7
    ship.size = "Medium"
    ship.cargo_space = 110
    ship.upgrade_space = 115
    
    ship.sensor_range = 13
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.975
    
    ship.max_hull = 1050
    ship.hull = 1050
    ship.armor = 42
    ship.shields = {'fore': 520, 'aft': 440, 'port': 480, 'starboard': 480}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 390
    ship.power_distribution = {'engines': 130, 'shields': 130, 'weapons': 130}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=5, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=6, firing_arcs=['fore'], max_torpedoes=100, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 200
    ship.crew_count = 200
    return ship


def create_jein_class(name, registry):
    """Jein-class Cruiser"""
    ship = AdvancedShip(name, registry, "Jein", "Cruiser", 2385)
    ship.reputation_cost = 2800
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 210
    ship.upgrade_space = 140
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.5
    
    ship.max_hull = 1400
    ship.hull = 1400
    ship.armor = 80
    ship.shields = {'fore': 640, 'aft': 540, 'port': 590, 'starboard': 590}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 450
    ship.power_distribution = {'engines': 150, 'shields': 150, 'weapons': 150}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=9, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=150, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 550
    ship.crew_count = 550
    return ship


def create_shepard_class(name, registry):
    """Shepard-class Battlecruiser"""
    ship = AdvancedShip(name, registry, "Shepard", "Battlecruiser", 2385)
    ship.reputation_cost = 2900
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 260
    ship.upgrade_space = 150
    
    ship.sensor_range = 9
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.6
    
    ship.max_hull = 1550
    ship.hull = 1550
    ship.armor = 130
    ship.shields = {'fore': 700, 'aft': 580, 'port': 640, 'starboard': 640}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 480
    ship.power_distribution = {'engines': 160, 'shields': 160, 'weapons': 160}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=170, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=10, firing_arcs=['aft'], max_torpedoes=140, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 700
    ship.crew_count = 700
    return ship


def create_duderstadt_class(name, registry):
    """Duderstadt-class Science Vessel"""
    ship = AdvancedShip(name, registry, "Duderstadt", "Science Vessel", 2385)
    ship.reputation_cost = 2900
    ship.minimum_rank = 7
    ship.size = "Medium"
    ship.cargo_space = 140
    ship.upgrade_space = 125
    
    ship.sensor_range = 14
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.6
    
    ship.max_hull = 1150
    ship.hull = 1150
    ship.armor = 48
    ship.shields = {'fore': 580, 'aft': 500, 'port': 540, 'starboard': 540}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 420
    ship.power_distribution = {'engines': 140, 'shields': 140, 'weapons': 140}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=6, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=6, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('photon', mark=7, firing_arcs=['fore'], max_torpedoes=110, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 400
    ship.crew_count = 400
    return ship


def create_gagarin_class(name, registry):
    """Gagarin-class Battlecruiser"""
    ship = AdvancedShip(name, registry, "Gagarin", "Battlecruiser", 2385)
    ship.reputation_cost = 3000
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 270
    ship.upgrade_space = 155
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.6
    
    ship.max_hull = 1600
    ship.hull = 1600
    ship.armor = 135
    ship.shields = {'fore': 720, 'aft': 600, 'port': 660, 'starboard': 660}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 495
    ship.power_distribution = {'engines': 165, 'shields': 165, 'weapons': 165}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=180, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=10, firing_arcs=['aft'], max_torpedoes=150, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 750
    ship.crew_count = 750
    return ship


def create_excelsior_ii_class(name, registry):
    """Excelsior II-class Advanced Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Excelsior II", "Advanced Heavy Cruiser", 2385)
    ship.reputation_cost = 3000
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 300
    ship.upgrade_space = 150
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.6
    
    ship.max_hull = 1650
    ship.hull = 1650
    ship.armor = 95
    ship.shields = {'fore': 700, 'aft': 580, 'port': 640, 'starboard': 640}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 495
    ship.power_distribution = {'engines': 165, 'shields': 165, 'weapons': 165}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=170, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=9, firing_arcs=['aft'], max_torpedoes=140, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 800
    ship.crew_count = 800
    return ship


def create_alita_class(name, registry):
    """Alita-class Heavy Escort Carrier"""
    ship = AdvancedShip(name, registry, "Alita", "Heavy Escort Carrier", 2385)
    ship.reputation_cost = 3100
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 190
    ship.upgrade_space = 145
    
    ship.sensor_range = 8
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.5
    
    ship.max_hull = 1400
    ship.hull = 1400
    ship.armor = 100
    ship.shields = {'fore': 640, 'aft': 540, 'port': 590, 'starboard': 590}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 435
    ship.power_distribution = {'engines': 145, 'shields': 145, 'weapons': 145}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=220, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=11, firing_arcs=['aft'], max_torpedoes=180, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 550
    ship.crew_count = 550
    return ship


def create_echelon_class(name, registry):
    """Echelon-class Battlecruiser"""
    ship = AdvancedShip(name, registry, "Echelon", "Battlecruiser", 2385)
    ship.reputation_cost = 3100
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 260
    ship.upgrade_space = 155
    
    ship.sensor_range = 10
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.6
    
    ship.max_hull = 1550
    ship.hull = 1550
    ship.armor = 130
    ship.shields = {'fore': 720, 'aft': 600, 'port': 660, 'starboard': 660}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 495
    ship.power_distribution = {'engines': 165, 'shields': 165, 'weapons': 165}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=180, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 700
    ship.crew_count = 700
    return ship


def create_edison_class(name, registry):
    """Edison-class Temporal Warship"""
    ship = AdvancedShip(name, registry, "Edison", "Temporal Warship", 2385)
    ship.reputation_cost = 3200
    ship.minimum_rank = 7
    ship.size = "Medium"
    ship.cargo_space = 150
    ship.upgrade_space = 140
    
    ship.sensor_range = 11
    ship.turn_speed = 1
    ship.impulse_speed = 7
    ship.warp_speed = 9.7
    
    ship.max_hull = 1350
    ship.hull = 1350
    ship.armor = 112
    ship.shields = {'fore': 660, 'aft': 560, 'port': 610, 'starboard': 610}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 465
    ship.power_distribution = {'engines': 155, 'shields': 155, 'weapons': 155}
    
    ship.weapon_arrays = [
        WeaponArray('antiproton', mark=11, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('antiproton', mark=10, firing_arcs=['aft'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('chroniton', mark=13, firing_arcs=['fore'], max_torpedoes=140, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 300
    ship.crew_count = 300
    return ship


def create_sagan_class(name, registry):
    """Sagan-class Multi-Mission Explorer"""
    ship = AdvancedShip(name, registry, "Sagan", "Multi-Mission Explorer", 2385)
    ship.reputation_cost = 3200
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 240
    ship.upgrade_space = 145
    
    ship.sensor_range = 12
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.7
    
    ship.max_hull = 1450
    ship.hull = 1450
    ship.armor = 82
    ship.shields = {'fore': 670, 'aft': 560, 'port': 615, 'starboard': 615}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 465
    ship.power_distribution = {'engines': 155, 'shields': 155, 'weapons': 155}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=9, firing_arcs=['fore'], max_torpedoes=150, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 600
    ship.crew_count = 600
    return ship


def create_constitution_iii_class(name, registry):
    """Constitution III-class Exploration Vessel"""
    ship = AdvancedShip(name, registry, "Constitution III", "Exploration Vessel", 2385)
    ship.reputation_cost = 3300
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 250
    ship.upgrade_space = 150
    
    ship.sensor_range = 11
    ship.turn_speed = 2
    ship.impulse_speed = 7
    ship.warp_speed = 9.7
    
    ship.max_hull = 1500
    ship.hull = 1500
    ship.armor = 82
    ship.shields = {'fore': 680, 'aft': 560, 'port': 620, 'starboard': 620}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 480
    ship.power_distribution = {'engines': 160, 'shields': 160, 'weapons': 160}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=9, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=160, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=8, firing_arcs=['aft'], max_torpedoes=130, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 500
    ship.crew_count = 500
    return ship


def create_vesta_class(name, registry):
    """Vesta-class Multi-Mission Explorer"""
    ship = AdvancedShip(name, registry, "Vesta", "Multi-Mission Explorer", 2385)
    ship.reputation_cost = 3500
    ship.minimum_rank = 7
    ship.size = "Large"
    ship.cargo_space = 280
    ship.upgrade_space = 155
    
    ship.sensor_range = 13
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.85
    
    ship.max_hull = 1450
    ship.hull = 1450
    ship.armor = 82
    ship.shields = {'fore': 700, 'aft': 580, 'port': 640, 'starboard': 640}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 480
    ship.power_distribution = {'engines': 160, 'shields': 160, 'weapons': 160}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=8, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=160, upgrade_space_cost=10)
    ]
    
    # Special: Quantum slipstream drive
    ship.special_weapons.append('Quantum Slipstream Drive')
    
    ship.max_crew = 750
    ship.crew_count = 750
    return ship


# ═══════════════════════════════════════════════════════════════════
# RANK 8: VICE ADMIRAL - Command Ships
# ═══════════════════════════════════════════════════════════════════

def create_curiosity_class(name, registry):
    """Curiosity-class Heavy Cruiser"""
    ship = AdvancedShip(name, registry, "Curiosity", "Heavy Cruiser", 2385)
    ship.reputation_cost = 3600
    ship.minimum_rank = 8
    ship.size = "Large"
    ship.cargo_space = 290
    ship.upgrade_space = 160
    
    ship.sensor_range = 11
    ship.turn_speed = 2
    ship.impulse_speed = 6
    ship.warp_speed = 9.7
    
    ship.max_hull = 1600
    ship.hull = 1600
    ship.armor = 88
    ship.shields = {'fore': 740, 'aft': 620, 'port': 680, 'starboard': 680}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 510
    ship.power_distribution = {'engines': 170, 'shields': 170, 'weapons': 170}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=180, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 800
    ship.crew_count = 800
    return ship


def create_venture_class(name, registry):
    """Venture-class Galaxy Dreadnought"""
    ship = AdvancedShip(name, registry, "Venture", "Galaxy Dreadnought", 2385)
    ship.reputation_cost = 3800
    ship.minimum_rank = 8
    ship.size = "Very Large"
    ship.cargo_space = 520
    ship.upgrade_space = 210
    
    ship.sensor_range = 11
    ship.turn_speed = 3
    ship.impulse_speed = 5
    ship.warp_speed = 9.7
    
    ship.max_hull = 2100
    ship.hull = 2100
    ship.armor = 170
    ship.shields = {'fore': 850, 'aft': 680, 'port': 765, 'starboard': 765}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 570
    ship.power_distribution = {'engines': 190, 'shields': 190, 'weapons': 190}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=12, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=11, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['fore'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=14, firing_arcs=['fore'], max_torpedoes=220, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=12, firing_arcs=['aft'], max_torpedoes=180, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 1000
    ship.crew_count = 1000
    return ship


def create_odyssey_class(name, registry):
    """Odyssey-class Star Cruiser"""
    ship = AdvancedShip(name, registry, "Odyssey", "Star Cruiser", 2385)
    ship.reputation_cost = 4000
    ship.minimum_rank = 8
    ship.size = "Huge"
    ship.cargo_space = 600
    ship.upgrade_space = 230
    
    ship.sensor_range = 12
    ship.turn_speed = 3
    ship.impulse_speed = 5
    ship.warp_speed = 9.8
    
    ship.max_hull = 2200
    ship.hull = 2200
    ship.armor = 118
    ship.shields = {'fore': 900, 'aft': 720, 'port': 810, 'starboard': 810}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 600
    ship.power_distribution = {'engines': 200, 'shields': 200, 'weapons': 200}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=10, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=10, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=9, firing_arcs=['fore'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=12, firing_arcs=['fore'], max_torpedoes=240, upgrade_space_cost=10),
        TorpedoBay('quantum', mark=10, firing_arcs=['aft'], max_torpedoes=200, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 2500
    ship.crew_count = 2500
    return ship


def create_yorktown_class(name, registry):
    """Yorktown-class Science Star Cruiser"""
    ship = AdvancedShip(name, registry, "Yorktown", "Science Star Cruiser", 2385)
    ship.reputation_cost = 4200
    ship.minimum_rank = 8
    ship.size = "Huge"
    ship.cargo_space = 580
    ship.upgrade_space = 225
    
    ship.sensor_range = 15
    ship.turn_speed = 3
    ship.impulse_speed = 5
    ship.warp_speed = 9.8
    
    ship.max_hull = 2150
    ship.hull = 2150
    ship.armor = 82
    ship.shields = {'fore': 880, 'aft': 700, 'port': 790, 'starboard': 790}
    ship.max_shields = ship.shields.copy()
    
    ship.warp_core_max_power = 585
    ship.power_distribution = {'engines': 195, 'shields': 195, 'weapons': 195}
    
    ship.weapon_arrays = [
        WeaponArray('phaser', mark=9, firing_arcs=['fore', 'port', 'starboard'], upgrade_space_cost=5),
        WeaponArray('phaser', mark=8, firing_arcs=['aft', 'port', 'starboard'], upgrade_space_cost=5)
    ]
    ship.torpedo_bays = [
        TorpedoBay('quantum', mark=10, firing_arcs=['fore'], max_torpedoes=230, upgrade_space_cost=10)
    ]
    
    ship.max_crew = 2500
    ship.crew_count = 2500
    return ship


# ═══════════════════════════════════════════════════════════════════
# FEDERATION SHIP CATALOGUE
# ═══════════════════════════════════════════════════════════════════

# Dictionary mapping Federation ship class names to their creation functions
FEDERATION_CATALOGUE = {
    # Rank 0
    'Daedalus': create_daedalus_class,
    'Oberth': create_oberth_class,
    'Sydney': create_sydney_class,
    'Miranda': create_miranda_class,
    
    # Rank 1
    'Ptolemy': create_ptolemy_class,
    'Soyuz': create_soyuz_class,
    'Constitution': create_constitution_class,
    
    # Rank 2
    'Hermes': create_hermes_class,
    'Saladin': create_saladin_class,
    'Constellation': create_constellation_class,
    'Antares': create_antares_class,
    
    # Rank 3
    'Constitution Refit': create_constitution_refit_class,
    'Excelsior': create_excelsior_class,
    'Ambassador': create_ambassador_class,
    'Springfield': create_springfield_class,
    'Cheyenne': create_cheyenne_class,
    'Challenger': create_challenger_class,
    'New Orleans': create_new_orleans_class,
    'Freedom': create_freedom_class,
    'Nova': create_nova_class,
    
    # Rank 4
    'Niagara': create_niagara_class,
    'Olympic': create_olympic_class,
    'Yeager': create_yeager_class,
    'Saber': create_saber_class,
    'Bradbury': create_bradbury_class,
    'Renaissance': create_renaissance_class,
    'Steamrunner': create_steamrunner_class,
    'Norway': create_norway_class,
    'Nebula': create_nebula_class,
    'Centaur': create_centaur_class,
    'Intrepid': create_intrepid_class,
    'Akira': create_akira_class,
    
    # Rank 5
    'Curry': create_curry_class,
    'Aquarius': create_aquarius_class,
    'Defiant': create_defiant_class,
    'California': create_california_class,
    'Parliament': create_parliament_class,
    'Galaxy': create_galaxy_class,
    
    # Rank 6
    'Reliant': create_reliant_class,
    'Ross': create_ross_class,
    'Inquiry': create_inquiry_class,
    'Sutherland': create_sutherland_class,
    'Sovereign': create_sovereign_class,
    'Obena': create_obena_class,
    'Dauntless': create_dauntless_class,
    'Prometheus': create_prometheus_class,
    'Protostar': create_protostar_class,
    
    # Rank 7
    'Luna': create_luna_class,
    'Pathfinder': create_pathfinder_class,
    'Jein': create_jein_class,
    'Shepard': create_shepard_class,
    'Duderstadt': create_duderstadt_class,
    'Gagarin': create_gagarin_class,
    'Excelsior II': create_excelsior_ii_class,
    'Alita': create_alita_class,
    'Echelon': create_echelon_class,
    'Edison': create_edison_class,
    'Sagan': create_sagan_class,
    'Constitution III': create_constitution_iii_class,
    'Vesta': create_vesta_class,
    
    # Rank 8
    'Curiosity': create_curiosity_class,
    'Venture': create_venture_class,
    'Odyssey': create_odyssey_class,
    'Yorktown': create_yorktown_class,
}


def get_federation_ship(ship_class, name="USS Unnamed", registry="NCC-0000"):
    """
    Create a Federation ship by its class name.
    
    Args:
        ship_class: Name of the ship class (e.g., 'Miranda', 'Galaxy')
        name: Ship name (default: "USS Unnamed")
        registry: Ship registry number (default: "NCC-0000")
        
    Returns:
        AdvancedShip instance or None if class not found
    """
    if ship_class in FEDERATION_CATALOGUE:
        return FEDERATION_CATALOGUE[ship_class](name, registry)
    return None


def get_federation_ships_by_rank(min_rank=0, max_rank=8, player_reputation=0):
    """
    Get list of ship classes available for a given rank range and reputation.
    
    Args:
        min_rank: Minimum rank to include (default: 0)
        max_rank: Maximum rank to include (default: 8)
        player_reputation: Player's current reputation (filters by reputation_cost)
        
    Returns:
        List of dictionaries with ship info: {
            'class': ship class name,
            'type': ship type,
            'era': ship era,
            'minimum_rank': required rank,
            'reputation_cost': required reputation,
            'size': ship size,
            'hull': max hull points,
            'crew': max crew capacity
        }
    """
    available_ships = []
    
    for ship_class, creator_func in FEDERATION_CATALOGUE.items():
        # Create temporary ship to get its stats
        temp_ship = creator_func("USS Temp", "NCC-TEMP")
        
        # Check if ship meets criteria
        if (min_rank <= temp_ship.minimum_rank <= max_rank and 
            temp_ship.reputation_cost <= player_reputation):
            
            ship_info = {
                'class': ship_class,
                'type': temp_ship.type,
                'era': temp_ship.era,
                'minimum_rank': temp_ship.minimum_rank,
                'reputation_cost': temp_ship.reputation_cost,
                'size': temp_ship.size,
                'hull': temp_ship.max_hull,
                'crew': temp_ship.max_crew,
                'warp': temp_ship.warp_speed,
                'sensors': temp_ship.sensor_range
            }
            available_ships.append(ship_info)
    
    # Sort by rank, then by reputation cost
    available_ships.sort(key=lambda x: (x['minimum_rank'], x['reputation_cost']))
    
    return available_ships


def get_all_federation_ships():
    """
    Get list of all available Federation ship classes.
    
    Returns:
        List of ship class names
    """
    return sorted(FEDERATION_CATALOGUE.keys())


def get_federation_ships_at_rank(rank):
    """
    Get all ships available at a specific rank.
    
    Args:
        rank: The rank level (0-8)
        
    Returns:
        List of ship class names at that rank
    """
    ships_at_rank = []
    
    for ship_class, creator_func in FEDERATION_CATALOGUE.items():
        temp_ship = creator_func("USS Temp", "NCC-TEMP")
        if temp_ship.minimum_rank == rank:
            ships_at_rank.append(ship_class)
    
    return sorted(ships_at_rank)


def create_starting_ship(species="Human"):
    """
    Create the starting ship for a new character (Miranda-class).
    All species start with the same ship.
    
    Args:
        species: Character's species (not used, but kept for compatibility)
        
    Returns:
        Miranda-class AdvancedShip
    """
    return create_miranda_class("USS Enterprise", "NCC-1701")
