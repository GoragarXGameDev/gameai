from typing import List, Optional
from games.action import Action
from games.observation import Observation
from heuristics.heuristic import Heuristic
import math
import random
import sys

class MontecarloTreeSearchNode:
    def __init__(self, observation: 'Observation', heuristic: 'Heuristic', action: 'Action', parent: 'MontecarloTreeSearchNode' = None):
        """Node class for the tree used in Montecarlo Tree Search."""
        self.observation = observation
        self.heuristic = heuristic
        self.action = action
        self.parent = parent
        self.children: List['MontecarloTreeSearchNode'] = []
        self.visits = 0
        self.reward = 0

# region Methods
    def visit(self, reward: float) -> None:
        """Visits the `Node` by adding to the visit count and adding the reward to the total reward."""
        self.visits += 1
        self.reward += reward

    def add_child(self, child: 'MontecarloTreeSearchNode') -> None:
        """Adds a child to the `Node` child list."""
        self.children.append(child)

    def extend(self) -> None:
        """Extends the `Node` by generating a child for each possible action"""
        actions = self.observation.get_actions()
        for action in actions:
            new_observation = self.observation.clone()
            self.observation.game_parameters.forward_model.step(new_observation, action)
            self.children.append(MontecarloTreeSearchNode(new_observation, self.heuristic, action, self))

    def rollout(self) -> float:
        """Performs a random rollout from the `Node` and returns the reward."""
        new_observation = self.observation.clone()
        while not self.observation.game_parameters.forward_model.is_terminal(new_observation)\
                and not self.observation.game_parameters.forward_model.is_turn_finished(new_observation):
            self.observation.game_parameters.forward_model.step(new_observation, new_observation.get_random_action())
        return self.heuristic.get_reward(new_observation)

    def backpropagate(self, reward: float) -> None:
        """Backpropagates the reward to the `Node` and its parents."""
        self.visit(reward)
        parent = self.parent
        while parent is not None:
            parent.visit(reward)
            parent = parent.parent
# endregion

# region Getters
    def get_action(self) -> 'Action':
        """Returns the `ASMACAG.Game.Action.Action` of the `Node`."""
        return self.action

    def get_average_reward(self) -> float:
        """Returns the average reward of the `Node`"""
        return self.reward / self.visits if self.visits > 0 else -math.inf

    def get_best_child_by_average(self) -> "Optional[MontecarloTreeSearchNode]":
        """Returns the best child of the `Node` by average reward."""
        if len(self.children) == 0:
            return None
        best_child = self.children[0]
        best_average_reward = best_child.get_average_reward()
        
        for child in self.children:
            if child.get_average_reward() > best_average_reward:
                best_child = child
                best_average_reward = child.get_average_reward()
        return best_child

    def get_best_child_by_ucb(self, c_value: float) -> 'MontecarloTreeSearchNode':
        """Returns the child of the `Node` with the highest UCB value."""
        best_child = self.children[0]
        best_ucb = -math.inf
        
        for child in self.children:
            epsilon = random.random() / 1000
            if child.visits != 0:
                ucb = child.get_average_reward() + c_value * math.sqrt(math.log(self.visits) / child.visits) + epsilon
            else:
                ucb = sys.float_info.max - epsilon
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
        return best_child

    def get_random_child(self) -> 'MontecarloTreeSearchNode':
        """Returns a random child of the `Node`."""
        return random.choice(self.children)

    def get_amount_of_children(self) -> int:
        """Returns the amount of children of the `Node`."""
        return len(self.children)

    def get_is_unvisited(self) -> bool:
        """Returns whether the `Node` is unvisited."""
        return self.visits == 0

    def get_is_terminal(self) -> bool:
        """Returns whether the `Node` is terminal (as in the game is over or the turn is finished)."""
        return self.observation.game_parameters.forward_model.is_terminal(self.observation) \
            or self.observation.game_parameters.forward_model.is_turn_finished(self.observation)
# endregion