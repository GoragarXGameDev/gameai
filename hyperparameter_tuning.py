import math
from sys import argv

from joblib import Parallel, delayed

from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagGame
from heuristics import SimpleHeuristic
from players import MontecarloTreeSearchPlayer
from utils import GameEvaluatorOE, Ntbea


from utils.GameEvaluator import GameEvaluator


def evaluate(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds:int):
    mcts_player = MontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def do_asmacag_mcts(budget:float):
    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    game = AsmacagGame(parameters, forward_model)

    asmacag_evaluator = GameEvaluator(game, SimpleHeuristic())
    params_c = [round(0.35 + i*0.35, 2) for i in range(30)]
    n_games = 100
    rounds = 100
    cores = 8

    results = Parallel(n_jobs=cores)(
        delayed(evaluate)(c, asmacag_evaluator, n_games, budget, rounds)
        for c in params_c
    )

    best_c = None
    best_score = -math.inf
    out_str = ""
    for param_c, score in results:
        if score >= best_score:
            best_score = score
            best_c = param_c
        out_str += str(param_c) + "," + str(score) + " \n"

    out_str += "ASMACAG,MCTS," + str(budget) + "," + str(best_c)
    with open("out/hyper_asmacag_mcts_" + str(budget) + ".txt", "w") as f:
        f.write(out_str + " \n")


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
        elif algorithm == "mcts":
            do_asmacag_mcts(budget)



