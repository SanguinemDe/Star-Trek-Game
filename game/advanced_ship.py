"""
Advanced Ship System for Star Trek Game
Detailed ship mechanics including systems, crew, power management, and combat
Based on comprehensive design document
"""
import random
from .rng import game_rng


class AdvancedShip:
    """
    Detailed starship with all systems and crew
    This is the new comprehensive ship system
    """
    
    def __init__(self, name, registry, ship_class, ship_type, era_year):
        # ═══════════════════════════════════════════════════════════════════
        # BASIC INFORMATION
        # ═══════════════════════════════════════════════════════════════════
        self.name = name
        self.registry = registry
        self.ship_class = ship_class  # Miranda, Galaxy, etc.
        self.ship_type = ship_type  # Frigate, Cruiser, etc.
        self.era_year = era_year
        self.reputation_cost = 0  # Set by ship template
        self.minimum_rank = 0  # Set by ship template
        self.size = "Medium"  # Small, Medium, Large, Very Large, Huge
        self.cargo_space = 100  # Cargo capacity
        self.upgrade_space = 100  # Space for upgrades
        self.upgrade_space_used = 0
        self.dilithium = 1000  # Dilithium crystals for warp travel
        self.location = "Sol"  # Current star system
        self.provisions = 100  # Food and supplies
        
        # ═══════════════════════════════════════════════════════════════════
        # EQUIPMENT SLOTS (Mk I-XV Upgrades)
        # ═══════════════════════════════════════════════════════════════════
        self.equipped_items = {
            'shields': None,         # Shield Array (Mk I-XV)
            'impulse_engine': None,  # Impulse Engine (Mk I-XV)
            'warp_core': None,       # Warp Core (Mk I-XV)
            'warp_engine': None,     # Warp Drive (Mk I-XV)
            'deflector': None,       # Deflector Dish (Mk I-XV)
            'armor': None,           # Armor Plating (Mk I-XV)
            'weapons': [],           # List of weapon upgrades (Mk I-XV)
            'torpedoes': []          # List of torpedo launcher upgrades (Mk I-XV)
        }
        
        # ═══════════════════════════════════════════════════════════════════
        # NAVIGATION
        # ═══════════════════════════════════════════════════════════════════
        self.sensor_range = 5  # Hexes
        self.turn_speed = 2  # Hexes before turn (0=instant, higher=slower)
        self.impulse_speed = 5  # Combat movement
        self.warp_speed = 6.0  # Warp factor for travel
        
        # ═══════════════════════════════════════════════════════════════════
        # OFFENSE
        # ═══════════════════════════════════════════════════════════════════
        self.weapon_arrays = []  # List of WeaponArray objects
        self.torpedo_bays = []  # List of TorpedoBay objects
        self.special_weapons = []  # List of special weapons
        
        # ═══════════════════════════════════════════════════════════════════
        # DEFENSES
        # ═══════════════════════════════════════════════════════════════════
        self.max_hull = 1000
        self.hull = 1000
        self.armor = 50  # Damage reduction
        self.shields = {
            'fore': 500,
            'aft': 500,
            'port': 500,
            'starboard': 500
        }
        self.max_shields = {
            'fore': 500,
            'aft': 500,
            'port': 500,
            'starboard': 500
        }
        
        # Torpedo damage mechanics (adjustable at top of file)
        self.torpedo_shield_block = 0.90  # 90% blocked by shields
        self.torpedo_bypass = 0.10  # 10% always bleeds through
        self.torpedo_shield_cost = 0.20  # 20% deducted from shield meter
        
        # ═══════════════════════════════════════════════════════════════════
        # POWER ALLOCATION
        # ═══════════════════════════════════════════════════════════════════
        self.warp_core_max_power = 300  # Total power available
        self.power_distribution = {
            'engines': 100,
            'shields': 100,
            'weapons': 100
        }
        
        # ═══════════════════════════════════════════════════════════════════
        # SYSTEMS (Health Measured from 0-100)
        # ═══════════════════════════════════════════════════════════════════
        self.systems = {
            'warp_core': 100,
            'life_support': 100,
            'warp_engines': 100,
            'impulse_engines': 100,
            'weapons': 100,
            'sensors': 100,
            'shields': 100,
            'engineering': 100,
            'sick_bay': 100
        }
        
        # System repair limits (field repairs)
        # <25% can only repair to 25%, <50% can only repair to 50%
        # Need starbase for full repairs
        
        # ═══════════════════════════════════════════════════════════════════
        # CREW
        # ═══════════════════════════════════════════════════════════════════
        self.max_crew = 200
        self.crew_count = 200
        self.crew_skill = "Regular"  # Cadet, Green, Regular, Veteran, Elite, Legendary
        self.crew_morale = 100  # 0-100, affects performance
        
        # Crew skill bonuses:
        # Cadet: +0%, Green: +5%, Regular: +10%, Veteran: +15%, Elite: +20%, Legendary: +25%
        
        # ═══════════════════════════════════════════════════════════════════
        # COMMAND CREW (These are where Legendary Officers are Born)
        # ═══════════════════════════════════════════════════════════════════
        self.command_crew = {
            'captain': None,      # Player character
            'tactical': None,     # Weapons & shields
            'medical': None,      # Crew survival
            'engineer': None,     # Repairs & warp core
            'conn': None,         # Piloting & navigation
            'science': None       # Sensors & analysis
        }
        
        # ═══════════════════════════════════════════════════════════════════
        # COMBAT STATE
        # ═══════════════════════════════════════════════════════════════════
        self.facing = 0  # 0-5 hex facing
        self.position = (0, 0)  # Hex coordinates
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPATIBILITY PROPERTIES (for UI and legacy code)
    # ═══════════════════════════════════════════════════════════════════
    
    @property
    def type(self):
        """Alias for ship_type"""
        return self.ship_type
    
    @property
    def era(self):
        """Return era string from era_year"""
        if self.era_year < 2270:
            return "22nd Century"
        elif self.era_year < 2340:
            return "23rd Century"
        elif self.era_year < 2400:
            return "24th Century"
        else:
            return "25th Century"
    
    @property
    def crew_skill_level(self):
        """Alias for crew_skill"""
        return self.crew_skill
    
    # System health properties (for UI compatibility)
    @property
    def warp_core(self):
        return self.systems['warp_core']
    
    @property
    def life_support(self):
        return self.systems['life_support']
    
    @property
    def warp_engines(self):
        return self.systems['warp_engines']
    
    @property
    def impulse_engines(self):
        return self.systems['impulse_engines']
    
    @property
    def weapons_system(self):
        return self.systems['weapons']
    
    @property
    def sensors_system(self):
        return self.systems['sensors']
    
    @property
    def shields_system(self):
        return self.systems['shields']
    
    @property
    def engineering_system(self):
        return self.systems['engineering']
    
    @property
    def sick_bay(self):
        return self.systems['sick_bay']
        
    # ═══════════════════════════════════════════════════════════════════
    # CREW METHODS
    # ═══════════════════════════════════════════════════════════════════
    
    def get_crew_bonus(self, station=None):
        """
        Get crew skill bonus percentage
        If station is provided, get bonus for that specific officer station
        Otherwise return general crew skill bonus
        """
        bonuses = {
            'Cadet': 0.0,
            'Green': 0.05,
            'Regular': 0.10,
            'Veteran': 0.15,
            'Elite': 0.20,
            'Legendary': 0.25
        }
        
        base_bonus = bonuses.get(self.crew_skill, 0.0)
        
        # If requesting specific station bonus, check command crew
        if station and station in self.command_crew:
            officer = self.command_crew[station]
            if officer:
                # Officer provides additional bonus (CommandOfficer class would have a bonus attribute)
                # For now, just return base bonus
                return base_bonus * 100  # Return as percentage for compatibility
            else:
                return base_bonus * 100
        
        return base_bonus
    
    def train_crew(self):
        """Train crew to next skill level (costs reputation)"""
        levels = ['Cadet', 'Green', 'Regular', 'Veteran', 'Elite']
        current_index = levels.index(self.crew_skill) if self.crew_skill in levels else -1
        
        if current_index < len(levels) - 1:
            self.crew_skill = levels[current_index + 1]
            return True
        return False  # Can't train to Legendary, must earn it
    
    def check_crew_skill_degradation(self):
        """
        Check if crew skill drops due to casualties
        For every 25% of crew killed, skill level drops 1 level
        """
        crew_percentage = self.crew_count / self.max_crew
        
        skill_levels = ['Cadet', 'Green', 'Regular', 'Veteran', 'Elite', 'Legendary']
        current_index = skill_levels.index(self.crew_skill)
        
        # Determine how many levels to drop based on crew losses
        if crew_percentage >= 0.75:
            return  # No degradation
        elif crew_percentage >= 0.50:
            drop_levels = 1
        elif crew_percentage >= 0.25:
            drop_levels = 2
        else:
            drop_levels = 3
        
        new_index = max(0, current_index - drop_levels)
        self.crew_skill = skill_levels[new_index]
    
    def regenerate_crew(self, stardates_passed):
        """
        Slowly regenerate crew over time (medical bay recovery, transfers, etc.)
        Returns number of crew recovered
        """
        if self.crew_count >= self.max_crew:
            return 0
        
        # Recovery rate based on sick bay health
        sick_bay_efficiency = self.systems['sick_bay'] / 100.0
        recovery_rate = 1.0 * sick_bay_efficiency  # 1 crew per stardate at full efficiency
        
        crew_recovered = int(stardates_passed * recovery_rate)
        crew_recovered = min(crew_recovered, self.max_crew - self.crew_count)
        
        if crew_recovered > 0:
            self.crew_count += crew_recovered
            
        return crew_recovered
    
    def process_life_support_damage(self):
        """
        Process ongoing crew loss from damaged life support
        Returns number of casualties this turn
        """
        if self.systems['life_support'] >= 75:
            return 0  # Life support sufficient
        
        # Chance of casualties based on life support status
        life_support_status = self.systems['life_support']
        
        if life_support_status < 25:
            casualty_chance = 0.5  # 50% chance per day
            max_casualties = 5
        elif life_support_status < 50:
            casualty_chance = 0.2  # 20% chance per day
            max_casualties = 3
        else:  # 50-74%
            casualty_chance = 0.05  # 5% chance per day
            max_casualties = 1
        
        if game_rng.roll_critical(casualty_chance):
            casualties = game_rng.roll_damage(1, max_casualties)
            casualties = min(casualties, self.crew_count - 1)  # Never kill everyone
            self.crew_count -= casualties
            
            # Check for skill degradation
            self.check_crew_skill_degradation()
            
            return casualties
        
        return 0
    
    # ═══════════════════════════════════════════════════════════════════
    # SYSTEM EFFICIENCY & DAMAGE CASCADES
    # ═══════════════════════════════════════════════════════════════════
    
    def get_system_efficiency(self, system_name):
        """
        Get system efficiency (0.0 to 1.0+) including crew bonus and cascades
        
        Damage Cascades:
        - Warp Core: Reduces all other systems if damaged
        - Life Support: Reduces Weapons, Sensors, Engineering if damaged
        - Sensors: Reduces weapon accuracy if damaged
        """
        base_efficiency = self.systems[system_name] / 100.0
        crew_bonus = self.get_crew_bonus()
        
        # Apply damage cascades
        if system_name != 'warp_core':
            # Warp core damage affects everything
            warp_core_efficiency = self.systems['warp_core'] / 100.0
            base_efficiency *= warp_core_efficiency
        
        if system_name in ['weapons', 'sensors', 'engineering']:
            # Life support affects these systems
            life_support_efficiency = self.systems['life_support'] / 100.0
            base_efficiency *= life_support_efficiency
        
        # Apply crew bonus
        return min(2.0, base_efficiency * (1.0 + crew_bonus))  # Cap at 200%
    
    def get_system_penalties(self):
        """
        Get performance penalties from damaged systems
        Returns dict of multipliers (1.0 = normal, <1.0 = reduced performance)
        """
        penalties = {
            'weapons_damage': 1.0,
            'weapons_accuracy': 1.0,
            'warp_speed': 1.0,
            'impulse_speed': 1.0,
            'shield_recharge': 1.0,
            'sensor_range': 1.0,
            'evasion': 1.0
        }
        
        # Weapons system affects damage and accuracy
        weapons_status = self.systems['weapons'] / 100.0
        penalties['weapons_damage'] *= weapons_status
        penalties['weapons_accuracy'] *= (0.8 + weapons_status * 0.2)  # Min 80% accuracy
        
        # Engines affect speed and evasion
        impulse_status = self.systems['impulse_engines'] / 100.0
        warp_status = self.systems['warp_engines'] / 100.0
        penalties['impulse_speed'] *= impulse_status
        penalties['warp_speed'] *= warp_status
        penalties['evasion'] *= (0.5 + impulse_status * 0.5)  # Min 50% evasion
        
        # Shields system affects recharge rate
        shields_status = self.systems['shields'] / 100.0
        penalties['shield_recharge'] *= shields_status
        
        # Sensors affect range and targeting
        sensors_status = self.systems['sensors'] / 100.0
        penalties['sensor_range'] *= sensors_status
        penalties['weapons_accuracy'] *= (0.8 + sensors_status * 0.2)  # Min 80% accuracy
        
        # Apply crew skill bonus to all systems
        crew_bonus = 1.0 + self.get_crew_bonus()
        for key in penalties:
            penalties[key] *= crew_bonus
            penalties[key] = min(2.0, penalties[key])  # Cap at 200%
        
        return penalties
    
    # ═══════════════════════════════════════════════════════════════════
    # POWER MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def get_available_power(self):
        """Get total power available based on warp core health"""
        warp_core_efficiency = self.systems['warp_core'] / 100.0
        return int(self.warp_core_max_power * warp_core_efficiency)
    
    def redistribute_power(self, engines, shields, weapons):
        """
        Redistribute power between systems (must total to available power)
        Adding power to one system takes it away from the other 2
        Each system is capped at 200 power maximum.
        
        When shield power is reduced, current shields scale down proportionally
        to prevent exploiting the system (charging shields then moving power away).
        """
        available = self.get_available_power()
        total = engines + shields + weapons
        
        # Cap each system at 200 power maximum
        engines = min(engines, 200)
        shields = min(shields, 200)
        weapons = min(weapons, 200)
        
        # Recalculate total after capping
        total = engines + shields + weapons
        
        if total <= available:
            # Calculate old and new shield bonuses to scale current shields
            old_shield_bonus = self.get_shield_power_bonus()
            
            # Update power distribution
            self.power_distribution['engines'] = engines
            self.power_distribution['shields'] = shields
            self.power_distribution['weapons'] = weapons
            
            # Calculate new shield bonus
            new_shield_bonus = self.get_shield_power_bonus()
            
            # Scale current shields proportionally if shield power changed
            if old_shield_bonus != new_shield_bonus and old_shield_bonus > 0:
                scale_factor = new_shield_bonus / old_shield_bonus
                
                # Apply scaling to all shield arcs (current shields only, not max)
                import math
                for arc in self.shields:
                    self.shields[arc] = math.ceil(self.shields[arc] * scale_factor)
                    # Don't exceed new max shields
                    self.shields[arc] = min(self.shields[arc], self.get_max_shields_for_arc(arc))
            
            return True
        return False
    
    # ========================================================================
    # POWER MANAGEMENT - SCALING BONUSES
    # ========================================================================
    
    def get_engine_power_bonus(self):
        """
        Calculate movement bonus based on engine power allocation (graduated bonus)
        
        GRADUATED BONUS SYSTEM:
        - 100 power = 0 bonus (balanced allocation baseline)
        - 200 power = max bonus (full allocation)
        - Scales linearly between 100 and 200
        
        Max bonuses by ship size:
        - Small/Medium/Large ships: 0 → +1 → +2 → +3 (graduated)
        - Very Large/Huge ships: 0 → +1 → +2 (graduated)
        
        Example: Odyssey (Huge) with 5 base MP
        - 100 power = 5 MP (+0 bonus)
        - 150 power = 6 MP (+1 bonus, 50% of max)
        - 200 power = 7 MP (+2 bonus, 100% of max)
        
        Example: Miranda (Medium) with 6 base MP
        - 100 power = 6 MP (+0 bonus)
        - 133 power = 7 MP (+1 bonus, 33% of max)
        - 167 power = 8 MP (+2 bonus, 67% of max)
        - 200 power = 9 MP (+3 bonus, 100% of max)
        
        Returns:
            float: Bonus movement points to add (0 to max_bonus)
        """
        engine_power = self.power_distribution['engines']
        
        # Determine max bonus based on ship size
        if self.size in ["Small", "Medium", "Large"]:
            max_bonus = 3.0
        elif self.size in ["Very Large", "Huge"]:
            max_bonus = 2.0
        else:
            max_bonus = 0.0
        
        # Graduated scaling from 100 (0 bonus) to 200 (max bonus)
        if engine_power <= 100:
            return 0.0
        
        power_above_balanced = engine_power - 100
        percentage = power_above_balanced / 100.0  # 0.0 to 1.0
        
        return max_bonus * percentage
    
    def get_shield_power_bonus(self):
        """
        Calculate shield bonus based on shield power allocation (sliding scale)
        
        SLIDING SCALE SYSTEM:
        - 0 power = 1.0x shields (no allocation)
        - 100 power = 1.0x shields (balanced allocation)
        - 200 power = 1.5x shields (full allocation, +50% max)
        
        This affects both shield capacity and regeneration rate.
        When power is reduced, current shields scale down proportionally.
        
        Example: Ship with 1000 base max shields
        - 0 power = 1000 shields (1.0x, 0% bonus)
        - 100 power = 1000 shields (1.0x, 0% bonus, balanced)
        - 150 power = 1250 shields (1.25x, 50% of max bonus)
        - 200 power = 1500 shields (1.5x, 100% of max bonus)
        
        Returns:
            float: Multiplier for shields (1.0 to 1.5)
        """
        shield_power = self.power_distribution['shields']
        
        # Calculate percentage above balanced (100 power)
        # 100 power = 0% → 1.0x (no bonus)
        # 150 power = 50% → 1.25x (half bonus)
        # 200 power = 100% → 1.5x (full bonus)
        if shield_power <= 100:
            return 1.0
        
        power_above_balanced = shield_power - 100
        percentage = power_above_balanced / 100.0  # 0.0 to 1.0
        
        # Max bonus is +50% (1.0 baseline + 0.5 max bonus)
        return 1.0 + (0.5 * percentage)
    
    def get_weapon_power_bonus(self):
        """
        Calculate weapon damage bonus based on weapon power allocation (sliding scale)
        
        SLIDING SCALE SYSTEM (ARRAYS ONLY, not torpedoes):
        - 0 power = 1.0x damage (no allocation)
        - 100 power = 1.0x damage (balanced allocation)
        - 200 power = 1.5x damage (full allocation, +50% max)
        
        This prevents one-shotting while making arrays more effective.
        Torpedoes remain high-risk/high-reward (unaffected by power).
        
        Example: Yorktown phaser doing 35 base damage
        - 0 power = 35 damage (1.0x, 0% bonus)
        - 100 power = 35 damage (1.0x, 0% bonus, balanced)
        - 150 power = 43.75 damage (1.25x, 50% of max bonus)
        - 200 power = 52.5 damage (1.5x, 100% of max bonus)
        - Photon torpedo: ALWAYS full damage (not affected)
        
        Returns:
            float: Multiplier for array damage (1.0 to 1.5)
        """
        weapon_power = self.power_distribution['weapons']
        
        # Calculate percentage above balanced (100 power)
        # 100 power = 0% → 1.0x (no bonus)
        # 150 power = 50% → 1.25x (half bonus)
        # 200 power = 100% → 1.5x (full bonus)
        if weapon_power <= 100:
            return 1.0
        
        power_above_balanced = weapon_power - 100
        percentage = power_above_balanced / 100.0  # 0.0 to 1.0
        
        # Max bonus is +50% (1.0 baseline + 0.5 max bonus)
        return 1.0 + (0.5 * percentage)
    
    def get_current_movement_points(self):
        """
        Calculate actual movement points with power bonus applied
        
        Returns:
            int: Movement points for this turn (base + power bonus, rounded up)
        """
        import math
        base_mp = self.impulse_speed
        bonus_mp = self.get_engine_power_bonus()
        return math.ceil(base_mp + bonus_mp)
    
    def get_max_shields_for_arc(self, arc):
        """
        Calculate max shields for an arc with power bonus applied
        
        Args:
            arc: Shield arc ('fore', 'aft', 'port', 'starboard')
        
        Returns:
            int: Max shield value for this arc with power bonus (rounded up)
        """
        import math
        base_max = self.max_shields[arc]
        shield_bonus = self.get_shield_power_bonus()
        return math.ceil(base_max * shield_bonus)
    
    # ═══════════════════════════════════════════════════════════════════
    # DAMAGE & COMBAT
    # ═══════════════════════════════════════════════════════════════════
    
    def take_damage(self, damage, arc, damage_type='energy'):
        """
        Apply damage to ship
        
        Args:
            damage: Amount of damage
            arc: 'fore', 'aft', 'port', 'starboard'
            damage_type: 'energy', 'torpedo', 'special'
        
        Returns:
            dict with damage results
        """
        if damage_type == 'torpedo':
            # Torpedo mechanics: 90% blocked, 10% bypass, 20% shield cost
            shield_blocked = damage * self.torpedo_shield_block
            bypass_damage = damage * self.torpedo_bypass
            shield_cost = damage * self.torpedo_shield_cost
            
            if self.shields[arc] > 0:
                # Shield absorbs some damage
                actual_shield_damage = min(shield_cost, self.shields[arc])
                self.shields[arc] -= actual_shield_damage
                
                # Apply bypass damage to hull (reduced by armor)
                hull_damage = bypass_damage * (1.0 - self.armor / 100.0)
            else:
                # Shields down, full torpedo damage to hull (reduced by armor)
                hull_damage = damage * (1.0 - self.armor / 100.0)
            
            # Ensure hull damage is never negative
            hull_damage = max(0, hull_damage)
        else:
            # Energy weapons: shields block all until depleted
            if self.shields[arc] > 0:
                shield_damage = min(damage, self.shields[arc])
                self.shields[arc] -= shield_damage
                remaining_damage = max(0, damage - shield_damage)  # Ensure non-negative
            else:
                remaining_damage = damage
            
            # Apply remaining damage to hull (reduced by armor)
            if remaining_damage > 0:
                armor_reduction = self.armor / 100.0
                hull_damage = remaining_damage * (1.0 - armor_reduction)
            else:
                hull_damage = 0
            
            # Ensure hull damage is never negative
            hull_damage = max(0, hull_damage)
        
        # Apply hull damage
        if hull_damage > 0:
            self.hull -= hull_damage
            
            # Calculate crew casualties
            casualties = self.calculate_casualties(hull_damage)
            self.crew_count = max(0, self.crew_count - casualties)
            
            # Check for skill level drop (every 25% crew lost)
            self.check_crew_skill_degradation()
            
            # Random system damage (returns list of damaged systems)
            damaged_systems = self.apply_system_damage(hull_damage)
        else:
            casualties = 0
            damaged_systems = []
        
        # Check for hull failure or warp core breach
        if self.hull <= 0:
            self.hull = 0
            from .logger import get_logger
            logger = get_logger(__name__)
            logger.warning(f"{self.name}: HULL INTEGRITY FAILURE - Ship disabled!")
            
            # Catastrophic hull failure causes massive casualties (50% base)
            hull_failure_casualties = self.calculate_hull_failure_casualties()
            total_casualties = casualties + hull_failure_casualties
            
            logger.warning(f"{self.name}: Hull failure casualties: {hull_failure_casualties} crew lost")
            
            # Hull at 0 = disabled but not destroyed (unless warp core breaches)
            breach_result = self.check_warp_core_breach()
            
            return {
                'destroyed': breach_result['ship_destroyed'],  # Only true if warp core breached
                'disabled': not breach_result['ship_destroyed'],  # True if just hull failure
                'warp_core_breach': breach_result['breach'],
                'breach_survived': breach_result['survived'],
                'hull_damage': hull_damage,
                'casualties': total_casualties + breach_result['casualties'],
                'system_damage': damaged_systems
            }
        
        # Check for warp core breach even if hull > 0 (system damage could destroy warp core)
        if self.systems['warp_core'] <= 0:
            from .logger import get_logger
            logger = get_logger(__name__)
            breach_result = self.check_warp_core_breach()
            
            return {
                'destroyed': breach_result['ship_destroyed'],
                'disabled': False,
                'warp_core_breach': breach_result['breach'],
                'breach_survived': breach_result['survived'],
                'hull_damage': hull_damage,
                'casualties': casualties + breach_result['casualties'],
                'system_damage': damaged_systems
            }
        
        return {
            'destroyed': False,
            'disabled': False,
            'warp_core_breach': False,
            'hull_damage': hull_damage,
            'casualties': casualties,
            'system_damage': damaged_systems
        }
    
    def calculate_casualties(self, hull_damage):
        """
        Calculate crew casualties from hull damage
        Mitigated by life support, sick bay, and medical officer
        """
        # Base casualty rate
        casualty_rate = hull_damage / self.max_hull * 0.1  # 10% of damage ratio
        
        # Mitigate with life support
        life_support_efficiency = self.get_system_efficiency('life_support')
        casualty_rate *= (1.0 - life_support_efficiency * 0.5)
        
        # Mitigate with sick bay
        sick_bay_efficiency = self.get_system_efficiency('sick_bay')
        casualty_rate *= (1.0 - sick_bay_efficiency * 0.3)
        
        # Mitigate with medical officer
        if self.command_crew['medical']:
            medical_bonus = self.command_crew['medical'].get_skill_bonus()
            casualty_rate *= (1.0 - medical_bonus * 0.2)
        
        casualties = int(self.max_crew * casualty_rate)
        return max(0, casualties)
    
    def calculate_hull_failure_casualties(self):
        """
        Calculate crew casualties when hull reaches 0%
        Catastrophic structural failure - ship disabled but salvageable
        Base 50% casualty rate, mitigated by systems and crew
        """
        import math
        
        # Base catastrophic casualty rate: 50% of crew
        base_casualty_rate = 0.50
        
        # Mitigate with life support - keeps crew areas pressurized
        life_support_efficiency = self.get_system_efficiency('life_support')
        casualty_rate = base_casualty_rate * (1.0 - life_support_efficiency * 0.4)  # Up to 40% reduction
        
        # Mitigate with sick bay - treat injured crew
        sick_bay_efficiency = self.get_system_efficiency('sick_bay')
        casualty_rate *= (1.0 - sick_bay_efficiency * 0.3)  # Up to 30% reduction
        
        # Mitigate with medical officer skill
        if self.command_crew['medical']:
            medical_bonus = self.command_crew['medical'].get_skill_bonus()
            casualty_rate *= (1.0 - medical_bonus * 0.2)  # Up to 20% reduction
        
        # Calculate final casualties
        casualties = math.ceil(self.crew_count * casualty_rate)
        
        from .logger import get_logger
        logger = get_logger(__name__)
        logger.info(f"{self.name}: Hull failure casualty calculation:")
        logger.info(f"  Base rate: {base_casualty_rate*100:.1f}%")
        logger.info(f"  Life support mitigation: {life_support_efficiency*100:.1f}%")
        logger.info(f"  Sick bay mitigation: {sick_bay_efficiency*100:.1f}%")
        if self.command_crew['medical']:
            logger.info(f"  Medical officer bonus: {medical_bonus*100:.1f}%")
        logger.info(f"  Final rate: {casualty_rate*100:.1f}%")
        logger.info(f"  Casualties: {casualties} of {self.crew_count} crew")
        
        return max(0, min(casualties, self.crew_count))  # Can't exceed crew count
    
    def apply_system_damage(self, hull_damage):
        """
        Apply damage to internal systems based on hull damage severity
        
        Damage Model:
        - Hull integrity affects damage chance and severity
        - Critical systems (warp core, life support) have lower damage chance but higher consequences
        - Damage cascades from critical systems to others
        - Warp core at 0 = catastrophic breach (big boom)
        - Hull at 0 = ship disabled but not destroyed (unless warp core breach)
        
        Damage Probability increases with hull damage:
        - 0-25% hull: Low chance of system damage
        - 25-50% hull: Moderate chance, minor damage
        - 50-75% hull: High chance, moderate damage
        - 75-100% hull: Very high chance, severe damage
        """
        from .logger import get_logger
        logger = get_logger(__name__)
        
        # Calculate hull integrity percentage
        hull_integrity = self.hull / self.max_hull
        damage_ratio = hull_damage / self.max_hull
        
        # Base chance increases as hull integrity decreases
        if hull_integrity > 0.75:
            base_chance = damage_ratio * 0.15  # 15% at high integrity
            damage_severity = (0.05, 0.10)  # 5-10% system damage
        elif hull_integrity > 0.50:
            base_chance = damage_ratio * 0.30  # 30% at moderate integrity
            damage_severity = (0.08, 0.15)  # 8-15% system damage
        elif hull_integrity > 0.25:
            base_chance = damage_ratio * 0.50  # 50% at low integrity
            damage_severity = (0.12, 0.25)  # 12-25% system damage
        else:
            base_chance = damage_ratio * 0.75  # 75% at critical integrity
            damage_severity = (0.20, 0.40)  # 20-40% system damage (severe)
        
        # System damage priorities (chance multipliers)
        # Critical systems less likely to take direct damage, but consequences are worse
        system_vulnerability = {
            'warp_core': 0.4,        # Protected, but critical if damaged
            'life_support': 0.5,     # Somewhat protected
            'shields': 1.2,          # More exposed (emitters on hull)
            'weapons': 1.0,          # Standard vulnerability
            'impulse_engines': 0.8,  # Somewhat protected
            'warp_drive': 0.6,       # Well protected
            'sensors': 1.1,          # Exposed arrays
            'engineering': 0.7,      # Interior systems
            'sick_bay': 0.9,         # Interior but vulnerable
            'auxiliary_systems': 1.0 # Standard
        }
        
        damaged_systems = []
        
        for system_name, vulnerability in system_vulnerability.items():
            if system_name not in self.systems:
                continue
                
            # Skip if system already destroyed
            if self.systems[system_name] <= 0:
                continue
            
            # Calculate damage chance for this system
            system_chance = base_chance * vulnerability
            
            if game_rng.roll_critical(system_chance):
                # Calculate damage amount
                current_health = self.systems[system_name]
                min_dmg = int(current_health * damage_severity[0])
                max_dmg = int(current_health * damage_severity[1])
                
                system_damage = game_rng.roll_damage(max(1, min_dmg), max(1, max_dmg))
                old_health = self.systems[system_name]
                self.systems[system_name] = max(0, self.systems[system_name] - system_damage)
                new_health = self.systems[system_name]
                
                damaged_systems.append({
                    'system': system_name,
                    'damage': system_damage,
                    'old_health': old_health,
                    'new_health': new_health,
                    'destroyed': new_health == 0
                })
                
                logger.info(f"{self.name}: {system_name} damaged! {old_health:.1f}% -> {new_health:.1f}%")
                
                # Check for critical system failure
                if new_health == 0:
                    logger.warning(f"{self.name}: {system_name} DESTROYED!")
                    self._handle_system_destroyed(system_name)
        
        return damaged_systems
    
    def _handle_system_destroyed(self, system_name):
        """Handle consequences of system destruction"""
        from .logger import get_logger
        logger = get_logger(__name__)
        
        if system_name == 'warp_core':
            logger.critical(f"{self.name}: WARP CORE BREACH IMMINENT!")
            # Don't trigger breach here, wait for check_warp_core_breach()
            
        elif system_name == 'life_support':
            logger.warning(f"{self.name}: Life support failed! Crew efficiency severely reduced!")
            # Crew casualties increase over time without life support
            
        elif system_name == 'impulse_engines':
            logger.warning(f"{self.name}: Impulse engines offline! Ship mobility compromised!")
            
        elif system_name == 'warp_drive':
            logger.warning(f"{self.name}: Warp drive offline! Cannot achieve warp speed!")
            
        elif system_name == 'shields':
            logger.warning(f"{self.name}: Shield generators destroyed! No shield regeneration!")
            
        elif system_name == 'weapons':
            logger.warning(f"{self.name}: Weapon systems destroyed! Cannot fire weapons!")
            
        elif system_name == 'sensors':
            logger.warning(f"{self.name}: Sensors destroyed! Targeting severely degraded!")
    
    def check_warp_core_breach(self):
        """
        Check if warp core breach occurs when warp core reaches 0%
        
        Warp Core Breach = GUARANTEED SHIP DESTRUCTION
        - Warp core at 0% = immediate catastrophic breach
        - Ship ALWAYS completely destroyed (no salvage, total loss)
        - Small chance crew can evacuate to escape pods before explosion
        - Engineer skill can slightly improve crew evacuation odds
        
        Hull reaching 0 = Ship disabled but intact (can be salvaged/repaired at starbase)
        Warp core reaching 0 = Ship lost forever, crew evacuation possible
        
        Returns:
            dict with breach status and crew survival result
        """
        from .logger import get_logger
        logger = get_logger(__name__)
        
        if self.systems['warp_core'] <= 0:
            logger.critical(f"{self.name}: *** CATASTROPHIC WARP CORE BREACH ***")
            
            # Base crew evacuation chance is very low (10%)
            base_survival = 0.10
            
            # Engineer can improve evacuation odds slightly
            if self.command_crew['engineer']:
                engineer_bonus = self.command_crew['engineer'].get_skill_bonus()
                # Engineer adds up to 20% evacuation chance (max 30% total)
                survival_chance = min(0.30, base_survival + (engineer_bonus * 0.20))
                logger.info(f"Engineer {self.command_crew['engineer'].name} attempting emergency evacuation...")
            else:
                survival_chance = base_survival
            
            # Roll for crew evacuation
            crew_evacuated = game_rng.roll_critical(survival_chance)
            
            if crew_evacuated:
                logger.warning(f"{self.name}: SHIP DESTROYED - Crew evacuated to escape pods! ({int(survival_chance * 100)}% made it out)")
                casualties = 0  # Crew survived
            else:
                logger.critical(f"{self.name}: SHIP DESTROYED - All hands lost with the ship!")
                casualties = self.crew_count  # Total crew loss
            
            return {
                'breach': True,
                'survived': crew_evacuated,  # Did crew escape?
                'survival_chance': survival_chance,
                'casualties': casualties,
                'ship_destroyed': True  # Ship ALWAYS destroyed
            }
        
        return {
            'breach': False,
            'survived': True,
            'survival_chance': 1.0,
            'casualties': 0,
            'ship_destroyed': False
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # REPAIRS
    # ═══════════════════════════════════════════════════════════════════
    
    def repair_system(self, system_name, repair_amount):
        """
        Repair a system (with field repair limits)
        
        Field Repair Limits:
        - <25% health: Can only repair to 25%
        - <50% health: Can only repair to 50%
        - Need starbase for full repairs beyond these limits
        """
        current_health = self.systems[system_name]
        
        # Field repair limits
        if current_health < 25:
            max_field_repair = 25
        elif current_health < 50:
            max_field_repair = 50
        else:
            max_field_repair = 100
        
        # Engineering efficiency affects repair speed
        engineering_efficiency = self.get_system_efficiency('engineering')
        actual_repair = repair_amount * engineering_efficiency
        
        # Engineer officer bonus
        if self.command_crew['engineer']:
            engineer_bonus = self.command_crew['engineer'].get_skill_bonus()
            actual_repair *= (1.0 + engineer_bonus)
        
        new_health = min(max_field_repair, current_health + actual_repair)
        self.systems[system_name] = new_health
        
        return new_health
    
    def starbase_repair(self, system_name):
        """Full repair at starbase (no limits)"""
        self.systems[system_name] = 100
        return 100
    
    def regenerate_shields(self, amount_per_arc):
        """
        Regenerate shields based on power allocation and system health
        
        Power bonus affects both regeneration rate AND shield capacity.
        This allows tactical decisions: high shield power for tankiness,
        or low shield power for offensive/speed builds.
        """
        import math
        shield_efficiency = self.get_system_efficiency('shields')
        shield_power_bonus = self.get_shield_power_bonus()
        
        regen_rate = amount_per_arc * shield_efficiency * shield_power_bonus
        
        for arc in self.shields:
            # Use power-modified max shields
            max_for_arc = self.get_max_shields_for_arc(arc)
            new_shield_value = self.shields[arc] + regen_rate
            self.shields[arc] = min(max_for_arc, math.ceil(new_shield_value))
    
    # ═══════════════════════════════════════════════════════════════════
    # WEAPONS
    # ═══════════════════════════════════════════════════════════════════
    
    def fire_weapons(self, target, arc):
        """
        Fire all weapons in an arc at a target
        
        Args:
            target: Target ship
            arc: Firing arc ('fore', 'aft', 'port', 'starboard')
        
        Returns:
            list of damage dealt
        """
        weapons_efficiency = self.get_system_efficiency('weapons')
        sensors_efficiency = self.get_system_efficiency('sensors')
        weapon_power_bonus = self.get_weapon_power_bonus()  # New: proper scaling
        crew_bonus = self.get_crew_bonus()
        
        # Tactical officer bonus
        tactical_bonus = 0.0
        if self.command_crew['tactical']:
            tactical_bonus = self.command_crew['tactical'].get_skill_bonus()
        
        damage_dealt = []
        
        # Fire energy weapons in arc
        for weapon in self.weapon_arrays:
            if arc in weapon.firing_arcs:
                # Calculate hit chance (sensors affect accuracy)
                hit_chance = 0.85 * sensors_efficiency * (1.0 + tactical_bonus * 0.3)
                
                if game_rng.roll_hit(hit_chance):
                    # Calculate damage with proper power scaling (rounded up)
                    import math
                    base_damage = weapon.base_damage
                    damage = base_damage * weapons_efficiency * weapon_power_bonus
                    damage *= (1.0 + crew_bonus + tactical_bonus * 0.5)
                    damage = math.ceil(damage)
                    
                    damage_dealt.append({
                        'type': 'energy',
                        'weapon': weapon.weapon_type,
                        'damage': damage
                    })
        
        # Fire torpedoes (NOTE: weapon_power_bonus NOT applied - torpedoes always full damage)
        for torp_bay in self.torpedo_bays:
            if arc in torp_bay.firing_arcs and torp_bay.torpedoes > 0:
                hit_chance = 0.75 * sensors_efficiency * (1.0 + tactical_bonus * 0.3)
                
                if game_rng.roll_hit(hit_chance):
                    import math
                    base_damage = torp_bay.base_damage
                    damage = base_damage * weapons_efficiency
                    damage *= (1.0 + tactical_bonus * 0.5)
                    damage = math.ceil(damage)
                    
                    torp_bay.torpedoes -= 1
                    
                    damage_dealt.append({
                        'type': 'torpedo',
                        'weapon': torp_bay.torpedo_type,
                        'damage': damage
                    })
        
        return damage_dealt
    
    # ═══════════════════════════════════════════════════════════════════
    # STATUS
    # ═══════════════════════════════════════════════════════════════════
    
    def get_ship_status(self):
        """Get comprehensive ship status"""
        return {
            'name': self.name,
            'registry': self.registry,
            'class': self.ship_class,
            'type': self.ship_type,
            'hull': f"{int(self.hull)}/{self.max_hull}",
            'hull_percent': self.hull / self.max_hull * 100,
            'shields': {arc: int(val) for arc, val in self.shields.items()},
            'crew': f"{self.crew_count}/{self.max_crew}",
            'crew_skill': self.crew_skill,
            'systems': {k: int(v) for k, v in self.systems.items()},
            'power': self.power_distribution,
            'available_power': self.get_available_power()
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # EQUIPMENT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def install_equipment(self, equipment_item):
        """
        Install equipment upgrade on ship
        
        Args:
            equipment_item: Equipment object from game.equipment
            
        Returns:
            True if successful, False if not enough upgrade space
        """
        # Check if we have enough upgrade space
        if self.upgrade_space_used + equipment_item.upgrade_space_cost > self.upgrade_space:
            return False
        
        equipment_type = equipment_item.equipment_type
        
        # Uninstall old equipment of this type first
        if equipment_type in ['shields', 'impulse_engine', 'warp_core', 'warp_engine', 'deflector', 'armor']:
            old_equipment = self.equipped_items[equipment_type]
            if old_equipment:
                self.upgrade_space_used -= old_equipment.upgrade_space_cost
            self.equipped_items[equipment_type] = equipment_item
        elif equipment_type == 'weapon':
            self.equipped_items['weapons'].append(equipment_item)
        elif equipment_type in ['photon', 'quantum']:
            self.equipped_items['torpedoes'].append(equipment_item)
        
        self.upgrade_space_used += equipment_item.upgrade_space_cost
        return True
    
    def uninstall_equipment(self, equipment_type, index=0):
        """
        Remove equipment from ship
        
        Args:
            equipment_type: Type of equipment to remove
            index: For weapons/torpedoes, which one to remove
            
        Returns:
            Removed equipment item or None
        """
        if equipment_type in ['shields', 'impulse_engine', 'warp_core', 'warp_engine', 'deflector', 'armor']:
            old_equipment = self.equipped_items[equipment_type]
            if old_equipment:
                self.upgrade_space_used -= old_equipment.upgrade_space_cost
                self.equipped_items[equipment_type] = None
                return old_equipment
        elif equipment_type == 'weapons' and index < len(self.equipped_items['weapons']):
            old_equipment = self.equipped_items['weapons'].pop(index)
            self.upgrade_space_used -= old_equipment.upgrade_space_cost
            return old_equipment
        elif equipment_type == 'torpedoes' and index < len(self.equipped_items['torpedoes']):
            old_equipment = self.equipped_items['torpedoes'].pop(index)
            self.upgrade_space_used -= old_equipment.upgrade_space_cost
            return old_equipment
        
        return None
    
    def get_equipment_bonuses(self):
        """
        Calculate all equipment bonuses applied to ship stats
        
        Returns:
            dict of absolute bonus values (not multipliers)
        """
        bonuses = {
            'shield_capacity': 0,      # Absolute shield points
            'shield_regeneration': 0,  # Regen points per turn
            'hull': 0,                 # Absolute hull points
            'armor': 0,                # Absolute armor value
            'warp_core_power': 0,      # Absolute power increase
            'impulse_speed': 0,        # Hexes per turn
            'turn_rate': 0,            # Turn cost reduction
            'warp_speed': 0.0,         # Warp factor increase
            'sensor_range': 0,         # Hex range increase
            'weapon_damage': 0,        # Not used - weapons have individual marks
            'weapon_accuracy': 0       # Accuracy percentage
        }
        
        # Shield equipment
        if self.equipped_items['shields']:
            shield_eq = self.equipped_items['shields']
            bonuses['shield_capacity'] = shield_eq.get_capacity_bonus()
            bonuses['shield_regeneration'] = shield_eq.get_regeneration_bonus()
            bonuses['armor'] += shield_eq.get_damage_reduction()
        
        # Impulse engine
        if self.equipped_items['impulse_engine']:
            impulse_eq = self.equipped_items['impulse_engine']
            bonuses['impulse_speed'] = impulse_eq.get_speed_bonus()
            bonuses['turn_rate'] = impulse_eq.get_turn_rate_bonus()
        
        # Warp core
        if self.equipped_items['warp_core']:
            core_eq = self.equipped_items['warp_core']
            bonuses['warp_core_power'] = core_eq.get_power_bonus()
        
        # Deflector
        if self.equipped_items['deflector']:
            deflector_eq = self.equipped_items['deflector']
            bonuses['sensor_range'] = deflector_eq.get_sensor_range_bonus()
        
        # Warp engine
        if self.equipped_items['warp_engine']:
            warp_eq = self.equipped_items['warp_engine']
            bonuses['warp_speed'] = warp_eq.get_warp_speed_bonus()
        
        # Armor
        if self.equipped_items['armor']:
            armor_eq = self.equipped_items['armor']
            bonuses['armor'] += armor_eq.get_armor_bonus()
            bonuses['hull'] = armor_eq.get_hull_bonus()
        
        # Note: Weapon damage comes from WeaponArray.get_damage() which already factors in mark
        # Accuracy bonus from equipment is cumulative
        if self.equipped_items['weapons']:
            total_accuracy = 0
            for weapon_eq in self.equipped_items['weapons']:
                total_accuracy += weapon_eq.get_accuracy_bonus()
            bonuses['weapon_accuracy'] = total_accuracy / len(self.equipped_items['weapons'])
        
        return bonuses
    
    def get_total_stats(self):
        """Get ship's total stats including equipment bonuses"""
        bonuses = self.get_equipment_bonuses()
        
        return {
            'hull': self.max_hull + bonuses['hull'],
            'armor': self.armor + bonuses['armor'],
            'shields': {arc: val + bonuses['shield_capacity'] for arc, val in self.max_shields.items()},
            'impulse_speed': self.impulse_speed + bonuses['impulse_speed'],
            'warp_speed': self.warp_speed + bonuses['warp_speed'],
            'sensor_range': self.sensor_range + bonuses['sensor_range'],
            'power': self.warp_core_max_power + bonuses['warp_core_power']
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # WEAPON FIRE RATE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def advance_all_weapon_cooldowns(self):
        """Advance cooldowns for all weapons by 1 turn (call at end of combat turn)"""
        for weapon in self.weapon_arrays:
            weapon.advance_cooldown()
        for torpedo in self.torpedo_bays:
            torpedo.advance_cooldown()
        for special in self.special_weapons:
            if hasattr(special, 'advance_cooldown'):
                special.advance_cooldown()
    
    def get_ready_weapons(self):
        """Get list of all weapons ready to fire"""
        ready = []
        
        # Energy weapons
        for i, weapon in enumerate(self.weapon_arrays):
            if weapon.can_fire():
                ready.append(('array', i, weapon))
        
        # Torpedoes
        for i, torpedo in enumerate(self.torpedo_bays):
            if torpedo.can_fire():
                ready.append(('torpedo', i, torpedo))
        
        # Special weapons
        for i, special in enumerate(self.special_weapons):
            if hasattr(special, 'can_fire') and special.can_fire():
                ready.append(('special', i, special))
        
        return ready
    
    def get_weapon_status(self):
        """Get status of all weapons for display"""
        status = {
            'energy_weapons': [],
            'torpedoes': [],
            'special_weapons': []
        }
        
        for weapon in self.weapon_arrays:
            status['energy_weapons'].append({
                'type': weapon.weapon_type,
                'mark': weapon.mark,
                'damage': weapon.get_damage(),
                'arcs': weapon.firing_arcs,
                'ready': weapon.can_fire(),
                'cooldown': weapon.cooldown_remaining
            })
        
        for torpedo in self.torpedo_bays:
            status['torpedoes'].append({
                'type': torpedo.torpedo_type,
                'mark': torpedo.mark,
                'damage': torpedo.get_damage(),
                'arcs': torpedo.firing_arcs,
                'torpedoes': torpedo.torpedoes,
                'max_torpedoes': torpedo.max_torpedoes,
                'ready': torpedo.can_fire(),
                'cooldown': torpedo.cooldown_remaining,
                'base_cooldown': torpedo.get_base_cooldown()
            })
        
        return status
    
    # ═══════════════════════════════════════════════════════════════════
    # SENSOR & TARGETING SYSTEM
    # ═══════════════════════════════════════════════════════════════════
    
    def get_effective_sensor_range(self):
        """
        Get effective sensor range including equipment bonuses
        
        Returns:
            Sensor range in hexes
        """
        bonuses = self.get_equipment_bonuses()
        base_range = self.sensor_range
        
        # Add deflector bonuses
        bonus_range = bonuses.get('sensor_range', 0)
        
        # System damage reduces sensor range
        sensor_efficiency = self.get_system_efficiency('sensors')
        
        effective_range = (base_range + bonus_range) * sensor_efficiency
        return max(1, int(effective_range))  # Minimum 1 hex
    
    def get_targeting_accuracy(self, distance_in_hexes):
        """
        Calculate targeting accuracy modifier based on distance and sensor range
        
        Args:
            distance_in_hexes: Distance to target in hexes
        
        Returns:
            Accuracy modifier as a multiplier (0.0 to 2.0+)
            Returns None if target is beyond maximum range (2x sensors)
        
        Accuracy Breakdown:
        - Point Blank (0-3 hex): +50% accuracy (1.5x)
        - Close Range (4-5 hex): +25% accuracy (1.25x)
        - Medium Range (6-8 hex): 0% modifier (1.0x)
        - Long Range (9-11 hex): -25% accuracy (0.75x)
        - Extreme Range (12-13 hex): -40% accuracy (0.6x)
        - Beyond 13 hexes: Out of range for most weapons
        
        Weapon Max Ranges:
        - Phasers: 12 hexes maximum
        - Torpedoes: 15 hexes maximum
        """
        sensor_range = self.get_effective_sensor_range()
        
        # Point blank range (0-3 hex)
        if distance_in_hexes <= 3:
            return 1.50  # +50% accuracy
        
        # Close range (4-5 hex)
        if distance_in_hexes <= 5:
            return 1.25  # +25% accuracy
        
        # Medium range (6-8 hex)
        if distance_in_hexes <= 8:
            return 1.0  # No modifier
        
        # Long range (9-11 hex)
        if distance_in_hexes <= 11:
            return 0.75  # -25% accuracy
        
        # Extreme range (12-13 hex)
        if distance_in_hexes <= 13:
            return 0.60  # -40% accuracy
        
        # Beyond effective range
        return None  # Out of range
    
    def can_target(self, distance_in_hexes):
        """
        Check if target is within maximum targeting range
        
        Args:
            distance_in_hexes: Distance to target
        
        Returns:
            True if target can be engaged, False otherwise
        """
        # Maximum effective range is 13 hexes
        return distance_in_hexes <= 13
    
    def get_range_description(self, distance_in_hexes):
        """
        Get descriptive range band for distance
        
        Args:
            distance_in_hexes: Distance to target
        
        Returns:
            String describing range band and accuracy
        """
        accuracy = self.get_targeting_accuracy(distance_in_hexes)
        
        if accuracy is None:
            return "OUT OF RANGE (Cannot Target)"
        
        if distance_in_hexes <= 3:
            return f"POINT BLANK (+50% accuracy)"
        elif distance_in_hexes <= 5:
            return f"CLOSE RANGE (+25% accuracy)"
        elif distance_in_hexes <= 8:
            return f"MEDIUM RANGE (optimal)"
        elif distance_in_hexes <= 11:
            return f"LONG RANGE (-25% accuracy)"
        elif distance_in_hexes <= 13:
            return f"EXTREME RANGE (-40% accuracy)"
        else:
            return "OUT OF RANGE (Cannot Target)"
    
    def get_target_arc(self, target_hex_q, target_hex_r):
        """
        Calculate which firing arc the target is in based on hex coordinates
        
        Hex facing system:
        - facing 0 = East (right) = FORE
        - facing 1 = Southeast = FORE/STARBOARD
        - facing 2 = Southwest = AFT/STARBOARD  
        - facing 3 = West (left) = AFT
        - facing 4 = Northwest = AFT/PORT
        - facing 5 = Northeast = FORE/PORT
        
        Args:
            target_hex_q: Target's q coordinate
            target_hex_r: Target's r coordinate
            
        Returns:
            Primary arc string: 'fore', 'aft', 'port', or 'starboard'
        """
        import math
        
        # Calculate angle to target
        dq = target_hex_q - self.hex_q
        dr = target_hex_r - self.hex_r
        
        # Convert axial to cube coordinates for angle calculation
        dx = dq
        dy = -dq - dr
        dz = dr
        
        # Calculate angle in degrees (0 = East, counterclockwise)
        angle_to_target = math.degrees(math.atan2(dz, dx)) % 360
        
        # Ship's facing angle (each facing = 60 degrees)
        ship_facing_angle = (self.facing * 60) % 360
        
        # Relative angle (0 = directly ahead)
        relative_angle = (angle_to_target - ship_facing_angle + 360) % 360
        
        # Determine arc based on relative angle
        # Fore: -45 to +45 degrees (315-45)
        # Starboard: 45 to 135 degrees
        # Aft: 135 to 225 degrees
        # Port: 225 to 315 degrees
        
        if relative_angle <= 45 or relative_angle >= 315:
            return 'fore'
        elif 45 < relative_angle <= 135:
            return 'starboard'
        elif 135 < relative_angle <= 225:
            return 'aft'
        else:  # 225 < relative_angle < 315
            return 'port'
    
    def get_shield_facing_hit(self, attacker_hex_q, attacker_hex_r):
        """
        Calculate which of THIS ship's shield facings is being hit from an attacker's position
        
        Args:
            attacker_hex_q: Attacker's q coordinate
            attacker_hex_r: Attacker's r coordinate
            
        Returns:
            Shield facing string: 'fore', 'aft', 'port', or 'starboard'
        """
        import math
        
        # Calculate angle from THIS ship to the attacker
        dq = attacker_hex_q - self.hex_q
        dr = attacker_hex_r - self.hex_r
        
        # Convert axial to cube coordinates for angle calculation
        dx = dq
        dy = -dq - dr
        dz = dr
        
        # Calculate angle in degrees (0 = East, counterclockwise)
        angle_to_attacker = math.degrees(math.atan2(dz, dx)) % 360
        
        # Ship's facing angle (each facing = 60 degrees)
        ship_facing_angle = (self.facing * 60) % 360
        
        # Relative angle (0 = directly ahead)
        relative_angle = (angle_to_attacker - ship_facing_angle + 360) % 360
        
        # Determine which shield facing is being hit
        # Fore shields face forward (ship's front)
        # If attacker is in front, fore shields get hit
        if relative_angle <= 45 or relative_angle >= 315:
            return 'fore'
        elif 45 < relative_angle <= 135:
            return 'starboard'
        elif 135 < relative_angle <= 225:
            return 'aft'
        else:  # 225 < relative_angle < 315
            return 'port'
    
    def get_occupied_hexes(self, hex_grid=None):
        """
        Get list of all hexes occupied by this ship based on its size
        
        Args:
            hex_grid: HexGrid object (optional, only needed if you need neighbor calculation)
        
        Returns:
            List of (q, r) tuples for all hexes this ship occupies
            
        Size mapping:
            Small, Medium, Large = 1 hex (center only)
            Very Large, Huge = 7 hexes (center + 6 neighbors)
        """
        # Single hex ships
        if self.size in ["Small", "Medium", "Large"]:
            return [(self.hex_q, self.hex_r)]
        
        # Multi-hex ships (Very Large, Huge)
        elif self.size in ["Very Large", "Huge"]:
            occupied = [(self.hex_q, self.hex_r)]  # Center hex
            
            # Add 6 surrounding hexes
            # Axial direction vectors for 6 neighbors
            directions = [
                (+1, 0), (+1, -1), (0, -1),
                (-1, 0), (-1, +1), (0, +1)
            ]
            for dq, dr in directions:
                occupied.append((self.hex_q + dq, self.hex_r + dr))
            
            return occupied
        
        # Default to single hex
        return [(self.hex_q, self.hex_r)]
    
    def is_multi_hex(self):
        """
        Check if this ship occupies multiple hexes on the grid
        
        Returns:
            bool: True if ship is Very Large or Huge (occupies 7 hexes),
                  False if Small/Medium/Large (occupies 1 hex)
        """
        return self.size in ["Very Large", "Huge"]
    
    # ========================================================================
    # COLLISION DETECTION SYSTEM
    # ========================================================================
    
    def would_collide_at(self, new_q, new_r, all_ships):
        """
        Multi-Hex Collision Detection
        
        Checks if moving this ship to a new position would cause it to overlap
        with any other ship. For multi-hex ships (Very Large/Huge), ALL 7 hexes
        are checked against ALL hexes of other ships.
        
        This is the authoritative collision detection method - all movement systems
        should call this before executing a move.
        
        ALGORITHM:
        ----------
        1. Temporarily calculate what hexes this ship would occupy at new position
        2. For each hex we would occupy:
           3. For each other ship in combat:
              4. Get all hexes that ship occupies
              5. Check for overlap
              6. If overlap found, return collision details
        7. If no overlaps found, movement is legal
        
        SHIP SIZES:
        -----------
        - Small/Medium/Large: 1 hex (center only)
        - Very Large/Huge: 7 hexes (center + 6 neighbors)
        
        Args:
            new_q (int): Target Q coordinate (center hex for multi-hex ships)
            new_r (int): Target R coordinate (center hex for multi-hex ships)
            all_ships (list): All ships currently in combat (including self)
            
        Returns:
            tuple: (would_collide, blocking_ship, colliding_hexes)
                - would_collide (bool): True if movement would cause collision
                - blocking_ship (Ship or None): The ship blocking movement
                - colliding_hexes (list): List of (q,r) tuples where collision occurs
        
        Example Usage:
            >>> ship = enterprise  # Huge ship at (5, 3)
            >>> would_collide, blocker, hexes = ship.would_collide_at(6, 3, all_ships)
            >>> if would_collide:
            >>>     print(f"Can't move! {blocker.name} is blocking at {hexes}")
            >>> else:
            >>>     # Safe to move
            >>>     ship.hex_q, ship.hex_r = 6, 3
        """
        # Temporarily calculate what hexes we would occupy at new position
        old_q, old_r = self.hex_q, self.hex_r
        self.hex_q = new_q
        self.hex_r = new_r
        would_occupy = self.get_occupied_hexes()
        self.hex_q = old_q
        self.hex_r = old_r
        
        # Check each hex against all other ships
        for test_hex_q, test_hex_r in would_occupy:
            for other_ship in all_ships:
                # Skip self and destroyed ships
                if other_ship == self or other_ship.hull <= 0:
                    continue
                
                # Get other ship's occupied hexes
                other_hexes = other_ship.get_occupied_hexes()
                
                # Check for overlap
                if (test_hex_q, test_hex_r) in other_hexes:
                    return (True, other_ship, [(test_hex_q, test_hex_r)])
        
        return (False, None, [])
    
    def can_move_to(self, new_q, new_r, all_ships):
        """
        Simplified Collision Check (Boolean Result)
        
        Convenience wrapper around would_collide_at() that returns a simple
        boolean answer. Use this when you only need to know if a move is legal,
        without needing details about what's blocking it.
        
        Args:
            new_q (int): Target Q coordinate
            new_r (int): Target R coordinate
            all_ships (list): All ships in combat
            
        Returns:
            bool: True if movement is legal (no collision)
                  False if movement would cause collision
        
        Example Usage:
            >>> if ship.can_move_to(new_q, new_r, all_ships):
            >>>     ship.hex_q, ship.hex_r = new_q, new_r
            >>>     print("Moved successfully!")
            >>> else:
            >>>     print("Movement blocked!")
        """
        would_collide, _, _ = self.would_collide_at(new_q, new_r, all_ships)
        return not would_collide


class WeaponArray:
    """Energy weapon array (phasers, disruptors, etc)"""
    
    def __init__(self, weapon_type, mark, firing_arcs, upgrade_space_cost=5):
        self.weapon_type = weapon_type  # 'phaser', 'disruptor', etc.
        self.mark = mark  # Mk I-XV
        self.firing_arcs = firing_arcs  # List: ['fore', 'port', etc]
        self.upgrade_space_cost = upgrade_space_cost  # Space used in ship
        self.cooldown_remaining = 0  # Turns until can fire again (0 = ready)
        
    def get_damage(self):
        """Calculate damage based on weapon type and mark"""
        # Base damage per weapon type at Mk I
        base_damages = {
            'phaser': 15,
            'disruptor': 18,
            'plasma': 20,
            'polaron': 16,
            'tetryon': 14
        }
        base = base_damages.get(self.weapon_type, 15)
        # Each mark adds +5 damage
        return base + (self.mark - 1) * 5
    
    def get_cooldown_time(self):
        """
        Get base cooldown time for this weapon type
        Energy weapons fire every turn (cooldown = 0)
        """
        return 0  # Energy weapons always ready
    
    def can_fire(self):
        """Check if weapon is ready to fire"""
        return self.cooldown_remaining <= 0
    
    def fire(self, crew_skill_bonus=0.0):
        """
        Fire the weapon and set cooldown
        
        Args:
            crew_skill_bonus: Crew skill bonus (0.0 to 0.25 for Cadet to Legendary)
        
        Returns:
            Damage dealt, or 0 if on cooldown
        """
        if not self.can_fire():
            return 0
        
        # Energy weapons have no cooldown, fire immediately
        self.cooldown_remaining = self.get_cooldown_time()
        return self.get_damage()
    
    def advance_cooldown(self):
        """Advance cooldown by 1 turn"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
    
    def get_visual_effect_type(self):
        """
        Get the visual effect type for this weapon.
        Used by GUI to determine which beam/effect sprites to use.
        
        Returns:
            String identifier for visual effect ('phaser_beam', 'disruptor_beam', etc.)
        """
        # Map weapon types to their visual effects
        effect_map = {
            'phaser': 'phaser_beam',
            'disruptor': 'disruptor_beam',  # Future: different colored beam
            'plasma': 'plasma_beam',        # Future: green beam
            'polaron': 'polaron_beam',      # Future: purple beam
            'tetryon': 'tetryon_beam'       # Future: blue beam
        }
        return effect_map.get(self.weapon_type, 'phaser_beam')
    
    def get_beam_color(self):
        """
        Get the color tint for this weapon's beam.
        Used by GUI for simple colored beams when custom sprites not available.
        
        Returns:
            RGB tuple (r, g, b)
        """
        color_map = {
            'phaser': (255, 150, 50),      # Orange
            'disruptor': (50, 255, 50),    # Green
            'plasma': (100, 255, 100),     # Light green
            'polaron': (150, 50, 255),     # Purple
            'tetryon': (50, 150, 255)      # Blue
        }
        return color_map.get(self.weapon_type, (255, 150, 50))


class TorpedoBay:
    """Torpedo launcher"""
    
    def __init__(self, torpedo_type, mark, firing_arcs, max_torpedoes=100, upgrade_space_cost=10):
        self.torpedo_type = torpedo_type  # 'photon', 'quantum', etc.
        self.mark = mark  # Mk I-XV
        self.firing_arcs = firing_arcs
        self.torpedoes = max_torpedoes
        self.max_torpedoes = max_torpedoes
        self.upgrade_space_cost = upgrade_space_cost
        self.cooldown_remaining = 0  # Turns until can fire again (0 = ready)
        
    def get_damage(self):
        """Calculate torpedo damage based on type and mark"""
        # Base damage per torpedo type at Mk I
        base_damages = {
            'photon': 80,
            'quantum': 100,
            'plasma': 90,
            'tricobalt': 120
        }
        base = base_damages.get(self.torpedo_type, 80)
        # Each mark adds +10 damage
        return base + (self.mark - 1) * 10
    
    def get_base_cooldown(self):
        """
        Get base cooldown time for this torpedo type (in turns)
        Higher marks reduce cooldown slightly
        """
        # Base cooldown per torpedo type
        base_cooldowns = {
            'photon': 3,      # Standard torpedoes: 3 turn cooldown
            'quantum': 4,     # More powerful: 4 turn cooldown
            'plasma': 3,      # Similar to photon
            'tricobalt': 5    # Very powerful: 5 turn cooldown
        }
        base_cooldown = base_cooldowns.get(self.torpedo_type, 3)
        
        # Higher marks reduce cooldown (max 1 turn reduction at Mk XV)
        mark_reduction = min(1, self.mark // 5)  # -1 turn at Mk V, X, XV
        
        return max(2, base_cooldown - mark_reduction)  # Minimum 2 turn cooldown
    
    def get_cooldown_with_crew(self, crew_skill_bonus=0.0):
        """
        Get cooldown time modified by crew skill
        
        Args:
            crew_skill_bonus: Crew skill bonus (0.0 to 0.25)
                - Cadet: 0.0 (no reduction)
                - Green: 0.05 (5% faster)
                - Regular: 0.10 (10% faster)
                - Veteran: 0.15 (15% faster)
                - Elite: 0.20 (20% faster)
                - Legendary: 0.25 (25% faster)
        
        Returns:
            Cooldown in turns (minimum 1)
        """
        base = self.get_base_cooldown()
        # Crew skill reduces cooldown time
        modified = base * (1.0 - crew_skill_bonus)
        return max(1, int(round(modified)))  # Minimum 1 turn cooldown
    
    def can_fire(self):
        """Check if torpedo bay is ready to fire"""
        return self.cooldown_remaining <= 0 and self.torpedoes > 0
    
    def fire(self, crew_skill_bonus=0.0):
        """
        Fire a torpedo and set cooldown
        
        Args:
            crew_skill_bonus: Crew skill bonus (0.0 to 0.25)
        
        Returns:
            Damage dealt, or 0 if on cooldown or out of torpedoes
        """
        if not self.can_fire():
            return 0
        
        # Fire torpedo
        self.torpedoes -= 1
        damage = self.get_damage()
        
        # Set cooldown based on crew skill
        self.cooldown_remaining = self.get_cooldown_with_crew(crew_skill_bonus)
        
        return damage
    
    def advance_cooldown(self):
        """Advance cooldown by 1 turn"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
    
    def reload(self, amount=None):
        """Reload torpedoes (at starbase or with supplies)"""
        if amount is None:
            self.torpedoes = self.max_torpedoes
        else:
            self.torpedoes = min(self.max_torpedoes, self.torpedoes + amount)
    
    def get_visual_effect_type(self):
        """
        Get the visual effect type for this torpedo.
        Used by GUI to determine which projectile sprites to use.
        
        Returns:
            String identifier for visual effect ('photon_torpedo', 'quantum_torpedo', etc.)
        """
        return f"{self.torpedo_type}_torpedo"
    
    def get_projectile_sprite_sheet(self):
        """
        Get the sprite sheet filename for this torpedo type.
        
        Returns:
            Filename of sprite sheet in assets/sfx/torpedoes/
        """
        sprite_map = {
            'photon': 'photon_sheet.png',
            'quantum': 'quantum_sheet.png',
            'plasma': 'plasma_sheet.png',
            'tricobalt': 'tricobalt_sheet.png',
            'tetryon': 'tetryon_sheet.png'
        }
        return sprite_map.get(self.torpedo_type, 'photon_sheet.png')


class CommandOfficer:
    """Command crew officer"""
    
    def __init__(self, name, position, species, skill_level="Regular"):
        self.name = name
        self.position = position  # 'tactical', 'medical', etc.
        self.species = species
        self.skill_level = skill_level  # Cadet -> Legendary
        self.experience = 0
        
    def get_skill_bonus(self):
        """Get officer's skill bonus"""
        bonuses = {
            'Cadet': 0.0,
            'Green': 0.05,
            'Regular': 0.10,
            'Veteran': 0.15,
            'Elite': 0.20,
            'Legendary': 0.25
        }
        return bonuses.get(self.skill_level, 0.0)
    
    def gain_experience(self, xp):
        """Gain experience and potentially level up"""
        self.experience += xp
        
        # Level up thresholds (can't train to Legendary, must earn it)
        levels = ['Cadet', 'Green', 'Regular', 'Veteran', 'Elite', 'Legendary']
        current_index = levels.index(self.skill_level)
        
        xp_required = [0, 100, 300, 600, 1000, 2000]
        
        for i in range(current_index + 1, len(levels)):
            if self.experience >= xp_required[i]:
                self.skill_level = levels[i]
    
    def to_dict(self):
        """Serialize officer to dictionary"""
        return {
            'name': self.name,
            'position': self.position,
            'species': self.species,
            'skill_level': self.skill_level,
            'experience': self.experience
        }
    
    @classmethod
    def from_dict(cls, data):
        """Deserialize officer from dictionary"""
        officer = cls(data['name'], data['position'], data['species'], data['skill_level'])
        officer.experience = data['experience']
        return officer


# Add save/load methods to AdvancedShip
def _add_save_load_methods():
    """Add to_dict and from_dict methods to AdvancedShip"""
    
    def to_dict(self):
        """Serialize ship to dictionary for saving"""
        return {
            # Basic info
            'name': self.name,
            'registry': self.registry,
            'ship_class': self.ship_class,
            'ship_type': self.ship_type,
            'era_year': self.era_year,
            'reputation_cost': self.reputation_cost,
            'minimum_rank': self.minimum_rank,
            'size': self.size,
            'cargo_space': self.cargo_space,
            'upgrade_space': self.upgrade_space,
            'upgrade_space_used': self.upgrade_space_used,
            'dilithium': self.dilithium,
            'location': self.location,
            'provisions': self.provisions,
            
            # Navigation
            'sensor_range': self.sensor_range,
            'turn_speed': self.turn_speed,
            'impulse_speed': self.impulse_speed,
            'warp_speed': self.warp_speed,
            
            # Defenses
            'max_hull': self.max_hull,
            'hull': self.hull,
            'armor': self.armor,
            'shields': self.shields,
            'max_shields': self.max_shields,
            
            # Power
            'warp_core_max_power': self.warp_core_max_power,
            'power_distribution': self.power_distribution,
            
            # Systems
            'systems': self.systems,
            
            # Crew
            'max_crew': self.max_crew,
            'crew_count': self.crew_count,
            'crew_skill': self.crew_skill,
            'crew_morale': self.crew_morale,
            
            # Weapons (serialize WeaponArray objects)
            'weapon_arrays': [
                {
                    'weapon_type': w.weapon_type,
                    'base_damage': w.base_damage,
                    'firing_arcs': w.firing_arcs,
                    'cooldown_remaining': w.cooldown_remaining
                } for w in self.weapon_arrays
            ],
            
            # Torpedoes (serialize TorpedoBay objects)
            'torpedo_bays': [
                {
                    'torpedo_type': t.torpedo_type,
                    'base_damage': t.base_damage,
                    'firing_arcs': t.firing_arcs,
                    'torpedoes': t.torpedoes,
                    'max_torpedoes': t.max_torpedoes,
                    'cooldown_remaining': t.cooldown_remaining,
                    'mark': t.mark
                } for t in self.torpedo_bays
            ],
            
            # Command crew (serialize officers)
            'command_crew': {
                pos: officer.to_dict() if officer else None
                for pos, officer in self.command_crew.items()
            },
            
            # Combat state
            'facing': self.facing,
            'position': self.position
        }
    
    @classmethod
    def from_dict(cls, data):
        """Deserialize ship from dictionary"""
        # Create ship with basic info
        ship = cls(
            data['name'],
            data['registry'],
            data['ship_class'],
            data['ship_type'],
            data['era_year']
        )
        
        # Restore all attributes
        ship.reputation_cost = data['reputation_cost']
        ship.minimum_rank = data['minimum_rank']
        ship.size = data['size']
        ship.cargo_space = data['cargo_space']
        ship.upgrade_space = data['upgrade_space']
        ship.upgrade_space_used = data['upgrade_space_used']
        ship.dilithium = data['dilithium']
        ship.location = data['location']
        ship.provisions = data['provisions']
        
        # Navigation
        ship.sensor_range = data['sensor_range']
        ship.turn_speed = data['turn_speed']
        ship.impulse_speed = data['impulse_speed']
        ship.warp_speed = data['warp_speed']
        
        # Defenses
        ship.max_hull = data['max_hull']
        ship.hull = data['hull']
        ship.armor = data['armor']
        ship.shields = data['shields']
        ship.max_shields = data['max_shields']
        
        # Power
        ship.warp_core_max_power = data['warp_core_max_power']
        ship.power_distribution = data['power_distribution']
        
        # Systems
        ship.systems = data['systems']
        
        # Crew
        ship.max_crew = data['max_crew']
        ship.crew_count = data['crew_count']
        ship.crew_skill = data['crew_skill']
        ship.crew_morale = data['crew_morale']
        
        # Weapons (deserialize WeaponArray objects)
        ship.weapon_arrays = [
            WeaponArray(
                w['weapon_type'],
                w['base_damage'],
                w['firing_arcs']
            ) for w in data['weapon_arrays']
        ]
        # Restore cooldowns
        for i, w_data in enumerate(data['weapon_arrays']):
            ship.weapon_arrays[i].cooldown_remaining = w_data['cooldown_remaining']
        
        # Torpedoes (deserialize TorpedoBay objects)
        ship.torpedo_bays = [
            TorpedoBay(
                t['torpedo_type'],
                t['base_damage'],
                t['firing_arcs'],
                t['max_torpedoes'],
                t['mark']
            ) for t in data['torpedo_bays']
        ]
        # Restore ammo and cooldowns
        for i, t_data in enumerate(data['torpedo_bays']):
            ship.torpedo_bays[i].torpedoes = t_data['torpedoes']
            ship.torpedo_bays[i].cooldown_remaining = t_data['cooldown_remaining']
        
        # Command crew (deserialize officers)
        ship.command_crew = {
            pos: CommandOfficer.from_dict(officer_data) if officer_data else None
            for pos, officer_data in data['command_crew'].items()
        }
        
        # Combat state
        ship.facing = data['facing']
        ship.position = tuple(data['position'])
        
        return ship
    
    # Add methods to AdvancedShip class
    AdvancedShip.to_dict = to_dict
    AdvancedShip.from_dict = from_dict

# Call the function to add the methods
_add_save_load_methods()


# ═══════════════════════════════════════════════════════════════════
# SHIP TEMPLATES
# ═══════════════════════════════════════════════════════════════════

