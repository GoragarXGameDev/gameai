from abc import abstractmethod
from io import TextIOWrapper
from typing import Optional
from games.action import Action
from games.forward_model import ForwardModel
from games.game_state import GameState
from games.observation import Observation
from players.player import Player
import random
import sys
import func_timeout

class Game:
    """Class that will define how to play the game"""
    
    @property
    @abstractmethod
    def game_state(self) -> 'GameState':
        """Returns the `GameState` of the game"""
        pass

    @property
    @abstractmethod
    def save_file(self) -> Optional[TextIOWrapper]:
        """Returns the file where the game is saved"""
        pass

    @property
    @abstractmethod
    def forward_model(self) -> 'ForwardModel':
        """Returns the `ForwardModel` of the game"""
        pass

# region Methods
    def reset(self) -> None:
        """Resets the `GameState` so that is ready for a new `Game`."""
        self.game_state.reset()

    def run(self, player_0: 'Player', player_1: 'Player', budget: float, verbose: bool, enforce_time: bool) -> None:
        """Runs a `Game`."""
        save_str = ""

        if self.game_state.get_game_parameters().get_seed() is None:
            seed = random.randrange(sys.maxsize)
        else:
            seed = self.game_state.get_game_parameters().get_seed()

        random.seed(seed)
        if self.save_file is not None:
            save_str += f"{seed}\n"
        if verbose:
            print("")
            print("*** ------------------------------------------------- ")
            print(f"*** Game started with seed {seed}")
            print("*** ------------------------------------------------- ")

        self.reset()

        if self.save_file is not None:
            save_str += f"{self.game_state.get_game_parameters()}\n"
            save_str += f"{player_0!s} {player_1!s}\n"
            save_str += self.add_custom_info_to_save_file()

        players = [player_0, player_1]

        # Run players' turns while the game is not finished
        while not self.forward_model.is_terminal(self.game_state):
            action = self.play_turn(players[self.game_state.get_current_turn()], budget, verbose, enforce_time)

            if self.save_file is not None:
                save_str += f"{self.game_state.get_current_turn()!s} {action!s}\n"

            self.forward_model.on_turn_ended(self.game_state)

        if self.save_file is not None:
            self.save_file.write(save_str)
            self.save_file.close()

    def play_turn(self, player: 'Player', budget: float, verbose: bool, enforce_time: bool) -> 'Action':
        """Performs a `Player` turn."""
        if verbose:
            print("")
            print("---------------------------------------- ")
            print(f"Player {self.game_state.get_cur} [{player!s}] turn")
            print("---------------------------------------- ")
            print(f"{self.game_state}\n")

        while not self.forward_model.is_turn_finished(self.game_state):
            # Observable part of the GameState
            observation = self.game_state.get_observation()

            # When enforce_time is True, the player has budget seconds to think.
            # If they take more than that, a random action is played instead.
            if enforce_time:
                try:
                    action = func_timeout.func_timeout(budget, self.think, args=[player, observation, budget])
                except func_timeout.FunctionTimedOut:
                    if verbose:
                        print("Too much time thinking!")
                    action = self.think(player, observation, budget)
            else:
                action = self.think(player, observation, budget)

            if action is None:
                if verbose:
                    print("Player didn't return an action. A random action was selected!")
                action = self.get_random_action(observation)

            if verbose:
                print(f"Player {self.game_state.current_turn} selects {action!s}.")

            self.forward_model.step(self.game_state, action)

            if verbose:
                print(f"Score: [{self.game_state.player_0_score}] - [{self.game_state.player_1_score}]")
            return action

    def think(self, player: 'Player', observation: 'Observation', budget: float) -> 'Action':
        """Requires the `Player` to decide, given an `Observation`, what `Action` to play and returns it."""
        return player.think(observation, budget)

    def get_random_action(self, observation: 'Observation') -> 'Action':
        """Returns a random valid `Action` for the state defined in the given `Observation`."""
        actions = observation.get_actions()
        return random.choice(actions)
# endregion

# region Getters and Setters
    def set_save_file(self, filename: Optional[str]) -> None:
        """Sets the save file"""
        self.save_file = open(filename, "w") if filename is not None else None

    def set_forward_model(self, forward_model: 'ForwardModel') -> None:
        """Sets the `ForwardModel` of the game"""
        self.forward_model = forward_model

    def set_game_state(self, game_state: 'GameState') -> None:
        """Sets the `GameState` of the game"""
        self.game_state = game_state

    def get_winner(self) -> int:
        """Returns the index of the `Player` that is winning the `Game`."""
        if self.game_state.player_0_score > self.game_state.player_1_score:
            return 0
        elif self.game_state.player_1_score > self.game_state.player_0_score:
            return 1
        else:
            return -1
# endregion
        
# region Overridable
    def add_custom_info_to_save_file(self):
        """Adds custom information to the save file"""
        pass
# endregion