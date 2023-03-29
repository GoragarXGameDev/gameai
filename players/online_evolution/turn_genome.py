from collections import defaultdict
from typing import List
from games import Action, Observation, ForwardModel
import random

class TurnGenome:
    def __init__(self):
        """Turn Genome class used in the Online Evolution algorithm."""
        self.actions: List['Action'] = []
        self.reward = 0

# region Methods
    def random(self, observation: 'Observation', forward_model: 'ForwardModel', visited_states: defaultdict) -> int:
        """Fills up this genome with random valid actions"""
        self.actions.clear()
        self.reward = 0
        fm_visits = 0
        while not forward_model.is_terminal(observation) and not forward_model.is_turn_finished(observation):
            action = observation.get_random_action()
            self.actions.append(action)
            forward_model.step(observation, action)
            visited_states[observation] += 1
            fm_visits += 1
        return fm_visits

    def crossover(self, parent_a: 'TurnGenome', parent_b: 'TurnGenome', observation: 'Observation', forward_model: 'ForwardModel', visited_states: defaultdict) -> int:
        """Fills up this genome with a crossover of the two parents"""
        self.reward = 0
        actions_count = min(observation.get_game_parameters().get_action_points_per_turn(), len(self.actions))
        for i in range(actions_count):
            # choose a random parent and add action at index if valid, otherwise use the other parent
            added = False
            if bool(random.getrandbits(1)):
                if (len(parent_a.actions) >= i) and observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True
                elif (len(parent_b.actions) >= i) and observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
            else:
                if (len(parent_b.actions) >= i) and observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
                elif (len(parent_a.actions) >= i) and observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True

            # if no action was added, add a random one
            if not added:
                action = observation.get_random_action()
                self.actions[i] = action

            forward_model.step(observation, self.actions[i])
            visited_states[observation] += 1
        return actions_count

    def mutate_at_random_index(self, observation: 'Observation', forward_model: 'ForwardModel', visited_states: defaultdict, verbose: bool = False) -> int:
        """Mutates this genome at a random action of the turn while keeping the whole turn valid. Note that the'Observation'state is not preserved."""
        mutation_index = random.randrange(len(self.actions))
        for i in range(len(self.actions)):
            if i == mutation_index:
                self.actions[i] = observation.get_random_action()
            elif i > mutation_index:
                if not observation.is_action_valid(self.actions[i]):
                    if verbose:
                        print(f"mutate_at_random_index: action {self.actions[i]} is not valid, replacing with random action")
                    self.actions[i] = observation.get_random_action()

            forward_model.step(observation, self.actions[i])
            visited_states[observation] += 1
        return len(self.actions)

    def clone(self) -> 'TurnGenome':
        """Returns a clone of this genome"""
        clone = TurnGenome()
        clone.set_reward(self.get_reward())
        for action in self.get_actions():
            clone.actions.append(action.clone())
        return clone

    def copy_into(self, other: 'TurnGenome') -> None:
        """Copies this genome into another one."""
        other.set_reward(self.get_reward())
        for i in range(len(self.get_actions())):
            if i < len(other.get_actions()):
                self.get_actions()[i].copy_into(other.get_actions()[i])
            else:
                other.get_actions().append(self.get_actions()[i].clone())
# endregion

# region Getters
    def get_actions(self) -> List['Action']:
        """Returns the list of actions of this genome."""
        return self.actions

    def get_reward(self) -> float:
        """Returns the reward of this genome."""
        return self.reward

    def set_reward(self, reward: float) -> None:
        """Sets the reward of this genome."""
        self.reward = reward
# endregion

# region Override
    def __str__(self):
        return f"TurnGenome [actions={self.actions}, reward={self.reward}]"
# endregion