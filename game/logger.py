"""
Logging System Setup
Centralized logging configuration for the game
"""
import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    Initialize game logging system.
    
    Creates logs directory if needed and configures both file and console logging.
    
    Args:
        log_level: Logging level (default: logging.INFO)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / "latest.log"
    archive_file = log_dir / f"game_{timestamp}.log"
    
    # If latest.log exists, archive it
    if log_file.exists():
        try:
            log_file.rename(archive_file)
        except Exception as e:
            print(f"Warning: Could not archive previous log: {e}")
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # File handler - detailed logs
            logging.FileHandler(log_file, encoding='utf-8'),
            # Console handler - warnings and above only
            logging.StreamHandler()
        ]
    )
    
    # Set console handler to only show warnings and above
    console_handler = logging.getLogger().handlers[1]
    console_handler.setLevel(logging.WARNING)
    
    # Log startup
    logging.info("=" * 60)
    logging.info("Star Trek Game - Logging System Initialized")
    logging.info(f"Log file: {log_file}")
    logging.info(f"Log level: {logging.getLevelName(log_level)}")
    logging.info("=" * 60)


def get_logger(name):
    """
    Get a logger for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger instance
    
    Example:
        logger = get_logger(__name__)
        logger.info("Starting combat")
        logger.warning("Shield strength low")
        logger.error("Failed to load ship data")
    """
    return logging.getLogger(name)


def log_exception(logger, exception, context=""):
    """
    Log an exception with full traceback.
    
    Args:
        logger: Logger instance
        exception: Exception object
        context: Additional context string
    """
    if context:
        logger.exception(f"{context}: {exception}")
    else:
        logger.exception(f"Exception occurred: {exception}")


def log_combat_start(logger, player_ship, enemy_ship):
    """Log combat initiation"""
    logger.info("=" * 40)
    logger.info(f"COMBAT START")
    logger.info(f"Player: {player_ship.name} ({player_ship.ship_class})")
    logger.info(f"Enemy: {enemy_ship.name} ({enemy_ship.ship_class})")
    logger.info("=" * 40)


def log_combat_end(logger, result, turns):
    """Log combat conclusion"""
    logger.info("=" * 40)
    logger.info(f"COMBAT END - {result}")
    logger.info(f"Duration: {turns} turns")
    logger.info("=" * 40)


def log_weapon_fire(logger, attacker, weapon, target, hit, damage=0):
    """Log weapon firing"""
    status = "HIT" if hit else "MISS"
    if hit:
        logger.debug(f"{attacker.name} fires {weapon} at {target.name} - {status} for {damage} damage")
    else:
        logger.debug(f"{attacker.name} fires {weapon} at {target.name} - {status}")


def log_ship_destroyed(logger, ship_name):
    """Log ship destruction"""
    logger.info(f"*** {ship_name} DESTROYED ***")


def log_performance(logger, operation, duration_ms):
    """
    Log performance metrics.
    
    Args:
        logger: Logger instance
        operation: Name of operation
        duration_ms: Duration in milliseconds
    """
    if duration_ms > 100:
        logger.warning(f"Performance: {operation} took {duration_ms:.2f}ms (SLOW)")
    else:
        logger.debug(f"Performance: {operation} took {duration_ms:.2f}ms")


def log_save_game(logger, save_file):
    """Log game save"""
    logger.info(f"Game saved to: {save_file}")


def log_load_game(logger, save_file):
    """Log game load"""
    logger.info(f"Game loaded from: {save_file}")


# Example usage
if __name__ == "__main__":
    # Initialize logging
    setup_logging()
    
    # Get logger for this module
    logger = get_logger(__name__)
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test exception logging
    try:
        1 / 0
    except Exception as e:
        log_exception(logger, e, "Math error test")
    
    print("\nCheck logs/latest.log for output!")
