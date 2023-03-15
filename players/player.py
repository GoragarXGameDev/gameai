from abc import ABC, abstractmethod
from games.action import Action
from games.forward_model import ForwardModel
from games.observation import Observation


class Player(ABC):
    """Abstract class that will define a player of the game"""
    def __init__(self):
        self.verbose = False

    @abstractmethod
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Returns the action to be executed"""
        pass

    def set_verbose(self, verbose: bool):
        """Set the verbosity of the player"""
        self.verbose = verbose
