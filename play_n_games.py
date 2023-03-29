import math
import sys
from typing import List
import scipy.stats as ss
import time
import datetime
from tqdm import tqdm
from games import Game
from players.ntuple_bandit_online_evolution import FitnessEvaluator
from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagFitnessEvaluator, AsmacagGame
from games.hero_academy import HeroAcademyGameParameters, HeroAcademyForwardModel, HeroAcademyGame
from games.tank_war import TankWarGameParameters, TankWarForwardModel, TankWarGame
from players import *
from heuristics import *
from utils import ConfigurationReader, ResultsWriter


def get_game(game_name: str) -> 'Game':
    """Given the name of the game to be played, create the corresponding game objects."""
    game = None
    if game_name == "asmacag":
        parameters = AsmacagGameParameters()
        forward_model = AsmacagForwardModel()
        game = AsmacagGame(parameters, forward_model)
    elif game_name == "heroacademy":
        parameters = HeroAcademyGameParameters()
        forward_model = HeroAcademyForwardModel()
        game = HeroAcademyGame(parameters, forward_model)
    elif game_name == "tankwar":
        parameters = TankWarGameParameters()
        forward_model = TankWarForwardModel()
        game = TankWarGame(parameters, forward_model)
    return game


def get_player(player_name: str, heuristic: 'Heuristic', conf: 'ConfigurationReader') -> 'Player':
    """Given the name of the player to be used, create the corresponding Player object."""
    player = None
    if player_name == "random":
        player = RandomPlayer()
    elif player_name == "greedy":
        player = GreedyActionPlayer(heuristic)
    elif player_name == "mcts":
        c = conf.get("c_mcts")
        player = MontecarloTreeSearchPlayer(heuristic, c)
    elif player_name == "oe":
        population_size = conf.get("population_size")
        mutation_rate = conf.get("mutation_rate_oe")
        survival_rate = conf.get("survival_rate")
        player = OnlineEvolutionPlayer(heuristic, population_size, mutation_rate, survival_rate)
    elif player_name == "ntboe":
        n_neighbours = conf.get("n_neighbours")
        mutation_rate = conf.get("mutation_rate_ntboe")
        n_initializations = conf.get("n_initializations")
        c = conf.get("c_ntboe")
        dimensions = get_dimensions(conf)
        fitness = get_fitness(conf, heuristic)
        player = NTupleBanditOnlineEvolutionPlayer(heuristic, fitness, dimensions, c,
                                                  n_neighbours, mutation_rate, n_initializations)
    return player


def get_heuristic(heuristic_name: str) -> 'Heuristic':
    """Given the heuristic name, create the corresponding Heuristic object."""
    heuristic = None
    if heuristic_name == "simple":
        heuristic = SimpleHeuristic()
    return heuristic


def get_fitness(conf: 'ConfigurationReader', heuristic: 'Heuristic') -> 'FitnessEvaluator':
    """Given the fitness evaluator name, create the corresponding FitnessEvaluator object."""
    fitness = None
    if conf.get("game_name") == "asmacag":
        fitness = AsmacagFitnessEvaluator(heuristic)
    return fitness


def get_dimensions(conf: 'ConfigurationReader') -> List[int]:
    dimensions = None
    if conf.get("game_name") == "asmacag":
        dimensions = [38, 38, 38]
    return dimensions


def run_n_games(gm: 'Game', pl1: 'Player', pl2: 'Player', n_gms: int,
                budget: int, rounds: int, verbose: bool, enforce_time: bool) -> List[int]:
    """Run n_gms games and return the number of wins for each player and the number of ties."""
    wins1 = 0
    wins2 = 0
    ties = 0
    for _ in tqdm(range(n_gms), desc="Games"):
        winner = gm.run(pl1, pl2, budget, rounds, verbose, enforce_time)
        if winner == 0:
            wins1 += 1
        elif winner == 1:
            wins2 += 1
        else:
            ties += 1
    return [wins1, wins2, ties]


