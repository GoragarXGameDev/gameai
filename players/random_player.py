from games.action import Action
from games.forward_model import ForwardModel
from games.observation import Observation
from players.player import Player

class RandomPlayer(Player):
    def __init__(self):
        """Player class implemented for Random players."""
        super().__init__()

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Think about the next action to take."""
        return observation.get_random_action()
# endregion

# region Override
    def __str__(self):
        return "RandomPlayer"
# endregion