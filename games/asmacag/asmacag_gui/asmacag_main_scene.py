# Asmacag
from games.asmacag import AsmacagCardType

#Components
from gui_framework.components import *
from games.asmacag.asmacag_gui.asmacag_prefabs import *

#Prefabs
from gui_framework.basic_prefabs import *
from games.asmacag.asmacag_gui.asmacag_components import *

#Scene
from gui_framework.scenes.scene import Scene

# Pygame stuff
import pygame

# Screen constants (in pixels)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
MARGIN = 8
SCALE_FACTOR = 3
CARD_WIDTH = 24
CARD_HEIGHT = 32
CARD_SPACING = 4
DROPZONE_WIDTH = CARD_WIDTH + 4
DROPZONE_HEIGHT = CARD_HEIGHT + 4

# Create scene
main_scene = Scene("Main", SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN, SCALE_FACTOR)

def create_main_scene(game):
    create_background()
    create_board(game.game_state)
    create_multiplier_dropzones()
    create_player_0_hand(game.game_state)
    create_player_1_hand(game.game_state)
    create_ui(game.game_state)
    create_confirm_button()
    return main_scene


def create_background():
    background = GameObject(main_scene, "background")
    background.add_component(SpriteRenderer(background, pygame.image.load('games/asmacag/asmacag_gui/assets/asmacag_background.png')))


def create_board(game_state):
    # Create board object.
    board = GameObject(main_scene, "board")

    # Create grid layout, store reference.
    board_grid_layout = GridLayout(board,
                                   cell_width=CARD_WIDTH,
                                   cell_height=CARD_HEIGHT,
                                   spacing_x=CARD_SPACING * 3,
                                   spacing_y=CARD_SPACING * 3,
                                   columns= 7,
                                   adaptable_size=True)
    board.add_component(board_grid_layout)

    # Get the board cards. For each card, create a dropzone and add the card.
    board_cards = game_state.board.cards
    for i, card in enumerate(board_cards):
        dropzone = GO_BaseDropzone(main_scene, f"dropzone_{i}", board, width=CARD_WIDTH + 4, height=CARD_HEIGHT + 4)
        dropzone.get_component(LayoutComponent).spacing_x = -CARD_WIDTH + CARD_SPACING * 2

        new_card = GO_AsmacagCard(main_scene, f"board_card_{i}", card, parent=dropzone)
        new_card.get_component(SpriteRenderer).color = (200, 200, 200)
        dropzone.get_component(LayoutComponent).arrange_children()

    #Set position, rearrange children
    board_grid_layout.arrange_children()
    x_pos = (main_scene.width - board_grid_layout.container_width) // 2
    y_pos = (main_scene.height - board_grid_layout.container_height) // 2
    board.transform.local_position = (x_pos, y_pos)


def create_confirm_button():
    confirm_button = GO_Button(main_scene, "confirm_button", width=64, height=24, text="Confirm")
    confirm_button.transform.local_position = (
        main_scene.width - main_scene.margin - confirm_button.width,
        main_scene.height - main_scene.margin - confirm_button.height)

    def confirm_callback():
        print("Some call to the 'backend' should be done here.")

    confirm_button.button.callback = confirm_callback


def create_player_0_hand(game_state):
    #Create object. Using Dropzone prefab as a base, since it uses the same exact components.
    player_0_hand = GO_BaseDropzone(main_scene, "player_0_hand", width=DROPZONE_WIDTH * 9, height=DROPZONE_HEIGHT, max_objects=9)
    # The hand accepts all cards. Modify prefab accepted cards
    player_0_hand.get_component(CardDraggableTarget).accepted_cards =\
        [AsmacagCardType.NUMBER.value, AsmacagCardType.DIV2.value, AsmacagCardType.MULT2.value]
    # Modify prefab sprite
    player_0_hand.get_component(SpriteRenderer).sprite =(
        pygame.image.load('games/asmacag/asmacag_gui/assets/player_0_hand.png'))

    # Create Cards
    player_0_cards = game_state.player_0_hand.cards
    for i, card in enumerate(player_0_cards):
        GO_AsmacagCard(main_scene,f"player_0_card_{i}", card, parent=player_0_hand, is_player_card=True)
    player_0_hand.get_component(LayoutComponent).arrange_children()

    # Move object to position
    x_pos = (main_scene.width - player_0_hand.width) // 2
    y_pos = (main_scene.height - CARD_HEIGHT - main_scene.margin)
    player_0_hand.transform.local_position = (x_pos, y_pos)