def stat_test(point1: int, point2: int, n: int) -> float:
    """two-proportion z-test to compare the performance of two bots"""
    # Number of games played
    n1 = n
    n2 = n

    # Number of games won by each bot
    w1 = point1
    w2 = point2

    # Proportions of games won by each bot
    p1 = w1 / n1
    p2 = w2 / n2

    # Pooled proportion
    p = (w1 + w2) / (n1 + n2)

    # Standard error
    se = math.sqrt(p*(1-p)*(1/n1 + 1/n2))

    # z-score
    z = (p1 - p2) / se

    # Two-tailed p-value
    p_value = 2 * (1 - ss.norm.cdf(abs(z)))
    return p_value


if __name__ == '__main__':
    """ Play n matches of a game between two players."""
    """ Usage: python play_n_games.py configuration_file.json"""

    if len(sys.argv) != 2:
        print("Usage: python play_n_games.py configuration_file.json")
        sys.exit(1)

    conf = ConfigurationReader(sys.argv[1])

    game_name = conf.get("game_name")
    player1_name = conf.get("player1_name")
    player2_name = conf.get("player2_name")
    n_games = conf.get("n_games")
    heuristic_name = conf.get("heuristic_name")
    verbose = conf.get("verbose")
    enforce_time = conf.get("enforce_time")
    budget = conf.get("budget")
    rounds = conf.get("rounds")

    game = get_game(game_name)
    heuristic = get_heuristic(heuristic_name)
    player1 = get_player(player1_name, heuristic, conf)
    player2 = get_player(player2_name, heuristic, conf)

    print("Game           : {}".format(game_name))
    print("Heuristic      : {}".format(heuristic_name))
    print("Player1        : {}".format(player1_name))
    print("Player2        : {}".format(player2_name))
    print("Number of games: {}".format(n_games))

    wins1 = 0
    wins2 = 0
    ties = 0
    t0 = time.time()
    w1, w2, t = run_n_games(game, player1, player2, int(n_games/2), budget, rounds, verbose, enforce_time)
    wins1 += w1
    wins2 += w2
    ties += t

    w1, w2, t = run_n_games(game, player2, player1, int(n_games/2), budget, rounds, verbose, enforce_time)
    wins2 += w1
    wins1 += w2
    ties += t
    tf = time.time() - t0

    if wins1 > wins2:
        p_value = stat_test(wins1, wins2, n_games)
    else:
        p_value = stat_test(wins2, wins1, n_games)

    print("Player 1 won   : {} games ".format(wins1))
    print("Player 2 won   : {} games ".format(wins2))
    print("Ties           : {} games ".format(ties))
    print("Two-proportion z-test (0.05): {}".format(p_value))

    if wins1 > wins2:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player1_name, player2_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player1_name, player2_name))
    else:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player2_name, player1_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player2_name, player1_name))

    output_filename = conf.get("result_file")
    result = ResultsWriter()
    result.set("game_name", game_name)
    result.set("heuristic_name", heuristic_name)
    result.set("player1_name", player1_name)
    result.set("player2_name", player2_name)
    result.set("n_games", n_games)
    result.set("budget", budget)
    result.set("wins1", wins1)
    result.set("wins2", wins2)
    result.set("ties", ties)
    result.set("player_1_forward_model_visits", player1.get_forward_model_visits() / n_games)
    result.set("player_1_visited_states", player1.get_visited_states_count() / n_games)
    result.set("player_2_forward_model_visits", player2.get_forward_model_visits() / n_games)
    result.set("player_2_visited_states", player2.get_visited_states_count() / n_games)
    result.set("p_value", p_value)
    result.set("processing_time", tf)
    result.set("date", datetime.datetime.now().strftime("%Y-%m-%d"))
    result.set("hour", datetime.datetime.now().strftime("%H:%M:%S"))
    result.write(output_filename)
