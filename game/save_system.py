"""
Save/Load System with Dataclasses
Version-aware save file management
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime
import logging


# Current save file version
SAVE_VERSION = 1


@dataclass
class ShipData:
    """Serializable ship data"""
    name: str
    registry: str
    ship_class: str
    hull: int
    max_hull: int
    shields: Dict[str, int]
    max_shields: Dict[str, int]
    position: Optional[tuple] = None  # (hex_q, hex_r)
    facing: int = 0
    
    # Weapon loadout (simplified for now)
    weapon_arrays: List[dict] = field(default_factory=list)
    torpedo_bays: List[dict] = field(default_factory=list)
    
    # Resources
    crew_count: int = 0
    max_crew: int = 0
    cargo: Dict[str, int] = field(default_factory=dict)


@dataclass
class PlayerData:
    """Player character data"""
    name: str
    rank: str
    rank_level: int = 0
    reputation: int = 0
    credits: int = 0
    
    # Statistics
    missions_completed: int = 0
    ships_destroyed: int = 0
    sectors_explored: int = 0


@dataclass
class MissionData:
    """Mission/quest data"""
    mission_id: str
    title: str
    description: str
    status: str  # "active", "completed", "failed"
    objectives: List[str] = field(default_factory=list)
    rewards: Dict[str, int] = field(default_factory=dict)


@dataclass
class GameSaveData:
    """Complete save game data"""
    version: int = SAVE_VERSION
    save_name: str = "Quicksave"
    timestamp: str = ""
    playtime_seconds: int = 0
    
    # Core game data
    player: Optional[PlayerData] = None
    player_ship: Optional[ShipData] = None
    
    # Mission state
    active_missions: List[MissionData] = field(default_factory=list)
    completed_missions: List[str] = field(default_factory=list)  # mission IDs
    
    # Galaxy state
    current_sector: Optional[str] = None
    discovered_sectors: List[str] = field(default_factory=list)
    
    # Inventory
    inventory: Dict[str, int] = field(default_factory=dict)
    
    # Flags and story progress
    story_flags: Dict[str, bool] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set timestamp if not provided"""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class SaveManager:
    """
    Manages save/load operations with versioning.
    
    Usage:
        save_mgr = SaveManager()
        
        # Save game
        save_data = GameSaveData(...)
        save_mgr.save_game(save_data, "slot_1")
        
        # Load game
        loaded = save_mgr.load_game("slot_1")
    """
    
    def __init__(self, save_dir="saves"):
        """
        Initialize save manager.
        
        Args:
            save_dir: Directory to store save files
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"SaveManager initialized: {self.save_dir.absolute()}")
    
    def save_game(self, save_data: GameSaveData, slot_name: str) -> bool:
        """
        Save game to file.
        
        Args:
            save_data: GameSaveData instance
            slot_name: Save slot name (without extension)
            
        Returns:
            bool: True if save successful
        """
        try:
            save_file = self.save_dir / f"{slot_name}.json"
            
            # Convert dataclass to dict
            data_dict = asdict(save_data)
            
            # Write to file with pretty formatting
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Game saved: {save_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save game: {e}")
            return False
    
    def load_game(self, slot_name: str) -> Optional[GameSaveData]:
        """
        Load game from file.
        
        Args:
            slot_name: Save slot name (without extension)
            
        Returns:
            GameSaveData instance or None if load failed
        """
        try:
            save_file = self.save_dir / f"{slot_name}.json"
            
            if not save_file.exists():
                self.logger.warning(f"Save file not found: {save_file}")
                return None
            
            # Read file
            with open(save_file, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            
            # Check version and migrate if needed
            version = data_dict.get('version', 0)
            if version != SAVE_VERSION:
                self.logger.warning(f"Save version mismatch: {version} (current: {SAVE_VERSION})")
                data_dict = self._migrate_save(data_dict, version)
            
            # Reconstruct dataclass
            save_data = self._dict_to_savedata(data_dict)
            
            self.logger.info(f"Game loaded: {save_file}")
            return save_data
            
        except Exception as e:
            self.logger.error(f"Failed to load game: {e}")
            return None
    
    def _dict_to_savedata(self, data_dict: dict) -> GameSaveData:
        """
        Convert dict to GameSaveData with nested dataclasses.
        
        Args:
            data_dict: Dictionary from JSON
            
        Returns:
            GameSaveData instance
        """
        # Convert player data
        player_data = None
        if data_dict.get('player'):
            player_data = PlayerData(**data_dict['player'])
        
        # Convert ship data
        ship_data = None
        if data_dict.get('player_ship'):
            ship_data = ShipData(**data_dict['player_ship'])
        
        # Convert missions
        missions = [
            MissionData(**m) for m in data_dict.get('active_missions', [])
        ]
        
        # Create save data
        return GameSaveData(
            version=data_dict.get('version', SAVE_VERSION),
            save_name=data_dict.get('save_name', 'Unnamed'),
            timestamp=data_dict.get('timestamp', ''),
            playtime_seconds=data_dict.get('playtime_seconds', 0),
            player=player_data,
            player_ship=ship_data,
            active_missions=missions,
            completed_missions=data_dict.get('completed_missions', []),
            current_sector=data_dict.get('current_sector'),
            discovered_sectors=data_dict.get('discovered_sectors', []),
            inventory=data_dict.get('inventory', {}),
            story_flags=data_dict.get('story_flags', {})
        )
    
    def _migrate_save(self, data_dict: dict, from_version: int) -> dict:
        """
        Migrate save file from old version to current.
        
        Args:
            data_dict: Old save data
            from_version: Version of old save
            
        Returns:
            dict: Migrated data
        """
        self.logger.info(f"Migrating save from v{from_version} to v{SAVE_VERSION}")
        
        # Example migration logic
        if from_version < 1:
            # Version 0 -> 1: Add new fields
            data_dict.setdefault('story_flags', {})
            data_dict.setdefault('discovered_sectors', [])
        
        # Update version
        data_dict['version'] = SAVE_VERSION
        
        return data_dict
    
    def list_saves(self) -> List[Dict[str, str]]:
        """
        List all available save files.
        
        Returns:
            List of dicts with save metadata
        """
        saves = []
        
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                saves.append({
                    'slot': save_file.stem,
                    'name': data.get('save_name', 'Unnamed'),
                    'timestamp': data.get('timestamp', ''),
                    'version': data.get('version', 0)
                })
            except Exception as e:
                self.logger.warning(f"Could not read save file {save_file}: {e}")
        
        # Sort by timestamp (newest first)
        saves.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return saves
    
    def delete_save(self, slot_name: str) -> bool:
        """
        Delete a save file.
        
        Args:
            slot_name: Save slot name
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            save_file = self.save_dir / f"{slot_name}.json"
            if save_file.exists():
                save_file.unlink()
                self.logger.info(f"Deleted save: {save_file}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete save: {e}")
            return False


