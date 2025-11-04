"""
Galaxy Map and Star System Generation
Procedurally generates the galaxy with fixed canonical systems
"""

import random
import math

class StarSystem:
    """Represents a star system"""
    
    STAR_TYPES = ['M', 'K', 'G', 'F', 'A', 'B', 'O']
    
    def __init__(self, name, x, y, star_type=None, is_canonical=False):
        self.name = name
        self.x = x
        self.y = y
        self.star_type = star_type or random.choice(self.STAR_TYPES)
        self.is_canonical = is_canonical
        self.explored = False
        
        # Planets
        self.planets = self._generate_planets()
        
        # Features
        self.has_station = is_canonical or random.random() < 0.05
        self.has_anomaly = random.random() < 0.1
        self.controlling_faction = None
        
        # Inhabitants
        self.inhabited = random.random() < 0.3
        self.civilization_level = random.randint(1, 10) if self.inhabited else 0
        
    def _generate_planets(self):
        """Generate planets for this system"""
        num_planets = random.randint(0, 12)
        planets = []
        
        for i in range(num_planets):
            planet_types = ['M-Class', 'Gas Giant', 'Ice', 'Desert', 'Volcanic', 
                          'Ocean', 'Barren', 'Toxic']
            planets.append({
                'number': i + 1,
                'type': random.choice(planet_types),
                'has_life': random.random() < 0.2,
                'resources': random.choice(['None', 'Dilithium', 'Rare Minerals', 'Abundant'])
            })
            
        return planets
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'star_type': self.star_type,
            'is_canonical': self.is_canonical,
            'explored': self.explored,
            'planets': self.planets,
            'has_station': self.has_station,
            'has_anomaly': self.has_anomaly,
            'controlling_faction': self.controlling_faction,
            'inhabited': self.inhabited,
            'civilization_level': self.civilization_level
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        system = cls(data['name'], data['x'], data['y'], data['star_type'], data['is_canonical'])
        system.explored = data['explored']
        system.planets = data['planets']
        system.has_station = data['has_station']
        system.has_anomaly = data['has_anomaly']
        system.controlling_faction = data['controlling_faction']
        system.inhabited = data['inhabited']
        system.civilization_level = data['civilization_level']
        return system


