from games.asmacag import *
from heuristics import SimpleHeuristic
from players import *

# Scene Management
from gui_framework.scenes.scene_manager import scene_manager
from games.asmacag.asmacag_gui.asmacag_main_scene import create_main_scene
from games.asmacag.asmacag_gui.asmacag_menu import create_menu

# Pygame stuff
import pygame

# Colors
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_0_COLOR = (255, 0, 0)
PLAYER_1_COLOR = (0, 255, 0)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
SCALE_FACTOR = 3

if __name__ == '__main__':
    # Players parameters
    ## Greedy Action
    greedy_hueristic = SimpleHeuristic()
    ## Greedy Turn
    greedyt_hueristic = SimpleHeuristic()
    ## Monte Carlo Tree Search
    mcts_heuristic = SimpleHeuristic()
    ## Online Evolution
    oe_heuristic = SimpleHeuristic()
    ## NTuple Bandit Online Evolution
    dimensions = [38, 38, 38]
    ntboe_heuristic = SimpleHeuristic()

    # Common parameters
    budget = 1  # time to think for the players (in seconds)
    rounds = 100  # number of rounds to play
    verbose = True  # whether to print messages
    enforce_time = True  # whether the player time to think is going to be enforced
    save_name = "out/sample_output.txt"  # where the game is going to be saved, can be None

    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    fitness_asmacag = AsmacagFitnessEvaluator(ntboe_heuristic)
    game = AsmacagGame(parameters, forward_model)

    random = RandomPlayer()
    greedy = GreedyActionPlayer(greedy_hueristic)
    greedyt = GreedyTurnPlayer(greedyt_hueristic)
    mcts = MontecarloTreeSearchPlayer(mcts_heuristic, 8)
    bbmcts = BridgeBurningMontecarloTreeSearchPlayer(mcts_heuristic, 8)
    nemcts = NonExploringMontecarloTreeSearchPlayer(mcts_heuristic)
    oe = OnlineEvolutionPlayer(oe_heuristic, 125, 0.15, 0.15)
    human_player = HumanPlayer()
    players = [human_player, greedy]                       # list of players

    #game.run(players[0], players[1], budget, rounds, verbose, enforce_time)
    #game.set_save_file(save_name)
    game.game_state.reset()

    # Create Window
    window = pygame.display.set_mode((SCREEN_WIDTH * SCALE_FACTOR, SCREEN_HEIGHT * SCALE_FACTOR))
    pygame.display.set_caption("ASMACAG: A Simple Multi-Action Card Game")
    pygame.init()

    # Create a clock to track time
    clock = pygame.time.Clock()

    # Load scenes
    scene_manager.loaded_scenes = [create_menu(), create_main_scene(game)]
    scene_manager.set_active_scene("Menu")

    # Main game loop
    running = True
    while running:
        # Calculate delta_time
        delta_time = clock.tick(60) / 1000.0

        # Clear the screen
        scene_manager.active_scene.surface.fill(BACKGROUND_COLOR)

        # Update al Game Objects of the active scene
        for game_object in scene_manager.active_scene.game_objects:
            game_object.update(delta_time)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ## Scale Window
        scaled_surface = (pygame.transform.scale(scene_manager.active_scene.surface, (SCREEN_WIDTH * SCALE_FACTOR, SCREEN_HEIGHT * SCALE_FACTOR)))

        ## Update display
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
    pygame.quit()