# Example usage
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Create test save data
    player = PlayerData(
        name="Captain Picard",
        rank="Captain",
        rank_level=8,
        reputation=10000,
        credits=50000,
        missions_completed=42,
        ships_destroyed=15
    )
    
    ship = ShipData(
        name="USS Enterprise",
        registry="NCC-1701-D",
        ship_class="Galaxy",
        hull=5000,
        max_hull=5000,
        shields={'fore': 2000, 'aft': 1500, 'port': 1800, 'starboard': 1800},
        max_shields={'fore': 2000, 'aft': 1500, 'port': 1800, 'starboard': 1800},
        crew_count=1000,
        max_crew=1000
    )
    
    mission = MissionData(
        mission_id="mission_001",
        title="Explore Sector 001",
        description="Survey the sector for resources",
        status="active",
        objectives=["Visit 3 systems", "Scan anomaly"],
        rewards={"credits": 1000, "reputation": 100}
    )
    
    save_data = GameSaveData(
        save_name="Test Save",
        player=player,
        player_ship=ship,
        active_missions=[mission],
        current_sector="Sector 001"
    )
    
    # Save game
    save_mgr = SaveManager()
    save_mgr.save_game(save_data, "test_slot")
    
    # List saves
    print("\nAvailable saves:")
    for save in save_mgr.list_saves():
        print(f"  {save['slot']}: {save['name']} ({save['timestamp']})")
    
    # Load game
    loaded = save_mgr.load_game("test_slot")
    if loaded:
        print(f"\nLoaded: {loaded.player.name} on {loaded.player_ship.name}")
        print(f"Missions: {len(loaded.active_missions)}")