class Galaxy:
    """Manages the galaxy map and systems"""
    
    # Canonical systems (famous locations)
    CANONICAL_SYSTEMS = {
        'Sol': {'x': 0, 'y': 0, 'faction': 'Federation', 'star_type': 'G'},
        'Vulcan': {'x': 16, 'y': -5, 'faction': 'Federation', 'star_type': 'K'},
        'Andoria': {'x': -12, 'y': 8, 'faction': 'Federation', 'star_type': 'F'},
        "Qo'noS": {'x': -25, 'y': 30, 'faction': 'Klingon Empire', 'star_type': 'K'},
        'Romulus': {'x': 35, 'y': -40, 'faction': 'Romulan Star Empire', 'star_type': 'G'},
        'Cardassia': {'x': -45, 'y': -20, 'faction': 'Cardassian Union', 'star_type': 'G'},
        'Bajor': {'x': -38, 'y': -18, 'faction': 'Federation', 'star_type': 'G'},
        'Deep Space Nine': {'x': -38, 'y': -17, 'faction': 'Federation', 'star_type': 'G'},
        'Ferenginar': {'x': 52, 'y': 15, 'faction': 'Ferengi Alliance', 'star_type': 'K'},
        'Betazed': {'x': 10, 'y': 12, 'faction': 'Federation', 'star_type': 'G'},
        'Trill': {'x': 8, 'y': -10, 'faction': 'Federation', 'star_type': 'G'},
        'Risa': {'x': 20, 'y': 5, 'faction': 'Federation', 'star_type': 'G'},
        'Starbase 1': {'x': 5, 'y': 3, 'faction': 'Federation', 'star_type': 'G'}
    }
    
    def __init__(self, size=100):
        self.size = size  # Galaxy radius
        self.systems = {}
        self.current_system = None
        
    def generate(self):
        """Generate the galaxy with canonical and procedural systems"""
        # Add canonical systems first
        for name, data in self.CANONICAL_SYSTEMS.items():
            system = StarSystem(name, data['x'], data['y'], data['star_type'], is_canonical=True)
            system.controlling_faction = data['faction']
            system.explored = (name == 'Sol')  # Only Sol starts explored
            system.inhabited = True
            system.civilization_level = 10
            self.systems[name] = system
            
        # Generate procedural systems
        num_systems = random.randint(150, 250)
        generated = 0
        attempts = 0
        max_attempts = num_systems * 10
        
        while generated < num_systems and attempts < max_attempts:
            attempts += 1
            
            # Random position
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, self.size)
            x = int(distance * math.cos(angle))
            y = int(distance * math.sin(angle))
            
            # Check if too close to existing systems
            too_close = False
            for system in self.systems.values():
                dist = math.sqrt((system.x - x)**2 + (system.y - y)**2)
                if dist < 5:  # Minimum distance between systems
                    too_close = True
                    break
                    
            if not too_close:
                name = self._generate_system_name()
                system = StarSystem(name, x, y)
                
                # Assign factions based on proximity to canonical systems
                system.controlling_faction = self._determine_faction(x, y)
                
                self.systems[name] = system
                generated += 1
                
        # Set starting position (Sol system)
        self.current_system = 'Sol'
        
    def _generate_system_name(self):
        """Generate a random system name"""
        prefixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta',
                   'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho',
                   'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
        
        suffixes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
        
        # Generate unique name
        while True:
            if random.random() < 0.3:
                # Greek letter + constellation
                constellations = ['Centauri', 'Orionis', 'Cygni', 'Draconis', 'Ursae',
                                'Serpentis', 'Aquilae', 'Leonis', 'Scorpii', 'Virginis']
                name = f"{random.choice(prefixes)} {random.choice(constellations)}"
            else:
                # Catalog number
                catalog = random.choice(['NGC', 'IC', 'M', 'HR'])
                number = random.randint(1000, 9999)
                name = f"{catalog}-{number}"
                
            if name not in self.systems:
                return name
                
    def _determine_faction(self, x, y):
        """Determine controlling faction based on proximity to faction homeworlds"""
        faction_centers = {
            'Federation': (0, 0),
            'Klingon Empire': (-25, 30),
            'Romulan Star Empire': (35, -40),
            'Cardassian Union': (-45, -20),
            'Ferengi Alliance': (52, 15)
        }
        
        closest_faction = None
        closest_distance = float('inf')
        
        for faction, (fx, fy) in faction_centers.items():
            distance = math.sqrt((x - fx)**2 + (y - fy)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_faction = faction
                
        # Distant systems may be unclaimed
        if closest_distance > 60:
            return random.choice([None, closest_faction])
            
        return closest_faction
        
    def get_system(self, name):
        """Get a system by name"""
        return self.systems.get(name)
        
    def get_nearby_systems(self, system_name, max_distance=20):
        """Get systems within range"""
        if system_name not in self.systems:
            return []
            
        current = self.systems[system_name]
        nearby = []
        
        for name, system in self.systems.items():
            if name == system_name:
                continue
                
            distance = math.sqrt((system.x - current.x)**2 + (system.y - current.y)**2)
            if distance <= max_distance:
                nearby.append((name, system, distance))
                
        # Sort by distance
        nearby.sort(key=lambda x: x[2])
        return nearby
        
    def calculate_distance(self, system1_name, system2_name):
        """Calculate distance between two systems"""
        if system1_name not in self.systems or system2_name not in self.systems:
            return None
            
        s1 = self.systems[system1_name]
        s2 = self.systems[system2_name]
        
        return math.sqrt((s2.x - s1.x)**2 + (s2.y - s1.y)**2)
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'size': self.size,
            'systems': {name: system.to_dict() for name, system in self.systems.items()},
            'current_system': self.current_system
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        galaxy = cls(data['size'])
        galaxy.systems = {name: StarSystem.from_dict(sys_data) 
                         for name, sys_data in data['systems'].items()}
        galaxy.current_system = data['current_system']
        return galaxy
