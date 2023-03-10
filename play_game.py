from games.asmacag.asmacag_fitness_evaluator import AsmacagFitnessEvaluator
from games.asmacag.asmacag_forward_model import AsmacagForwardModel
from games.asmacag.asmacag_game import AsmacagGame
from games.asmacag.asmacag_game_parameters import AsmacagGameParameters
from games.hero_academy.heroac_fitness_evaluator import HeroAcademyFitnessEvaluator
from games.hero_academy.heroac_forward_model import HeroAcademyForwardModel
from games.hero_academy.heroac_game import HeroAcademyGame
from games.hero_academy.heroac_game_parameters import HeroAcademyGameParameters
from players.greedy_action_player import GreedyActionPlayer
from players.montecarlo_tree_search_player import MontecarloTreeSearchPlayer
from players.ntuple_bandit_online_evolution_player import NTupleBanditOnlineEvolutionPlayer
from players.online_evolution_player import OnlineEvolutionPlayer
from players.random_player import RandomPlayer
from heuristics.simple_heuristic import SimpleHeuristic

if __name__ == '__main__':
    # Players parameters
    ## Greedy Action
    greedy_hueristic = SimpleHeuristic()
    ## Monte Carlo Tree Search
    mcts_heuristic = SimpleHeuristic()
    ## Online Evolution
    oe_heuristic = SimpleHeuristic()
    ## NTuple Bandit Online Evolution
    dimensions = [38, 38, 38]
    ntboe_heuristic = SimpleHeuristic()

    # Common parameters
    budget = 5                                  # time to think for the players (in seconds)
    verbose = True                              # whether to print messages
    enforce_time = True                         # whether the player time to think is going to be enforced
    save_name = "out/sample_output.txt"         # where the game is going to be saved, can be None

    # ASMACAG parameters
    # parameters = AsmacagGameParameters() 
    # forward_model = AsmacagForwardModel()
    # fitness_asmacag = AsmacagFitnessEvaluator(ntboe_heuristic)
    # game = AsmacagGame(parameters, forward_model)

    # Hero Academy parameters
    parameters = HeroAcademyGameParameters() 
    forward_model = HeroAcademyForwardModel()
    fitness_heroac = HeroAcademyFitnessEvaluator(ntboe_heuristic)
    game = HeroAcademyGame(parameters, forward_model)

    # Common players
    random = RandomPlayer()
    greedy = GreedyActionPlayer(greedy_hueristic)
    mcts = MontecarloTreeSearchPlayer(mcts_heuristic, 8)
    oe = OnlineEvolutionPlayer(oe_heuristic, 125, 0.15, 0.15)

    # ASMACAG players
    # ntboe_asmacag = NTupleBanditOnlineEvolutionPlayer(ntboe_heuristic, fitness_asmacag, dimensions, 8, 5, 0.55, 1000)

    # Hero Academy players
    ntboe_heroac = NTupleBanditOnlineEvolutionPlayer(ntboe_heuristic, fitness_heroac, dimensions, 8, 5, 0.55, 1000)
    
    players = [oe, mcts]                       # list of players

    game.set_save_file(save_name)

    game.run(players[0], players[1], budget, verbose, enforce_time)

    if verbose:
        print("")
        print("*** ------------------------------------------------- ")
        if game.get_winner() != -1:
            print(f"*** The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")
        else:
            print("*** There is a Tie.")
        print("*** ------------------------------------------------- ")
    else:
        print(f"The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")