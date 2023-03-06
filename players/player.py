from abc import ABC, abstractmethod
from games.action import Action
from games.observation import Observation

class Player(ABC):
    """Abstract class that will define a player of the game"""

    @abstractmethod
    def think(self, observation: 'Observation', budget: float) -> 'Action':
        """Returns the action to be executed"""
        pass
