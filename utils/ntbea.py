import time
from typing import List, Tuple
from utils.bandit_1d import Bandit1D
from utils.bandit_2d import Bandit2D
from utils.game_evaluator_oe import GameEvaluatorOE
import math
import random
from joblib import Parallel, delayed


class Ntbea:
    def __init__(self, parameters: List[List[float]], fitness: GameEvaluatorOE, c_value: float, n_neighbours: int, n_initializations: int):
        self.c_value = c_value                      # c parameter for UCB
        self.n_neighbours = n_neighbours            # amount of neighbours per iteration
        self.n_initializations = n_initializations  # amount of initial initializations
        self.n_parameters = len(parameters)         # number of parameters
        self.parameters_values = parameters         # possible values per parameter

        self.bandits1D: List[Bandit1D] = []  # 1D bandits
        self.bandits2D: List[Bandit2D] = []  # 2D bandits
        self.bandit1D_amount = self.n_parameters  # amount of 1D bandits
        self.bandit2D_amount = int((self.n_parameters * (self.n_parameters - 1)) / 2)  # amount of 2D bandits

        self.create_bandits()  # initialize the 1D and 2D bandits
        self.fitness = fitness
        self.n_iterations = 10
        self.cores = 1
        self.str_debug = ""
        self.do_str_debug = False
        self.l_perfects = []

# region set/get
    def set_cores(self, cores):
        self.cores = cores

    def set_str_debug_on(self):
        self.do_str_debug = True
        self.str_debug = ""

    def get_str_debug(self):
        return self.str_debug
# endregion

