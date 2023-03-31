from games import Game
from heuristics import Heuristic
from players import Player, OnlineEvolutionPlayer, RandomPlayer, GreedyActionPlayer
from typing import List


class GameEvaluatorOE:
    def __init__(self, game: 'Game', heuristic: 'Heuristic'):
        self.game = game
        self.heuristic = heuristic

    def evaluate(self, params: List[float], n_games: int, budget: int, rounds: int) -> float:
        """Play n_games OE vs random_player and greedy_action_player and return the pct of wins of the first."""
        p1 = OnlineEvolutionPlayer(self.heuristic, int(params[0]), params[1], params[2])
        p2 = RandomPlayer()
        p3 = GreedyActionPlayer(self.heuristic)

        points = 0
        [w1, w2, ties] = self.play_games(int(n_games / 4), budget, rounds, p1, p2)
        points += w1 + ties/2
        [w1, w2, ties] = self.play_games(int(n_games / 4), budget, rounds, p2, p1)
        points += w2 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 4), budget, rounds, p1, p3)
        points += w1 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 4), budget, rounds, p3, p1)
        points += w2 + ties / 2
        return points / n_games

    def play_games(self, n_games: int, budget: int, rounds: int, p1: 'Player', p2: 'Player') -> List[int]:
        """Play n_games between p1 and p2 and return the number of wins of p1."""
        w1 = 0
        w2 = 0
        ties = 0
        for i in range(n_games):
            self.game.run(p1, p2, budget, rounds, False, True)
            if self.game.get_winner() == 0:
                w1 += 1
            elif self.game.get_winner() == 1:
                w2 += 1
            elif self.game.get_winner() == -1:
                ties += 1
        return [w1, w2, ties]


