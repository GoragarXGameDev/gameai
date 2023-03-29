from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players import Player
import math
import time

class GreedyActionPlayer(Player):
    def __init__(self, heuristic: 'Heuristic'):
        """Player class implemented for Greedy Action players."""
        super().__init__()
        self.heuristic = heuristic
        self.turn = []

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of action for a complete turn using the Greedy Action algorithm and sets it as the turn."""
        self.turn.clear()

        # compute the turn
        t0 = time.time()
        current_observation = observation.clone()
        while time.time() - t0 < budget - 0.05 and len(self.turn) < observation.get_game_parameters().get_action_points_per_turn():
            best_reward = -math.inf
            best_action = None
            actions = current_observation.get_actions()
            new_observation = current_observation.clone()
            for action in actions:
                if time.time() - t0 > budget - 0.05:
                    break
                current_observation.copy_into(new_observation)
                forward_model.step(new_observation, action)
                self.forward_model_visits += 1
                self.visited_states[new_observation] += 1
                reward = self.heuristic.get_reward(new_observation)
                if reward >= best_reward:
                    best_action = action
                    best_reward = reward
            self.turn.append(best_action)
            forward_model.step(current_observation, best_action)
            best_action = None

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None
# endregion

# region Override
    def __str__(self):
        return "GreedyActionPlayer"
# endregion