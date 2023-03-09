from abc import ABC, abstractmethod
from typing import Any, Dict
from games.game_parameters import GameParameters
from games.observation import Observation

class GameState(ABC):
    """Abstract class that will define the state of the game"""

    @property
    @abstractmethod
    def game_parameters(self) -> 'GameParameters':
        """Returns the parameters of the game"""
        pass

    @property
    @abstractmethod
    def current_turn(self) -> int:
        """Returns the current turn"""
        pass

    @property
    @abstractmethod
    def player_0_score(self) -> int:
        """Returns the score of player 0"""
        pass

    @property
    @abstractmethod
    def player_1_score(self) -> int:
        """Returns the score of player 1"""
        pass

    @abstractmethod
    def get_observation(self) -> 'Observation':
        """Returns the observation of the game state"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets the game state"""
        pass

    @abstractmethod
    def get_state_info(self) -> Dict[str, Any]:
        """Returns the information of the game state"""
        pass