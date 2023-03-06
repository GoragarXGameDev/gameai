from abc import ABC, abstractmethod
from games.forward_model import ForwardModel

class GameParameters(ABC):
    """Abstract class that will define the parameters of the game"""

    @property
    @abstractmethod
    def forward_model(self) -> 'ForwardModel':
        """Returns the forward model of the game"""
        pass