import math
from sys import argv

from joblib import Parallel, delayed

from games import Game
from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagGame
from games.hero_academy import HeroAcademyGameParameters, HeroAcademyForwardModel, HeroAcademyGame
from games.tank_war import TankWarGameParameters, TankWarForwardModel, TankWarGame
from heuristics import SimpleHeuristic
from players import MontecarloTreeSearchPlayer, BridgeBurningMontecarloTreeSearchPlayer
from utils import GameEvaluator, Ntbea


def evaluate_mcts(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = MontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def evaluate_mctsfull(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = MontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    mcts_player.set_full_rollout_on()
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def evaluate_bbmcts(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = BridgeBurningMontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def do_mcts_style(game: Game, budget: float, out_filename: str, mcts_type: str):
    evaluator = GameEvaluator(game, SimpleHeuristic())
    params_c = [round(0.35 + i*0.35, 2) for i in range(30)]
    n_games = 60
    rounds = 100
    cores = 8

    results = None
    if mcts_type == "vanilla":
        results = Parallel(n_jobs=cores)(
            delayed(evaluate_mcts)(c, evaluator, n_games, budget, rounds)
            for c in params_c
        )
    elif mcts_type == "full":
        results = Parallel(n_jobs=cores)(
            delayed(evaluate_mctsfull)(c, evaluator, n_games, budget, rounds)
            for c in params_c
        )
    elif mcts_type == "bb":
        results = Parallel(n_jobs=cores)(
            delayed(evaluate_bbmcts)(c, evaluator, n_games, budget, rounds)
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

    out_str += "Best paramameters: " + str(best_c)
    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


def do_mcts(game: Game, budget: float, out_filename: str):
    do_mcts_style(game, budget, out_filename, "vanilla")


def do_mcts_full(game: Game, budget: float, out_filename: str):
    do_mcts_style(game, budget, out_filename, "full")


def do_bbmcts(game: Game, budget: float, out_filename: str):
    do_mcts_style(game, budget, out_filename, "bb")


def do_oe(game: Game, budget: float, out_filename: str):
    evaluator = GameEvaluator(game, SimpleHeuristic())

    c_value = 1.4
    n_neighbours = 100
    n_initializations = 100
    n_games = 30
    rounds = 100
    n_iterations = 100

    param_population_size = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_survival_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    params = [param_population_size, param_mutation_rate, param_survival_rate]

    cores = 8

    ntbea = Ntbea(params, evaluator, c_value, n_neighbours, n_initializations)
    ntbea.set_cores(cores)
    ntbea.set_str_debug_on()
    ntbea.set_algorithm("oe")
    ntbea.set_algorithm_heuristic(SimpleHeuristic())
    ntbea.set_verbose_on()
    best_params = ntbea.run(n_games, budget, n_iterations, rounds)

    out_str = ntbea.get_str_debug()
    out_str += "Best paramameters: " + \
              str(param_population_size[best_params[0]]) + "," + \
              str(param_mutation_rate[best_params[1]]) + "," + \
              str(param_survival_rate[best_params[2]])

    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


def do_ntboe(game: Game, budget: float, out_filename: str):
    pass
    evaluator = GameEvaluator(game, SimpleHeuristic())

    c_value = 1.4
    n_neighbours = 100
    n_initializations = 100
    n_games = 30
    rounds = 100
    n_iterations = 100

    param_c_value = [round(0.35 + i*0.35, 2) for i in range(10)]
    param_n_neighbours = [10 + i*10 for i in range(10)]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_n_initialization = [50 + i*50 for i in range(10)]
    params = [param_c_value, param_n_neighbours, param_mutation_rate, param_n_initialization]

    cores = 8

    ntbea = Ntbea(params, evaluator, c_value, n_neighbours, n_initializations)
    ntbea.set_cores(cores)
    ntbea.set_str_debug_on()
    ntbea.set_algorithm("ntboe")
    ntbea.set_algorithm_heuristic(SimpleHeuristic())

    best_params = ntbea.run(n_games, budget, n_iterations, rounds)

    out_str = ntbea.get_str_debug()
    out_str += "Best paramameters: " + \
        str(param_c_value[best_params[0]]) + "," + \
        str(param_n_neighbours[best_params[1]]) + "," + \
        str(param_mutation_rate[best_params[2]]) + "," + \
        str(param_n_initialization[best_params[3]])

    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


if __name__ == '__main__':
    game_name = argv[1]
    algorithm = argv[2]
    budget = float(argv[3])
    out_filename = "out/hyper_" + game_name + "_" + algorithm + "_" + str(budget) + ".txt"

    game = None
    if game_name == "asmacag":
        parameters = AsmacagGameParameters()
        forward_model = AsmacagForwardModel()
        game = AsmacagGame(parameters, forward_model)
    elif game_name == "tankwar":
        parameters = TankWarGameParameters()
        forward_model = TankWarForwardModel()
        game = TankWarGame(parameters, forward_model)
    elif game_name == "heroacademy":
        parameters = HeroAcademyGameParameters()
        forward_model = HeroAcademyForwardModel()
        game = HeroAcademyGame(parameters, forward_model)

    if algorithm == "oe":
        do_oe(game, budget, out_filename)
    elif algorithm == "mcts":
        do_mcts(game, budget, out_filename)
    elif algorithm == "mctsfull":
        do_mcts_full(game, budget, out_filename)
    elif algorithm == "bbmcts":
        do_bbmcts(game, budget, out_filename)
    elif algorithm == "ntboe":
        do_ntboe(game, budget, out_filename)
