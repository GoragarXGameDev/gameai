from sys import argv

from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagGame
from heuristics import SimpleHeuristic
from utils import GameEvaluatorOE, Ntbea
import smtplib


def do_asmacag_oe(budget: float):
    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    game = AsmacagGame(parameters, forward_model)

    asmacag_evaluator = GameEvaluatorOE(game, SimpleHeuristic())

    c_value = 1.4
    n_neighbours = 100
    n_initializations = 100
    n_games = 20
    rounds = 100
    n_iterations = 100

    param_population_size = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_survival_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    params = [param_population_size, param_mutation_rate, param_survival_rate]

    cores = 8

    ntbea = Ntbea(params, asmacag_evaluator, c_value, n_neighbours, n_initializations)
    ntbea.set_cores(cores)
    ntbea.set_str_debug_on()
    best_params = ntbea.run(n_games, budget, n_iterations, rounds)

    out_str = ntbea.get_str_debug()
    out_str += "ASMACAG,OE," + str(budget) + "," + \
              str(param_population_size[best_params[0]]) + "," + \
              str(param_mutation_rate[best_params[1]]) + "," + \
              str(param_survival_rate[best_params[2]])

    # write to file
    out_filename = "out/hyper_asmacag_oe_" + str(budget) + ".txt"
    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


if __name__ == '__main__':
    game_name = argv[1]
    algorithm = argv[2]
    budget = float(argv[3])

    if game_name == "asmacag":
        if algorithm == "oe":
            do_asmacag_oe(budget)



