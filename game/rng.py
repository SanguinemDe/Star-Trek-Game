"""
Central Random Number Generator System
Provides deterministic, replayable RNG for combat, loot, and events
"""
import random
import time
import logging


class GameRNG:
    """
    Central RNG system with seed management for deterministic replays.
    
    Usage:
        # Create with seed for deterministic behavior
        rng = GameRNG(seed=12345)
        
        # Or let it auto-generate seed
        rng = GameRNG()
        
        # Use for combat
        hit = rng.roll_hit(0.85)
        damage = rng.roll_damage(10, 50)
        
        # Save seed for replay
        seed = rng.get_seed()
    """
    
    def __init__(self, seed=None):
        """
        Initialize RNG system.
        
        Args:
            seed: Optional seed for deterministic behavior.
                  If None, generates seed from current time.
        """
        if seed is None:
            seed = int(time.time() * 1000) % (2**31)
        
        self.seed = seed
        self.rng = random.Random(seed)
        
        logging.info(f"GameRNG initialized with seed: {seed}")
    
    def get_seed(self):
        """Get current seed for replay purposes"""
        return self.seed
    
    def reseed(self, new_seed):
        """
        Reset RNG with new seed.
        Useful for loading saved games or starting new combat.
        """
        self.seed = new_seed
        self.rng = random.Random(new_seed)
        logging.info(f"GameRNG reseeded: {new_seed}")
    
    # ═══════════════════════════════════════════════════════════════════
    # COMBAT ROLLS
    # ═══════════════════════════════════════════════════════════════════
    
    def roll_hit(self, accuracy):
        """
        Roll to determine if a weapon hits.
        
        Args:
            accuracy: Hit chance as float (0.0 to 1.0)
            
        Returns:
            bool: True if hit, False if miss
        """
        return self.rng.random() < accuracy
    
    def roll_damage(self, min_damage, max_damage):
        """
        Roll damage within a range.
        
        Args:
            min_damage: Minimum damage (inclusive)
            max_damage: Maximum damage (inclusive)
            
        Returns:
            int: Damage dealt
        """
        return self.rng.randint(min_damage, max_damage)
    
    def roll_critical(self, crit_chance):
        """
        Roll for critical hit.
        
        Args:
            crit_chance: Critical chance as float (0.0 to 1.0)
            
        Returns:
            bool: True if critical hit
        """
        return self.rng.random() < crit_chance
    
    def roll_shield_facing(self, facings):
        """
        Randomly select which shield facing is hit.
        
        Args:
            facings: List of facing names ['fore', 'aft', 'port', 'starboard']
            
        Returns:
            str: Selected facing
        """
        return self.rng.choice(facings)
    
    def roll_initiative(self, base_value, dice_size=20):
        """
        Roll initiative for combat turn order.
        
        Args:
            base_value: Base initiative bonus
            dice_size: Size of die to roll (default d20)
            
        Returns:
            int: Total initiative (base + roll)
        """
        roll = self.rng.randint(1, dice_size)
        return base_value + roll
    
    # ═══════════════════════════════════════════════════════════════════
    # LOOT & REWARDS
    # ═══════════════════════════════════════════════════════════════════
    
    def roll_loot_quantity(self, min_items, max_items):
        """Roll number of loot items to drop"""
        return self.rng.randint(min_items, max_items)
    
    def roll_loot_quality(self, rarities):
        """
        Roll loot quality/rarity.
        
        Args:
            rarities: Dict of {quality: weight}, e.g. {'common': 0.7, 'rare': 0.25, 'epic': 0.05}
            
        Returns:
            str: Selected quality
        """
        return self.rng.choices(
            population=list(rarities.keys()),
            weights=list(rarities.values()),
            k=1
        )[0]
    
    def roll_credits(self, min_credits, max_credits):
        """Roll credit reward amount"""
        return self.rng.randint(min_credits, max_credits)
    
    # ═══════════════════════════════════════════════════════════════════
    # EXPLORATION & EVENTS
    # ═══════════════════════════════════════════════════════════════════
    
    def roll_encounter(self, encounter_chance):
        """
        Roll for random encounter.
        
        Args:
            encounter_chance: Chance as float (0.0 to 1.0)
            
        Returns:
            bool: True if encounter occurs
        """
        return self.rng.random() < encounter_chance
    
    def roll_sensor_detection(self, detection_chance):
        """Roll for sensor detection success"""
        return self.rng.random() < detection_chance
    
    def choose_random_event(self, events):
        """
        Choose random event from list.
        
        Args:
            events: List of possible events
            
        Returns:
            Selected event
        """
        return self.rng.choice(events)
    
    def choose_weighted_event(self, events, weights):
        """
        Choose event with weighted probability.
        
        Args:
            events: List of events
            weights: List of weights (same length as events)
            
        Returns:
            Selected event
        """
        return self.rng.choices(events, weights=weights, k=1)[0]
    
    # ═══════════════════════════════════════════════════════════════════
    # GENERIC UTILITIES
    # ═══════════════════════════════════════════════════════════════════
    
    def roll_d20(self):
        """Roll a d20"""
        return self.rng.randint(1, 20)
    
    def roll_d100(self):
        """Roll a d100 (percentile)"""
        return self.rng.randint(1, 100)
    
    def roll_dice(self, num_dice, die_size):
        """
        Roll multiple dice and sum.
        
        Args:
            num_dice: Number of dice to roll
            die_size: Size of each die
            
        Returns:
            int: Sum of all dice
        """
        return sum(self.rng.randint(1, die_size) for _ in range(num_dice))
    
    def random_float(self, min_val=0.0, max_val=1.0):
        """Random float in range"""
        return self.rng.uniform(min_val, max_val)
    
    def random_int(self, min_val, max_val):
        """Random integer in range (inclusive)"""
        return self.rng.randint(min_val, max_val)
    
    def shuffle(self, items):
        """
        Shuffle list in place.
        
        Args:
            items: List to shuffle
        """
        self.rng.shuffle(items)
    
    def chance(self, probability):
        """
        Simple probability check.
        
        Args:
            probability: Chance as float (0.0 to 1.0)
            
        Returns:
            bool: True if chance succeeds
        """
        return self.rng.random() < probability


# Global RNG instance (can be imported directly)
game_rng = GameRNG()


# Example usage
if __name__ == "__main__":
    # Test with specific seed for reproducibility
    rng = GameRNG(seed=42)
    
    print("=== Combat Tests ===")
    print(f"Hit roll (85% accuracy): {rng.roll_hit(0.85)}")
    print(f"Damage roll (10-50): {rng.roll_damage(10, 50)}")
    print(f"Critical hit (15% chance): {rng.roll_critical(0.15)}")
    print(f"Initiative (base 5): {rng.roll_initiative(5)}")
    
    print("\n=== Loot Tests ===")
    rarities = {'common': 0.7, 'rare': 0.25, 'epic': 0.05}
    print(f"Loot quality: {rng.roll_loot_quality(rarities)}")
    print(f"Credits: {rng.roll_credits(100, 1000)}")
    
    print("\n=== Utility Tests ===")
    print(f"d20 roll: {rng.roll_d20()}")
    print(f"d100 roll: {rng.roll_d100()}")
    print(f"3d6 roll: {rng.roll_dice(3, 6)}")
    
    print(f"\nSeed used: {rng.get_seed()}")
