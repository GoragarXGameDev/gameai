from games.observation import Observation
from heuristics.heuristic import Heuristic

class SimpleHeuristic(Heuristic):
    """Defines a simple reward for the current player."""
    
    def get_reward(self, observation: 'Observation'):
        """Returns a reward for the current player."""
        if observation.current_turn == 0:
            return observation.player_0_score - observation.player_1_score
        else:
            return observation.player_1_score - observation.player_0_score