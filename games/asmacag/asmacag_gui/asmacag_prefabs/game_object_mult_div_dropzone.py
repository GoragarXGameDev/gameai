# Asmacag backend stuff
from games.asmacag import AsmacagCardType

# GUI prefabs and components
from gui_framework.components import *
from games.asmacag.asmacag_gui.asmacag_components import CardDraggableTarget
from gui_framework.basic_prefabs.game_object import GameObject

# Pygame stuff
import pygame
from pygame import Color

CARD_WIDTH = 24
CARD_HEIGHT = 32
CARD_SPACING = 4
DROPZONE_OFFSET = 2
DROPZONE_SPRITE = 'games/asmacag/asmacag_gui/assets/mult_dropzone.png'


class GO_MultDivDropzone(GameObject):
    def __init__(self, scene, name="", parent=None, width:int=0,
                 height:int=0, max_objects=1, use_color=False):
        super().__init__(scene, name, parent)
        self.width = width
        self.height = height
        self.add_component(Collider(self, width, height))
        self.add_component(SpriteRenderer(self))
        self.add_component(HorizontalLayout(self,
                                            cell_width=CARD_WIDTH,
                                            spacing_x=- CARD_WIDTH + 8,
                                            padding=2,
                                            adaptable_size=True))
        accepted_cards = [AsmacagCardType.MULT2.value, AsmacagCardType.DIV2.value]
        self.add_component(CardDraggableTarget(self, accepted_cards, width=width, height=height, max_objects=max_objects))
        if use_color:
            self.set_color()
        else:
            self.set_sprite()

    def set_sprite(self):
        sprite = pygame.image.load(DROPZONE_SPRITE)
        self.get_component(SpriteRenderer).set_sprite(sprite)

    def set_color(self, color=Color(128, 128, 128)):
        sprite = pygame.Surface((self.width, self.height))
        sprite.fill(color)
        self.get_component(SpriteRenderer).set_sprite(sprite)



