# Asmacag backend stuff
from games.asmacag import AsmacagCard

# GUI prefabs and components
from gui_framework.components import *
from gui_framework.basic_prefabs.game_object import GameObject
from games.asmacag.asmacag_gui.asmacag_components.component_card_data import CardData

# Constants
CARD_WIDTH = 24
CARD_HEIGHT = 32

class GO_AsmacagCard(GameObject):
    """
    GameObject for Asmacag Cards.
    It has a CardData component that holds an instance of the AsmacagCard class.
    if it's a player card, a Draggable component is added.
    """
    def __init__(self, scene, name, asmacag_card:'AsmacagCard', parent=None, is_player_card:bool=False, is_visible:bool=True):
        super().__init__(scene, name, parent)

        #Add components
        self.add_component(SpriteRenderer(self, None))
        self.add_component(CardData(self, is_visible, asmacag_card))
        self.add_component(Collider(self, CARD_WIDTH, CARD_HEIGHT))

        if is_player_card:
            self.add_component(Draggable(self))

        self.start()