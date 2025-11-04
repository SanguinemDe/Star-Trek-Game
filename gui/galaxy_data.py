"""
Star Trek Galaxy Data
Accurate locations of major systems and political boundaries
Based on Star Trek lore and star charts
"""
from gui.hex_map import StarSystem

def create_star_trek_galaxy():
    """
    Create the Star Trek galaxy with major systems
    Coordinate system: (0, 0) = Sol system (Earth)
    Distances are approximate based on canon sources
    """
    systems = []
    
    # ===== FEDERATION CORE WORLDS =====
    
    # Sol System (Earth) - Federation Capital
    systems.append(StarSystem("Sol", 0, 0, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Vulcan - 16 light years from Earth
    systems.append(StarSystem("Vulcan", 8, -8, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Andoria - ~60 light years from Earth
    systems.append(StarSystem("Andoria", -30, -15, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Tellar Prime - ~61 light years from Earth
    systems.append(StarSystem("Tellar", 25, -25, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Betazed - ~300 light years from Earth
    systems.append(StarSystem("Betazed", 150, -75, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Trill - ~90 light years from Earth
    systems.append(StarSystem("Trill", -40, 20, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Bajor - ~52 light years from Earth
    systems.append(StarSystem("Bajor", 30, 15, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # Bolarus IX
    systems.append(StarSystem("Bolarus IX", -20, -40, faction='Federation', 
                             system_type='homeworld', importance='major'))
    
    # ===== MAJOR FEDERATION OUTPOSTS =====
    
    # Deep Space Nine / Bajor system
    systems.append(StarSystem("Deep Space Nine", 30, 16, faction='Federation', 
                             system_type='station', importance='major'))
    
    # Starbase 1 (Earth orbit)
    systems.append(StarSystem("Starbase 1", 0, 1, faction='Federation', 
                             system_type='station', importance='major'))
    
    # Starbase 375 (Dominion War staging area)
    systems.append(StarSystem("Starbase 375", 40, 25, faction='Federation', 
                             system_type='station', importance='major'))
    
    # Alpha Centauri - 4.3 light years from Earth
    systems.append(StarSystem("Alpha Centauri", 2, -2, faction='Federation', 
                             importance='major'))
    
    # Deneb - ~2600 ly but simplified for gameplay
    systems.append(StarSystem("Deneb", 80, -100, faction='Federation', 
                             importance='major'))
    
    # Rigel - ~860 light years
    systems.append(StarSystem("Rigel", -60, 80, faction='Federation', 
                             importance='major'))
    
    # ===== KLINGON EMPIRE =====
    
    # Qo'noS (Klingon Homeworld) - ~90 light years from Earth
    systems.append(StarSystem("Qo'noS", -45, 45, faction='Klingon', 
                             system_type='homeworld', importance='major'))
    
    # Boreth (Klingon monastery)
    systems.append(StarSystem("Boreth", -50, 40, faction='Klingon', 
                             importance='major'))
    
    # Khitomer
    systems.append(StarSystem("Khitomer", -40, 50, faction='Klingon', 
                             importance='major'))
    
    # Ty'Gokor
    systems.append(StarSystem("Ty'Gokor", -55, 50, faction='Klingon', 
                             importance='major'))
    
    # ===== ROMULAN STAR EMPIRE =====
    
    # Romulus - ~60 light years from Earth
    systems.append(StarSystem("Romulus", 30, -60, faction='Romulan', 
                             system_type='homeworld', importance='major'))
    
    # Remus (twin planet)
    systems.append(StarSystem("Remus", 31, -60, faction='Romulan', 
                             importance='major'))
    
    # ===== CARDASSIAN UNION =====
    
    # Cardassia Prime - ~60 light years from Bajor
    systems.append(StarSystem("Cardassia", 60, 40, faction='Cardassian', 
                             system_type='homeworld', importance='major'))
    
    # ===== NEUTRAL ZONE & BORDER SYSTEMS =====
    
    # Neutral Zone markers (Federation-Romulan)
    systems.append(StarSystem("Outpost 23", 20, -40, faction='Federation', 
                             system_type='outpost', importance='minor'))
    
    # ===== UNKNOWN/UNEXPLORED SPACE =====
    
    # Add some unexplored systems
    for i in range(50):
        import random
        q = random.randint(-100, 100)
        r = random.randint(-100, 100)
        # Don't overlap with major systems
        if not any(abs(s.q - q) < 5 and abs(s.r - r) < 5 for s in systems):
            systems.append(StarSystem(f"Unknown {i+1}", q, r, 
                                    faction=None, importance='minor'))
    
    return systems


def get_faction_boundaries():
    """
    Get approximate political boundaries
    Returns dict of faction -> list of border hexes
    """
    boundaries = {
        'Federation': [
            # Rough Federation space boundary
            (-60, -60), (60, -60), (80, 0), (60, 80), (-20, 60), (-60, 0)
        ],
        'Klingon': [
            # Klingon Empire boundary
            (-80, 20), (-40, 20), (-20, 60), (-60, 80), (-100, 60), (-100, 20)
        ],
        'Romulan': [
            # Romulan Star Empire boundary
            (10, -80), (60, -80), (80, -40), (60, -20), (20, -40), (10, -60)
        ],
        'Cardassian': [
            # Cardassian Union boundary
            (40, 20), (80, 20), (100, 60), (80, 80), (40, 60), (40, 40)
        ]
    }
    return boundaries
