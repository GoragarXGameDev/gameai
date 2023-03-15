from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagGame
from heuristics import SimpleHeuristic
from utils import GameEvaluatorOE
from ntbea import Ntbea
import random


if __name__ == '__main__':
    # random.seed(0)
    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    game = AsmacagGame(parameters, forward_model)

    asmacag_evaluator = GameEvaluatorOE(game, SimpleHeuristic())

    c_value = 0.5
    n_neighbours = 100
    mutation_rate = 0.5
    n_initializations = 100
    param_population_size = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_survival_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    params = [param_population_size, param_mutation_rate, param_survival_rate]

    ntbea = Ntbea(params, asmacag_evaluator, c_value, n_neighbours, mutation_rate, n_initializations)
    ntbea.run()
