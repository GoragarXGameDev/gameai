from abc import ABC, abstractmethod
from typing import List
from games.action import Action
from games.game_parameters import GameParameters

class Observation(ABC):
    """Abstract class that will define the observation of the game"""

    @property
    @abstractmethod
    def game_parameters(self) -> 'GameParameters':
        """Returns the parameters of the game"""
        pass

    @property
    @abstractmethod
    def action_points_left(self) -> int:
        """Returns the number of action points left"""
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
    def clone(self) -> 'Observation':
        """Return a copy of the observation"""
        pass
    
    @abstractmethod
    def copy_into(self, other: 'Observation') -> None:
        """Copy the observation into another observation"""
        pass

    @abstractmethod
    def is_action_valid(self, action: 'Action') -> bool:
        """Return True if the action is valid"""
        pass

    @abstractmethod
    def get_actions(self) -> List['Action']:
        """Return a list of valid actions"""
        pass

    @abstractmethod
    def get_random_action(self) -> 'Action':
        """Return a random valid action"""
        pass
