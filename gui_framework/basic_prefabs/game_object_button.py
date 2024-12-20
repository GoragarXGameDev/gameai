from gui_framework.basic_prefabs.game_object import GameObject
from gui_framework.components import *

#Pygame stuff
import pygame
from pygame import Color

class GO_Button(GameObject):
    def __init__(self, scene, name="", parent=None, width=0, height=0, callback=None, text="", sprite=None):
        super().__init__(scene, name, parent)
        self.width = width
        self.height = height

        # Component References
        self.sprite_renderer = SpriteRenderer(self, sprite)
        self.add_component(self.sprite_renderer)

        self.collider = Collider(self, width, height)
        self.add_component(self.collider)

        self.text_renderer = TextRenderer(self, width=width, height=height, text=text, h_alignment="center", v_alignment="center")
        self.add_component(self.text_renderer)

        self.button = Button(self, callback)
        self.add_component(self.button)

        self.start()
        self.set_color()

    def set_color(self, color=Color(128, 128, 128)):
        sprite = pygame.Surface((self.width, self.height))
        sprite.fill(color)
        self.get_component(SpriteRenderer).set_sprite(sprite)

