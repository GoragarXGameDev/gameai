from games.action import Action
from games.forward_model import ForwardModel
from games.observation import Observation
from heuristics.heuristic import Heuristic
from players.montecarlo_tree_search.montecarlo_tree_search_node import MontecarloTreeSearchNode
from players.player import Player
import time

class MontecarloTreeSearchPlayer(Player):
    """Entity that plays a game by using the Monte Carlo Tree Search algorithm to choose all actions in a turn."""
    def __init__(self, heuristic: 'Heuristic', c_value: float):
        super().__init__()
        self.heuristic = heuristic
        self.c_value = c_value
        self.turn = []


# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Computes a list of actions for a complete turn using the Monte Carlo Tree Search algorithm and returns them in order each time it's called during the turn."""
        if observation.get_action_points_left() == observation.get_game_parameters().get_action_points_per_turn():
            self.turn.clear()
            self.compute_turn(observation, forward_model, budget)
        if len(self.turn) == 0:
            return None
        return self.turn.pop(0)

    def compute_turn(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of action for a complete turn using the Monte Carlo Tree Search algorithm and sets it as the turn."""
        t0 = time.time()
        root = MontecarloTreeSearchNode(observation, self.heuristic, None)
        root.extend(forward_model)
        current_node = root

        while time.time() - t0 < budget - 0.12:
            best_child = current_node.get_best_child_by_ucb(self.c_value)
            if best_child.get_amount_of_children() > 0:
                current_node = best_child
            else:
                if not best_child.get_is_unvisited() and not best_child.get_is_terminal(forward_model):
                    best_child.extend(forward_model)
                    best_child = best_child.get_random_child()
                best_child.backpropagate(best_child.rollout(forward_model))
                current_node = root

        # retrieve the turn
        current_node = root
        for i in range(observation.get_game_parameters().get_action_points_per_turn()):
            best_child = current_node.get_best_child_by_average()
            if best_child is None:
                self.turn.append(None)
                continue
            self.turn.append(best_child.get_action() if best_child is not None else None)
            current_node = best_child
# endregion

# region Override
    def __str__(self):
        return f"MontecarloTreeSearchPlayer[{self.c_value}]"
# endregion