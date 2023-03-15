import math
import sys
from typing import List
import scipy.stats as ss

from games.asmacag import AsmacagGameParameters, AsmacagForwardModel, AsmacagFitnessEvaluator, AsmacagGame
from games import Game
from games.hero_academy import HeroAcademyGameParameters, HeroAcademyForwardModel, HeroAcademyGame
from games.tank_war import TankWarGameParameters, TankWarForwardModel, TankWarGame
from players import Player, RandomPlayer, GreedyActionPlayer, MontecarloTreeSearchPlayer, OnlineEvolutionPlayer
from heuristics import SimpleHeuristic
from heuristics import Heuristic
from utils.configuration_reader import ConfigurationReader


def get_game(game_name: str) -> 'Game':
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
    player = None
    if player_name == "random":
        player = RandomPlayer()
    elif player_name == "greedy":
        player = GreedyActionPlayer(heuristic)
    elif player_name == "mcts":
        c = conf.get("c")
        player = MontecarloTreeSearchPlayer(heuristic, c)
    elif player_name == "oe":
        population_size = conf.get("population_size")
        mutation_rate = conf.get("mutation_rate")
        survival_rate = conf.get("survival_rate")
        player = OnlineEvolutionPlayer(heuristic, population_size, mutation_rate, survival_rate)
    return player


def get_heuristic(heuristic_name: str) -> 'Heuristic':
    heuristic = None
    if heuristic_name == "simple":
        heuristic = SimpleHeuristic()
    return heuristic


def run_n_games(gm: 'Game', pl1: 'Player', pl2: 'Player', n_gms: int,
                budget: int, verbose: bool, enforce_time: bool) -> List[int]:
    wins1 = 0
    wins2 = 0
    ties = 0
    for i in range(n_gms):
        if (i+1) % max(n_gms//10, 1) == 0:
            print(str((i+1)*(100/n_gms)) + "% ", end="")

        gm.run(pl1, pl2, budget, verbose, enforce_time)

        if game.get_winner() == 0:
            wins1 += 1
        elif game.get_winner() == 1:
            wins2 += 1
        else:
            ties += 1
    print("")
    return [wins1, wins2, ties]


def actualize_points(results: List[int], points: List[float]) -> None:
    w1, w2, ties = results
    points[0] += w1
    points[1] += w2
    points[0] += ties / 2
    points[1] += ties / 2


def stat_test(point1, point2, n):
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

    game = get_game(game_name)
    heuristic = get_heuristic(heuristic_name)
    player1 = get_player(player1_name, heuristic, conf)
    player2 = get_player(player2_name, heuristic, conf)

    print("Game           : {}".format(game_name))
    print("Heuristic      : {}".format(heuristic_name))
    print("Player1        : {}".format(player1_name))
    print("Player2        : {}".format(player2_name))
    print("Number of games: {}".format(n_games))

    points = [0, 0]
    results = run_n_games(game, player1, player2, int(n_games/2), budget, verbose, enforce_time)
    actualize_points(results, points)
    results = run_n_games(game, player2, player1, int(n_games/2), budget, verbose, enforce_time)
    actualize_points(results, points)

    if points[0] > points[1]:
        p_value = stat_test(points[0], points[1], n_games)
    else:
        p_value = stat_test(points[1], points[0], n_games)

    print("Player 1 got   : {} points ".format(points[0]))
    print("Player 2 got   : {} points ".format(points[1]))
    print("Two-proportion z-test (0.05): {}".format(p_value))

    if points[0] > points[1]:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player1_name, player2_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player1_name, player2_name))
    else:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player2_name, player1_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player2_name, player1_name))
