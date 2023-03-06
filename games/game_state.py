from abc import ABC, abstractmethod
from games.observation import Observation

class GameState(ABC):
    """Abstract class that will define the state of the game"""

    @abstractmethod
    def get_observation(self) -> 'Observation':
        """Returns the observation of the game state"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets the game state"""
        pass