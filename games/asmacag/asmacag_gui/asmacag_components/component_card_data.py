from games.asmacag import AsmacagCard, AsmacagCardType

import pygame

from gui_framework.components import *

CARD_WIDTH = 24
CARD_HEIGHT = 32
CARD_VALUES = ['1', '2', '3', '4', '5', '6', 'x2', '/2', 'Hidden']
CARDS_SHEET = 'games/asmacag/asmacag_gui/assets/cards_spritesheet.png'

class CardData(Component):
    """
    Component that holds an instance of an AsmacagCard class and other relevant card data.
    """
    def __init__(self, game_object, is_visible:bool, asmacag_card: 'AsmacagCard'):
        super().__init__(game_object)
        self.is_visible = is_visible
        self.asmacag_card = asmacag_card
        self.set_sprite_by_card(asmacag_card)

    def set_sprite_by_card(self, asmacag_card: 'AsmacagCard'):
        """
        Given the AsmacagCard.card_type, returns a slice of the cards' spritesheet
        """
        if self.is_visible:
            if asmacag_card.card_type.value is AsmacagCardType.NUMBER.value:
                value = str(asmacag_card.number)
            elif asmacag_card.card_type.value is AsmacagCardType.MULT2.value:
                value = 'x2'
            elif asmacag_card.card_type.value is AsmacagCardType.DIV2.value:
                value = '/2'
            else:
                value = 'Hidden'
        else:
            value = 'Hidden'

        # Get the column from the sprite sheet
        sprite_sheet_col = CARD_VALUES.index(value)
        card_sprite = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        card_sprite.blit(pygame.image.load(CARDS_SHEET), (0, 0),(sprite_sheet_col * CARD_WIDTH, 0, CARD_WIDTH, CARD_HEIGHT))

        # Fetch SpriteRenderer and set sprite to the sliced sprite.
        self.game_object.get_component(SpriteRenderer).set_sprite(card_sprite)

