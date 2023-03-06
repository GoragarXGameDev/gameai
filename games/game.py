from abc import ABC, abstractmethod
from typing import Optional
from games.action import Action
from games.observation import Observation
from players.player import Player

class Game(ABC):
    """Abstract class that will define how to play the game"""

    @abstractmethod
    def reset(self) -> None:
        """Resets the game"""
        pass

    @abstractmethod
    def run(self, player_0: 'Player', player_1: 'Player', budget: float, verbose: bool, enforce_time: bool) -> None:
        """Runs the game"""
        pass

    @abstractmethod
    def play_turn(self, player: 'Player', budget: float, verbose: bool,enforce_time: bool) -> 'Action':
        """The current player plays a turn"""
        pass

    @abstractmethod
    def think(self, player: 'Player', observation: 'Observation', budget: float) -> 'Action':
        """The returns the action to be played"""
        pass

    @abstractmethod
    def get_random_action(self) -> 'Action':
        """Returns a random valid action"""
        pass

    @abstractmethod
    def set_save_file(self, save_file: Optional[str]) -> None:
        """Sets the save file"""
        pass

    @abstractmethod
    def get_winner(self) -> int:
        """Returns the winner of the game"""
        pass