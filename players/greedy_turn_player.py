from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players import Player
from players.greedy_turn.greedy_turn_node import GreedyTurnNode
import math
import time

class GreedyTurnPlayer(Player):
    def __init__(self, heuristic: 'Heuristic'):
        """Player class implemented for Greedy Turn players."""
        super().__init__()
        self.heuristic = heuristic
        self.turn = []

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of action for a complete turn using the Greedy Turn algorithm and sets it as the turn."""
        self.turn.clear()
        
        t0 = time.time()
        root = GreedyTurnNode(observation, self.heuristic, None)
        best_reward = -math.inf
        self.run_nodes(root, forward_model, budget, best_reward, 0, t0)

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None
        
    def run_nodes(self, node: 'GreedyTurnNode', forward_model: 'ForwardModel', budget: float, best_reward: float, index: int, t0: time) -> None:
        if index != 0:
            self.visited_states[node.get_observation()] += 1
            self.forward_model_visits += 1
        child: 'GreedyTurnNode' = None
        for child in node.extend(forward_model):
            if time.time() - t0 > budget:
                return
            if index == child.get_observation().get_game_parameters().get_action_points_per_turn() - 1:
                reward = self.heuristic.get_reward(child.get_observation())
                if reward >= best_reward:
                    best_reward = reward
                    self.turn = child.get_path()
                return
            else:
                self.run_nodes(child, forward_model, budget, best_reward, index + 1, t0)
# endregion

# region Override
    def __str__(self):
        return "GreedyTurnPlayer"
# endregion