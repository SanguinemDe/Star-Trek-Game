"""
Equipment and Upgrade System
Starfleet Mark (Mk) system for ship upgrades
"""


class Equipment:
    """Base class for ship equipment"""
    
    def __init__(self, name, mark, equipment_type, upgrade_space_cost):
        self.name = name
        self.mark = mark  # Mk I through Mk XV
        self.equipment_type = equipment_type  # 'weapon', 'shield', 'engine', 'deflector', 'warp_core', etc.
        self.upgrade_space_cost = upgrade_space_cost


class WeaponEquipment(Equipment):
    """Weapon system upgrades (Phasers, Disruptors, Torpedoes)"""
    
    def __init__(self, name, mark, weapon_type, upgrade_space_cost=5):
        super().__init__(name, mark, 'weapon', upgrade_space_cost)
        self.weapon_type = weapon_type  # 'phaser', 'disruptor', 'photon', 'quantum', 'plasma'
        
    def get_damage(self):
        """Absolute damage value based on weapon type and mark"""
        # Base damage per weapon type at Mk I
        base_damages = {
            'phaser': 15,
            'disruptor': 18,
            'plasma': 20,
            'polaron': 16,
            'tetryon': 14,
            'photon': 80,  # Torpedoes
            'quantum': 100,
            'tricobalt': 120
        }
        base = base_damages.get(self.weapon_type, 15)
        # Energy weapons: +5 per mark, Torpedoes: +10 per mark
        increment = 10 if self.weapon_type in ['photon', 'quantum', 'tricobalt', 'plasma_torp'] else 5
        return base + (self.mark - 1) * increment
    
    def get_accuracy_bonus(self):
        """Accuracy bonus in percentage points"""
        return self.mark * 2  # +2% accuracy per mark


class ShieldEquipment(Equipment):
    """Shield system upgrades"""
    
    def __init__(self, name, mark, shield_type='standard', upgrade_space_cost=8):
        super().__init__(name, mark, 'shield', upgrade_space_cost)
        self.shield_type = shield_type  # 'standard', 'regenerative', 'covariant', 'resilient'
        
    def get_capacity_bonus(self):
        """Shield capacity increase (absolute value)"""
        # Base: +50 capacity per mark
        # Covariant: +75 capacity per mark
        if self.shield_type == 'covariant':
            return self.mark * 75
        return self.mark * 50
    
    def get_regeneration_bonus(self):
        """Shield regeneration rate bonus (points per turn)"""
        # Regenerative: +8 points per mark
        # Standard: +3 points per mark
        if self.shield_type == 'regenerative':
            return self.mark * 8
        return self.mark * 3
    
    def get_damage_reduction(self):
        """Extra damage reduction for resilient shields (absolute armor value)"""
        if self.shield_type == 'resilient':
            return self.mark * 5  # +5 armor per mark
        return 0


class ImpulseEngineEquipment(Equipment):
    """Impulse engine upgrades"""
    
    def __init__(self, name, mark, upgrade_space_cost=6):
        super().__init__(name, mark, 'impulse_engine', upgrade_space_cost)
        
    def get_speed_bonus(self):
        """Impulse speed increase (hexes per turn)"""
        return self.mark * 1  # +1 hex per mark
    
    def get_turn_rate_bonus(self):
        """Turn rate improvement (reduces turn_speed value)"""
        return int(self.mark / 3)  # -1 turn cost every 3 marks


class WarpCoreEquipment(Equipment):
    """Warp core upgrades"""
    
    def __init__(self, name, mark, core_type='standard', upgrade_space_cost=10):
        super().__init__(name, mark, 'warp_core', upgrade_space_cost)
        self.core_type = core_type  # 'standard', 'overcharged', 'efficient'
        
    def get_power_bonus(self):
        """Total power increase (absolute value)"""
        # Overcharged: +20 power per mark
        # Standard: +15 power per mark
        if self.core_type == 'overcharged':
            return self.mark * 20
        return self.mark * 15
    
    def get_efficiency_bonus(self):
        """Power efficiency (reduces power costs)"""
        # Efficient cores reduce power consumption
        if self.core_type == 'efficient':
            return self.mark * 2  # -2% power costs per mark
        return 0


class DeflectorEquipment(Equipment):
    """Deflector dish upgrades (sensors and science)"""
    
    def __init__(self, name, mark, upgrade_space_cost=7):
        super().__init__(name, mark, 'deflector', upgrade_space_cost)
        
    def get_sensor_range_bonus(self):
        """Sensor range increase (hexes)"""
        return int(self.mark / 2)  # +1 hex every 2 marks
    
    def get_auxiliary_power_bonus(self):
        """Auxiliary power boost (absolute value)"""
        return self.mark * 5  # +5 aux power per mark


class WarpEngineEquipment(Equipment):
    """Warp drive upgrades"""
    
    def __init__(self, name, mark, upgrade_space_cost=8):
        super().__init__(name, mark, 'warp_engine', upgrade_space_cost)
        
    def get_warp_speed_bonus(self):
        """Warp speed improvement (warp factor increase)"""
        return self.mark * 0.1  # +0.1 warp factor per mark
    
    def get_sector_speed_bonus(self):
        """Sector travel speed increase (percentage)"""
        return self.mark * 5  # +5% speed per mark


