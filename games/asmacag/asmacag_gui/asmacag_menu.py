import pygame

# GUI prefabs and components.
from gui_framework.components import *
from gui_framework.basic_prefabs import *

# Scene Management
from gui_framework.scenes.scene_manager import scene_manager
from gui_framework.scenes.scene import Scene

# Screen constants (in pixels)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
MARGIN = 8
SCALE_FACTOR = 3

# Create scene
menu_scene = Scene("Menu", SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN, SCALE_FACTOR)

def create_menu():
    create_background()
    create_title()
    create_play_button()
    return menu_scene


def create_background():
    background = GameObject(menu_scene, "background")
    background.add_component(SpriteRenderer(background, pygame.image.load('games/asmacag/asmacag_gui/assets/asmacag_background.png')))


def create_title():
    # TODO: Create a proper title art instead of a simple TextRenderer.
    title = GameObject(menu_scene, "title_display")
    title.add_component(TextRenderer(title,
                                    width=256,
                                    height=64,
                                    text="ASMACAG",
                                    font_size=48,
                                    h_alignment="center"))
    title.transform.local_position = ((menu_scene.width - 256)//2, menu_scene.margin * 2)

    subtitle = GameObject(menu_scene, "subtitle")
    subtitle.add_component(TextRenderer(subtitle,
                                        width=256,
                                        height=16,
                                        text="A simple multi-action card game.",
                                        font_size=16,
                                        h_alignment="center"))
    subtitle.transform.local_position = ((menu_scene.width - 256) // 2, 72)


def create_play_button():
    # TODO: Button should probably not be just a gray box.
    play_button = GO_Button(menu_scene, "play_button", width=96, height=48, text="PLAY")
    play_button.text_renderer.set_font_size(32)
    play_button.transform.local_position = ((menu_scene.width - 96) // 2, menu_scene.height //2)

    def load_game():
        scene_manager.set_active_scene("Main")

    play_button.button.callback = load_game



