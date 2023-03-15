from typing import List
from utils import *
import math
import random

class Ntbea:
    def __init__(self, parameters: List[List[float]], fitness: GameEvaluatorOE, c_value: float, n_neighbours: int, mutation_rate: float, n_initializations: int):
        self.c_value = c_value                      # c parameter for UCB
        self.n_neighbours = n_neighbours            # amount of neighbours per iteration
        self.mutation_rate = mutation_rate          # mutation rate
        self.n_initializations = n_initializations  # amount of initial initializations
        self.n_parameters = len(parameters)         # number of parameters
        self.parameters_values = parameters         # possible values per parameter

        self.bandits1D: List['Bandit1D'] = []  # 1D bandits
        self.bandits2D: List['Bandit2D'] = []  # 2D bandits
        self.bandit1D_amount = self.n_parameters  # amount of 1D bandits
        self.bandit2D_amount = int((self.n_parameters * (self.n_parameters - 1)) / 2)  # amount of 2D bandits

        self.create_bandits()  # initialize the 1D and 2D bandits
        self.fitness = fitness

# region Methods
    def create_bandits(self) -> None:
        """Create the empty 1D and 2D bandits."""
        # Create empty 1D bandits
        for i in range(self.n_parameters):
            new_bandit = Bandit1D(self.c_value)
            self.bandits1D.append(new_bandit)

        # Create empty 2D bandits
        for i in range(0, self.n_parameters - 1):
            for j in range(i + 1, self.n_parameters):
                new_bandit = Bandit2D(self.c_value)
                self.bandits2D.append(new_bandit)

    def run(self) -> None:
        # initialize the bandits
        l_currents = []
        current = self.initialize_bandits()
        l_currents.append(current)
        print("Best individual: " + str(current))

        # run the algorithm
        # TODO: rest ntbea algorithm

    def initialize_bandits(self) -> List[int]:
        """Create n_initializations random individuals and evaluate them. Update the bandits with the results. Returns the best individual."""
        l_individuals = []
        # Create n_initializations random individuals
        for i in range(self.n_initializations):
            individual = []
            for j in range(self.n_parameters):
                individual.append(random.randint(0, len(self.parameters_values[j]) - 1))
            l_individuals.append(individual)

        # Evaluate the individuals
        best_score = -math.inf
        best_individual = None
        for individual in l_individuals:
            score = self.evaluate(individual)
            self.update_bandits(individual, score)
            print("Individual: " + str(individual) + " - Score: " + str(score))
            if score > best_score:
                best_score = score
                best_individual = individual
        return best_individual

    def update_bandits(self, individual: List[int], score: float) -> None:
        """Updates the bandits with the given individual and score."""
        # 1D
        for i in range(self.bandit1D_amount):
            element = individual[i]
            self.bandits1D[i].update(element, score)

        # 2D
        k = 0
        for i in range(0, self.n_parameters - 1):
            for j in range(i + 1, self.n_parameters):
                element1 = individual[i]
                element2 = individual[j]
                self.bandits2D[k].update(element1, element2, score)
                k += 1

    def evaluate(self, individual: List[int]) -> float:
        """Evaluates the given individual and returns the score."""
        parameters = []
        for i in range(self.n_parameters):
            parameters.append(self.parameters_values[i][individual[i]])
        return self.fitness.evaluate(parameters)
# endregion