# region Methods
    def create_bandits(self) -> None:
        """Create the empty 1D and 2D bandits. """
        # Create empty 1D bandits
        for i in range(self.n_parameters):
            new_bandit = Bandit1D(self.c_value)
            self.bandits1D.append(new_bandit)

        # Create empty 2D bandits
        for i in range(0, self.n_parameters - 1):
            for j in range(i + 1, self.n_parameters):
                new_bandit = Bandit2D(self.c_value)
                self.bandits2D.append(new_bandit)

    def run(self, n_games: int, budget: float, n_iteration: int, rounds: int) -> List[int]:
        """Run the NTBEA algorithm."""
        self.n_iterations = n_iteration
        self.l_perfects = []
        current, best_score = self.initialize_bandits(n_games, budget, rounds)

        if self.do_str_debug:
            self.str_debug += "Current: " + str(current) + "\n"

        iteration = 0
        while iteration < self.n_iterations:
            if self.do_str_debug:
                self.str_debug += "Iteration: " + str(iteration) + "\n"
            l_neighbours = self.get_neighbours(current)
            best_neighbour = self.get_best_neighbour(l_neighbours)
            score = self.evaluate(best_neighbour, n_games, budget, rounds)
            self.update_bandits(best_neighbour, score)

            if score >= best_score:
                best_score = score
                current = best_neighbour

            if score == 1.0:
                self.l_perfects.append(best_neighbour)

            if self.do_str_debug:
                self.str_debug += "Best neighbour: " + str(best_neighbour) + " Score: " + str(score) + \
                                  " Current: " + str(current) + " Best score: " + str(best_score) + "\n"
            iteration += 1

        if self.do_str_debug:
            self.str_debug += "Pre-Final best: " + str(current) + " Score: " + str(best_score) + "\n"
            for perfect in self.l_perfects:
                self.str_debug += "Perfect: " + str(perfect) + "\n"

        # Last step: look for the best individual into current neighbours (and l_perfects)
        final_best = self.get_the_final_best(current)
        self.str_debug += "Final best: " + str(final_best) + "\n"
        return final_best

    def get_the_final_best(self, current):
        """Look for the best individual into current neighbours (and l_perfects)."""
        l_neighbours = [current]                           # add current to the list of neighbours
        l_neighbours += self.l_perfects                    # add perfects to the list of neighbours
        l_neighbours = self.get_neighbours(current)        # add current neighbours to the list of neighbours
        for perfect in self.l_perfects:                    # add perfect neighbours to the list of neighbours
            l_neighbours += self.get_neighbours(perfect)

        best_neighbour = self.get_best_neighbour_final(l_neighbours)

        return best_neighbour

    def evaluate_individual(self, individual, n_games, budget, rounds):
        score = self.evaluate(individual, n_games, budget, rounds)
        self.update_bandits(individual, score)
        return individual, score

    def initialize_bandits(self, n_games: int, budget: float, rounds: int):
        """Create n_initializations random individuals and evaluate them. Update the bandits with the results.
        Returns the best individual."""
        l_individuals = []
        # Create n_initializations random individuals
        for i in range(self.n_initializations):
            individual = []
            for j in range(self.n_parameters):
                individual.append(random.randint(0, len(self.parameters_values[j]) - 1))
            l_individuals.append(individual)

        # Evaluate the individuals
        results = Parallel(n_jobs=self.cores)(
            delayed(self.evaluate_individual)(individual, n_games, budget, rounds)
            for individual in l_individuals
        )

        # Get the best individual
        best_score = -math.inf
        best_individual = None
        for individual, score in results:
            if self.do_str_debug:
                self.str_debug += "G -> " + str(individual) + " : " + str(score) + "\n"
            if score >= best_score:
                best_score = score
                best_individual = individual
            if score == 1.0:
                self.l_perfects.append(individual)
        return best_individual, best_score

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

    def evaluate(self, individual: List[int], n_games: int, budget: float, rounds: int) -> float:
        """Evaluates the given individual and returns the score."""
        parameters = []
        for i in range(self.n_parameters):
            parameters.append(self.parameters_values[i][individual[i]])
        return self.fitness.evaluate(parameters, n_games, budget, rounds)

    def get_neighbours(self, current: List[int]) -> List[List[int]]:
        """Returns a list of neighbours of the given individual."""
        l_neighbours = []
        for i in range(self.n_neighbours):
            neighbour = current.copy()
            idx = random.randint(0, self.n_parameters - 1)
            neighbour[idx] = random.randint(0, len(self.parameters_values[idx]) - 1)
            if neighbour not in l_neighbours:
                l_neighbours.append(neighbour)
        return l_neighbours

    def evalute_neighbour(self, neighbour: List[int]):
        """Evaluates the given neighbour and returns the score."""
        score = self.get_total_ucb(neighbour)
        return neighbour, score

    def evalute_neighbour_final(self, neighbour: List[int]):
        """Evaluates the given neighbour and returns the score using ucb_final."""
        score = self.get_total_ucb_final(neighbour)
        return neighbour, score

    def get_the_best_on_list(self, l_results: List[Tuple[List[int], float]]) -> List[int]:
        """Returns the best element of the given list of results."""
        best_score = -math.inf
        best_element = None
        for element, score in l_results:
            if self.do_str_debug:
                self.str_debug += "N -> " + str(element) + " : " + str(score) + "\n"
            if score >= best_score:
                best_score = score
                best_element = element
        return best_element

    def get_best_neighbour(self, l_neighbours: List[List[int]]) -> List[int]:
        """Returns the best neighbour of the given list of neighbours."""
        results = Parallel(n_jobs=self.cores)(
            delayed(self.evalute_neighbour)(neighbour)
            for neighbour in l_neighbours
        )

        best_neighbour = self.get_the_best_on_list(results)
        return best_neighbour

    def get_best_neighbour_final(self, l_neighbours: List[List[int]]) -> List[int]:
        """Returns the best neighbour of the given list of neighbours. Use ucb_final instead of ucb."""
        results = Parallel(n_jobs=self.cores)(
            delayed(self.evalute_neighbour_final)(neighbour)
            for neighbour in l_neighbours
        )

        best_neighbour = self.get_the_best_on_list(results)
        return best_neighbour

    def get_total_ucb(self, individual: List[int]) -> float:
        """Returns the total UCB of the given individual."""
        total_ucb = 0
        # 1D
        for i in range(self.bandit1D_amount):
            element = individual[i]
            total_ucb += self.bandits1D[i].get_ucb(element)

        # 2D
        k = 0
        for i in range(0, self.n_parameters - 1):
            for j in range(i + 1, self.n_parameters):
                element1 = individual[i]
                element2 = individual[j]
                total_ucb += self.bandits2D[k].get_ucb(element1, element2)
                k += 1

        return total_ucb

    def get_total_ucb_final(self, individual: List[int]) -> float:
        """Returns the total UCB of the given individual. It use ucb final instead of ucb."""
        total_ucb = 0
        # 1D
        for i in range(self.bandit1D_amount):
            element = individual[i]
            total_ucb += self.bandits1D[i].get_ucb_final(element)

        # 2D
        k = 0
        for i in range(0, self.n_parameters - 1):
            for j in range(i + 1, self.n_parameters):
                element1 = individual[i]
                element2 = individual[j]
                total_ucb += self.bandits2D[k].get_ucb_final(element1, element2)
                k += 1

        return total_ucb
# endregion
