from games import Action, Observation, ForwardModel
from players import Player

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