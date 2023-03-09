from abc import ABC, abstractmethod
from typing import Optional

class GameParameters(ABC):
    """Abstract class that will define the parameters of the game"""

    @property
    @abstractmethod
    def action_points_per_turn(self) -> int:
        """Returns the number of action points per turn"""
        pass

    @property
    @abstractmethod
    def seed(self) -> Optional[int]:
        """Returns the seed of the game"""
        pass