def create_player_1_hand(game_state):
    # Create object
    player_1_hand = GameObject(main_scene, "player_1_hand")
    player_1_hand.add_component(HorizontalLayout(player_1_hand, cell_width=CARD_WIDTH, spacing_x=CARD_SPACING, padding=2, adaptable_size=True))
    player_1_hand.add_component(SpriteRenderer(player_1_hand, pygame.image.load(
        'games/asmacag/asmacag_gui/assets/player_1_hand.png')))

    # Create Cards
    player_1_cards = game_state.player_0_hand.cards
    for i, card in enumerate(player_1_cards):
        GO_AsmacagCard(main_scene, f"player_0_card_{i}", card, parent=player_1_hand, is_player_card=False, is_visible=False)
    player_1_hand.get_component(LayoutComponent).arrange_children()

    # Move object to position
    x_pos = (main_scene.width - player_1_hand.get_component(LayoutComponent).container_width) // 2
    y_pos = main_scene.margin
    player_1_hand.transform.local_position = (x_pos, y_pos)


def create_multiplier_dropzones():
    #Instantiate parent, add Grid Layout
    multiplier_dropzone = GO_MultDivDropzone(main_scene,
                                        "multiplier_dropzone",
                                             None,
                                             width=DROPZONE_WIDTH * 2,
                                             height=DROPZONE_HEIGHT,
                                             max_objects=6)


    multiplier_dropzone.add_component(MultiplierHandler(multiplier_dropzone))
    multiplier_dropzone.transform.local_position = (32, (main_scene.height - DROPZONE_HEIGHT)//2)

    #Header Sprite
    multiplier_sprite = GameObject(main_scene, "multiplier_sprite")
    multiplier_sprite.add_component(SpriteRenderer(multiplier_sprite, pygame.image.load('games/asmacag/asmacag_gui/assets/multiply_sprite.png')))
    multiplier_sprite.transform.local_position = (29, (main_scene.height // 2) - DROPZONE_HEIGHT)



#region UI

def create_player_0_score(game_state):
    player_0_score = GameObject(main_scene, "player_0_score")
    current_score = f"Player 0: {game_state.player_0_score}"
    player_0_score.add_component(TextRenderer(player_0_score, 64, 32, current_score, h_alignment="right"))
    player_0_score.transform.local_position = (main_scene.margin, main_scene.height - main_scene.margin - 32)


def create_player_1_score(game_state):
    player_1_score = GameObject(main_scene, "player_0_score")
    current_score = f"Player 1: {game_state.player_1_score}"
    player_1_score.add_component(TextRenderer(player_1_score, 64, 32, current_score, h_alignment="left"))
    player_1_score.transform.local_position = (main_scene.width - main_scene.margin - 64, main_scene.margin)


def create_turn_display(game_state):
    turn_display = GameObject(main_scene, "turn_display")
    current_turn = f"Turn {game_state.current_turn}"
    turn_display.add_component(TextRenderer(turn_display, 64, 32, current_turn, h_alignment="left"))
    turn_display.transform.local_position = (main_scene.margin, main_scene.margin)


def create_actions_display(game_state):
    actions_display = GameObject(main_scene, "actions_display")
    actions_left = f"Actions left: {game_state.get_action_points_left()}"
    actions_display.add_component(TextRenderer(actions_display, 64, 32, actions_left, h_alignment="left"))
    actions_display.transform.local_position = (main_scene.margin, main_scene.margin + 16)


def create_ui(game_state):
    create_player_0_score(game_state)
    create_player_1_score(game_state)
    create_turn_display(game_state)
    create_actions_display(game_state)

#endregion