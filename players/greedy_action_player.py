from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players import Player
import math

class GreedyActionPlayer(Player):
    def __init__(self, heuristic: 'Heuristic'):
        """Player class implemented for Greedy Action players."""
        super().__init__()
        self.heuristic = heuristic

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Think about the next action to take."""
        best_reward = -math.inf
        best_action = None
        current_observation = observation.clone()
        actions = observation.get_actions()
        for action in actions:
            observation.copy_into(current_observation)
            forward_model.step(current_observation, action)
            reward = self.heuristic.get_reward(current_observation)
            if reward >= best_reward:
                best_action = action
                best_reward = reward
        if self.verbose:
            print(f"Best action: {best_action}")
        return best_action
# endregion

# region Override
    def __str__(self):
        return "GreedyActionPlayer"
# endregion