from players import *
from typing import List


class GameEvaluatorOE:
    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic

    def evaluate(self, params: List[float], n_games: int, budget: int) -> float:
        """Play n_games OE vs random_player and greedy_action_player and return the pct of wins of the first."""
        p1 = OnlineEvolutionPlayer(self.heuristic, int(params[0]), params[1], params[2])
        p2 = RandomPlayer()
        p3 = GreedyActionPlayer(self.heuristic)

        wins = 0
        wins += self.play_games(int(n_games / 4), budget, p1, p2)
        wins += self.play_games(int(n_games / 4), budget, p2, p1)
        wins += self.play_games(int(n_games / 4), budget, p1, p3)
        wins += self.play_games(int(n_games / 4), budget, p3, p1)
        return wins / (4 * int(n_games / 4))

    def play_games(self, n_games: int, budget: int, p1: Player, p2: Player) -> float:
        """Play n_games between p1 and p2 and return the number of wins of p1."""
        wins = 0
        for i in range(n_games):
            self.game.run(p1, p2, budget, False, True)
            if self.game.get_winner() == 0:
                wins += 1
            elif self.game.get_winner() == -1:
                wins += 0.5
        return wins


