from games import Game
from heuristics import Heuristic
from players import RandomPlayer, GreedyActionPlayer, GreedyTurnPlayer, \
    NTupleBanditOnlineEvolutionPlayer
from typing import List

from utils.game_evaluator import GameEvaluator


class GameEvaluatorNTBOE(GameEvaluator):
    def __init__(self, game: Game, heuristic: Heuristic):
        super().__init__(game, heuristic)

    def evaluate(self, params: List[float], n_games: int, budget: float, rounds: int) -> float:
        """Play n_games OE vs random_player and greedy_action_player and return the pct of wins of the first."""
        player = NTupleBanditOnlineEvolutionPlayer(self.heuristic, int(params[0]), params[1], params[2])
        p2 = RandomPlayer()
        p3 = GreedyActionPlayer(self.heuristic)
        p4 = GreedyTurnPlayer(self.heuristic)

        points = 0
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p2)
        points += w1 + ties/2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p2, player)
        points += w2 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p3)
        points += w1 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p3, player)
        points += w2 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p4)
        points += w1 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p4, player)
        points += w2 + ties / 2
        return points / n_games


