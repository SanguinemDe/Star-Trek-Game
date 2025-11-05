"""
Game State Machine
Manages high-level game states and transitions
"""
from enum import Enum, auto
import logging


class GameState(Enum):
    """
    High-level game states.
    Represents the current screen/mode the game is in.
    """
    STARTUP = auto()           # Initial loading/splash screen
    MAIN_MENU = auto()         # Main menu
    NEW_GAME = auto()          # Character creation
    LOAD_GAME = auto()         # Load save file screen
    GALAXY_MAP = auto()        # Galaxy map navigation
    SECTOR_MAP = auto()        # Sector-level navigation
    COMBAT = auto()            # Tactical combat
    STARBASE = auto()          # Starbase/station interface
    SHIP_MANAGEMENT = auto()   # Ship loadout/upgrade screen
    CREW_MANAGEMENT = auto()   # Crew assignment
    MISSION_BRIEFING = auto()  # Mission details
    DIALOGUE = auto()          # Conversation/story scenes
    SCAN_RESULTS = auto()      # Sensor scan display
    OPTIONS = auto()           # Settings menu
    PAUSED = auto()            # Game paused
    QUIT = auto()              # Exiting game
    
    def __str__(self):
        return self.name.replace('_', ' ').title()


class StateManager:
    """
    Manages game state transitions with history and validation.
    
    Usage:
        state_mgr = StateManager(initial_state=GameState.STARTUP)
        state_mgr.transition_to(GameState.MAIN_MENU)
        
        if state_mgr.current_state == GameState.COMBAT:
            # Handle combat
            pass
    """
    
    def __init__(self, initial_state=GameState.STARTUP):
        """
        Initialize state manager.
        
        Args:
            initial_state: Starting state (default: STARTUP)
        """
        self.current_state = initial_state
        self.previous_state = None
        self.state_history = [initial_state]
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"StateManager initialized: {initial_state}")
    
    def transition_to(self, new_state, allow_same=False):
        """
        Transition to a new state.
        
        Args:
            new_state: GameState to transition to
            allow_same: If True, allows transitioning to current state
            
        Returns:
            bool: True if transition succeeded
        """
        if not isinstance(new_state, GameState):
            self.logger.error(f"Invalid state: {new_state}")
            return False
        
        if new_state == self.current_state and not allow_same:
            self.logger.warning(f"Already in state: {new_state}")
            return False
        
        # Validate transition (can add rules here)
        if not self._can_transition(self.current_state, new_state):
            self.logger.error(f"Invalid transition: {self.current_state} -> {new_state}")
            return False
        
        # Perform transition
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_history.append(new_state)
        
        self.logger.info(f"State transition: {self.previous_state} -> {new_state}")
        return True
    
    def _can_transition(self, from_state, to_state):
        """
        Validate if transition is allowed.
        Add custom rules here as needed.
        
        Args:
            from_state: Current state
            to_state: Target state
            
        Returns:
            bool: True if transition is valid
        """
        # Example rule: Can't go to QUIT from COMBAT directly (must pause first)
        # if from_state == GameState.COMBAT and to_state == GameState.QUIT:
        #     return False
        
        # For now, allow all transitions
        return True
    
    def go_back(self):
        """
        Return to previous state.
        
        Returns:
            bool: True if successfully went back
        """
        if self.previous_state is None:
            self.logger.warning("No previous state to return to")
            return False
        
        return self.transition_to(self.previous_state, allow_same=True)
    
    def is_state(self, state):
        """
        Check if current state matches.
        
        Args:
            state: GameState to check
            
        Returns:
            bool: True if current state matches
        """
        return self.current_state == state
    
    def is_in_states(self, *states):
        """
        Check if current state is in list of states.
        
        Args:
            states: Variable number of GameState values
            
        Returns:
            bool: True if current state is in list
        """
        return self.current_state in states
    
    def get_state_name(self):
        """Get human-readable name of current state"""
        return str(self.current_state)
    
    def get_history(self, limit=10):
        """
        Get recent state history.
        
        Args:
            limit: Maximum number of states to return
            
        Returns:
            list: Recent states (newest first)
        """
        return list(reversed(self.state_history[-limit:]))
    
    def clear_history(self):
        """Clear state history (keeps current state)"""
        self.state_history = [self.current_state]
        self.logger.debug("State history cleared")


# Example screen interface (for reference)
class Screen:
    """
    Base class for game screens.
    Each screen should implement these methods.
    """
    
    def __init__(self):
        self.active = False
    
    def enter(self):
        """Called when entering this screen"""
        self.active = True
    
    def exit(self):
        """Called when leaving this screen"""
        self.active = False
    
    def update(self, dt):
        """
        Update screen logic.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    def render(self, surface):
        """
        Render screen to surface.
        
        Args:
            surface: pygame surface to draw on
        """
        pass
    
    def handle_events(self, events):
        """
        Handle pygame events.
        
        Args:
            events: List of pygame events
        """
        pass


class ScreenManager:
    """
    Manages screen instances and their lifecycle.
    Works in conjunction with StateManager.
    
    Usage:
        screen_mgr = ScreenManager()
        screen_mgr.register(GameState.MAIN_MENU, MainMenuScreen())
        screen_mgr.register(GameState.COMBAT, CombatScreen())
        
        # Switch screens
        screen_mgr.set_active(GameState.COMBAT)
        
        # In game loop
        screen_mgr.update(dt)
        screen_mgr.render(screen)
    """
    
    def __init__(self):
        self.screens = {}
        self.active_screen = None
        self.logger = logging.getLogger(__name__)
    
    def register(self, state, screen):
        """
        Register a screen for a specific state.
        
        Args:
            state: GameState this screen represents
            screen: Screen instance
        """
        self.screens[state] = screen
        self.logger.debug(f"Registered screen for state: {state}")
    
    def set_active(self, state):
        """
        Set active screen by state.
        
        Args:
            state: GameState to activate
            
        Returns:
            bool: True if successful
        """
        if state not in self.screens:
            self.logger.error(f"No screen registered for state: {state}")
            return False
        
        # Exit current screen
        if self.active_screen:
            self.active_screen.exit()
        
        # Enter new screen
        self.active_screen = self.screens[state]
        self.active_screen.enter()
        
        self.logger.info(f"Active screen set to: {state}")
        return True
    
    def update(self, dt):
        """Update active screen"""
        if self.active_screen:
            self.active_screen.update(dt)
    
    def render(self, surface):
        """Render active screen"""
        if self.active_screen:
            self.active_screen.render(surface)
    
    def handle_events(self, events):
        """Pass events to active screen"""
        if self.active_screen:
            self.active_screen.handle_events(events)


# Example usage
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Create state manager
    state_mgr = StateManager()
    
    # Simulate state transitions
    print(f"Current: {state_mgr.get_state_name()}")
    
    state_mgr.transition_to(GameState.MAIN_MENU)
    state_mgr.transition_to(GameState.GALAXY_MAP)
    state_mgr.transition_to(GameState.COMBAT)
    
    print(f"Current: {state_mgr.get_state_name()}")
    print(f"History: {[str(s) for s in state_mgr.get_history()]}")
    
    state_mgr.go_back()
    print(f"After go_back: {state_mgr.get_state_name()}")