class ArmorEquipment(Equipment):
    """Hull armor plating"""
    
    def __init__(self, name, mark, armor_type='ablative', upgrade_space_cost=6):
        super().__init__(name, mark, 'armor', upgrade_space_cost)
        self.armor_type = armor_type  # 'ablative', 'neutronium', 'polarized'
        
    def get_armor_bonus(self):
        """Armor damage reduction bonus (absolute armor value)"""
        # Ablative: +3 armor per mark
        # Neutronium: +4 armor per mark
        # Polarized: +2 armor per mark (but provides special bonuses vs energy weapons)
        if self.armor_type == 'neutronium':
            return self.mark * 4
        elif self.armor_type == 'polarized':
            return self.mark * 2
        return self.mark * 3  # ablative
    
    def get_hull_bonus(self):
        """Hull HP increase (absolute value)"""
        # Neutronium: +100 hull per mark
        # Standard: +50 hull per mark
        if self.armor_type == 'neutronium':
            return self.mark * 100
        return self.mark * 50


# ═══════════════════════════════════════════════════════════════════
# EQUIPMENT CATALOGUE
# ═══════════════════════════════════════════════════════════════════

def create_phaser_array(mark):
    """Create a phaser array of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Phaser Array Mk {mark_names[mark]}"
    return WeaponEquipment(name, mark, 'phaser', upgrade_space_cost=5)


def create_disruptor_array(mark):
    """Create a disruptor array of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Disruptor Array Mk {mark_names[mark]}"
    return WeaponEquipment(name, mark, 'disruptor', upgrade_space_cost=5)


def create_photon_launcher(mark):
    """Create a photon torpedo launcher of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Photon Torpedo Launcher Mk {mark_names[mark]}"
    return WeaponEquipment(name, mark, 'photon', upgrade_space_cost=5)


def create_quantum_launcher(mark):
    """Create a quantum torpedo launcher of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Quantum Torpedo Launcher Mk {mark_names[mark]}"
    return WeaponEquipment(name, mark, 'quantum', upgrade_space_cost=6)


def create_shield_array(mark, shield_type='standard'):
    """Create a shield array of specified mark and type"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    type_names = {
        'standard': 'Covariant Shield Array',
        'regenerative': 'Regenerative Shield Array',
        'covariant': 'Covariant Shield Array',
        'resilient': 'Resilient Shield Array'
    }
    name = f"{type_names.get(shield_type, 'Shield Array')} Mk {mark_names[mark]}"
    return ShieldEquipment(name, mark, shield_type, upgrade_space_cost=8)


def create_impulse_engine(mark):
    """Create an impulse engine of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Impulse Engine Mk {mark_names[mark]}"
    return ImpulseEngineEquipment(name, mark, upgrade_space_cost=6)


def create_warp_core(mark, core_type='standard'):
    """Create a warp core of specified mark and type"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    type_names = {
        'standard': 'Matter-Antimatter Warp Core',
        'overcharged': 'Overcharged Warp Core',
        'efficient': 'Efficient Warp Core'
    }
    name = f"{type_names.get(core_type, 'Warp Core')} Mk {mark_names[mark]}"
    return WarpCoreEquipment(name, mark, core_type, upgrade_space_cost=10)


def create_deflector(mark):
    """Create a deflector dish of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Deflector Dish Mk {mark_names[mark]}"
    return DeflectorEquipment(name, mark, upgrade_space_cost=7)


def create_warp_engine(mark):
    """Create warp engines of specified mark"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    name = f"Warp Drive Mk {mark_names[mark]}"
    return WarpEngineEquipment(name, mark, upgrade_space_cost=8)


def create_armor_plating(mark, armor_type='ablative'):
    """Create armor plating of specified mark and type"""
    mark_names = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    type_names = {
        'ablative': 'Ablative Armor',
        'neutronium': 'Neutronium Armor',
        'polarized': 'Polarized Hull Plating'
    }
    name = f"{type_names.get(armor_type, 'Armor')} Mk {mark_names[mark]}"
    return ArmorEquipment(name, mark, armor_type, upgrade_space_cost=6)


# Equipment availability by mark level
EQUIPMENT_MARK_REQUIREMENTS = {
    1: 0,   # Mk I - Starting equipment
    2: 0,   # Mk II - Available from start
    3: 1,   # Mk III - Requires rank 1
    4: 1,   # Mk IV - Requires rank 1
    5: 2,   # Mk V - Requires rank 2
    6: 2,   # Mk VI - Requires rank 2
    7: 3,   # Mk VII - Requires rank 3
    8: 3,   # Mk VIII - Requires rank 3
    9: 4,   # Mk IX - Requires rank 4
    10: 4,  # Mk X - Requires rank 4
    11: 5,  # Mk XI - Requires rank 5
    12: 6,  # Mk XII - Requires rank 6
    13: 7,  # Mk XIII - Requires rank 7
    14: 7,  # Mk XIV - Requires rank 7
    15: 8,  # Mk XV - Requires rank 8 (max)
}


def get_available_equipment_marks(player_rank):
    """Get maximum equipment mark available at player's rank"""
    max_mark = 1
    for mark, required_rank in EQUIPMENT_MARK_REQUIREMENTS.items():
        if player_rank >= required_rank:
            max_mark = mark
    return max_mark


def calculate_equipment_cost(mark, equipment_type):
    """Calculate dilithium cost for equipment purchase"""
    base_costs = {
        'weapon': 100,
        'shield': 150,
        'impulse_engine': 120,
        'warp_core': 200,
        'deflector': 100,
        'warp_engine': 180,
        'armor': 130
    }
    
    base_cost = base_costs.get(equipment_type, 100)
    # Cost increases exponentially with mark
    return int(base_cost * (1.5 ** (mark - 1)))
