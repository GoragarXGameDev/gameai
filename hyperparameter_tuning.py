from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagGame
from heuristics import SimpleHeuristic
from utils import GameEvaluatorOE, Ntbea
import random


def do_ASMACAG_OE(budget: float):
    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    game = AsmacagGame(parameters, forward_model)

    asmacag_evaluator = GameEvaluatorOE(game, SimpleHeuristic())

    c_value = 1.4
    n_neighbours = 10
    mutation_rate = 0.5
    n_initializations = 10
    n_games = 20
    rounds = 100
    n_iterations = 10

    param_population_size = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_survival_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    params = [param_population_size, param_mutation_rate, param_survival_rate]

    cores = 4

    ntbea = Ntbea(params, asmacag_evaluator, c_value, n_neighbours, mutation_rate, n_initializations)
    ntbea.set_cores(cores)
    best_params = ntbea.run(n_games, budget, n_iterations, rounds)

    out_str = "ASMACAG,OE," + str(budget) + "," + \
              str(param_population_size[best_params[0]]) + "," + \
              str(param_mutation_rate[best_params[1]]) + "," + \
              str(param_survival_rate[best_params[2]])

    # write to file
    out_filename = "out/hyper_asmacag_oe_" + str(budget) + ".txt"
    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


if __name__ == '__main__':
    do_ASMACAG_OE(0.1)
    #do_ASMACAG_OE(1.0)
    #do_ASMACAG_OE(3.0)
    #do_ASMACAG_OE(5.0)


