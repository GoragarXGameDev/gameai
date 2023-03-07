from typing import List
from games.action import Action
from games.observation import Observation
from heuristics.heuristic import Heuristic
from players.online_evolution.turn_genome import TurnGenome
from players.player import Player
import time
import random

class OnlineEvolutionPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', population_size: int, mutation_rate: float, survival_rate: float) -> None:
        """Entity that plays a game by using the Online Evolution algorithm to choose all actions in a turn."""
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.survival_rate = survival_rate
        self.heuristic = heuristic
        self.turn = []
        super().__init__()

# region Methods
    def think(self, observation: 'Observation', budget: float) -> 'Action':
        """Computes a list of actions for a complete turn using the Online Evolution algorithm and returns them in order each time it's called during the turn."""
        if observation.action_points_left == observation.game_parameters.action_points_per_turn and len(self.turn) > 0:
            self.turn.clear()
            self.compute_turn(observation, budget)
        if len(self.turn) == 0:
            return None
        return self.turn.pop(0)

    def compute_turn(self, observation: 'Observation', budget: float) -> None:
        """Computes a list of action for a complete turn using the Online Evolution algorithm and sets it as the turn."""
        t0 = time.time()
        population: List['TurnGenome'] = []
        killed: List['TurnGenome'] = []

        new_observation = observation.clone()
        # initial population
        for i in range(self.population_size):
            genome = TurnGenome()
            observation.copy_into(new_observation)
            genome.random(new_observation)
            population.append(genome)
            killed.append(genome)

        while time.time() - t0 < budget - 0.05:
            # evaluate the new genomes
            for genome in killed:
                observation.copy_into(new_observation)
                for action in genome.get_actions():
                    observation.game_parameters.forward_model.step(new_observation, action)
                genome.set_reward(self.heuristic.get_reward(new_observation))

            # kill the worst genomes
            killed.clear()
            population.sort(key=lambda g: g.get_reward(), reverse=True)
            first_killed_genome_index = int(self.survival_rate * self.population_size)
            for i in range(first_killed_genome_index, self.population_size):
                killed.append(population[i])

            # create new genomes using the remaining ones for crossover
            for killed_genome in killed:
                # decide parents
                parent_a_index = random.randrange(first_killed_genome_index)
                parent_b_index = random.randrange(first_killed_genome_index)
                while parent_a_index == parent_b_index and len(killed) > 1:
                    parent_b_index = random.randrange(first_killed_genome_index)

                # crossover
                observation.copy_into(new_observation)
                killed_genome.crossover(population[parent_a_index], population[parent_b_index], new_observation)

                # mutate
                if random.random() < self.mutation_rate:
                    observation.copy_into(new_observation)
                    killed_genome.mutate_at_random_index(new_observation)

        # select the best genome to use for the turn
        self.turn = population[0].get_actions()
# endregion

# region Override
    def __str__(self):
        return f"OEPlayer[{self.population_size!s}][{self.mutation_rate!s}][{self.survival_rate!s}]"
# endregion