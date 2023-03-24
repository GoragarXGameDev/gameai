from collections import defaultdict
from typing import List
from games import Action, Observation, ForwardModel
from heuristics import Heuristic

class GreedyTurnNode:
    def __init__(self, observation: 'Observation', heuristic: 'Heuristic', action: 'Action', parent: 'GreedyTurnNode' = None):
        """Node class for the tree used in Greedy Turn Search."""
        self.observation = observation
        self.heuristic = heuristic
        self.action = action
        self.parent = parent
        self.children: List['GreedyTurnNode'] = []

    def extend(self, forward_model: 'ForwardModel') -> List['GreedyTurnNode']:
        """Extends the `Node` by generating a child for each possible action"""
        actions = self.observation.get_actions()
        for action in actions:
            new_observation = self.observation.clone()
            forward_model.step(new_observation, action)
            child = GreedyTurnNode(new_observation, self.heuristic, action, self)
            self.children.append(child)
            yield child
    
    def get_path(self) -> List['Action']:
        """Returns the path from the root to this node."""
        path = []
        node = self
        while node.parent is not None:
            path.insert(0, node.action)
            node = node.parent
        return path
    
    def get_children(self) -> List['GreedyTurnNode']:
        return self.children
    
    def get_observation(self) -> 'Observation':
        return self.observation