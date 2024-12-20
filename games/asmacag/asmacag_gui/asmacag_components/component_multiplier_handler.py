from gui_framework.components import Component
from games.asmacag.asmacag_gui.asmacag_components.component_card_data import CardData

from games.asmacag import AsmacagCardType

class MultiplierHandler(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.current_multiplier = 1
        self.start()

    def update(self, delta_time):
        # TODO: search how to make events/callbacks/trigger functions only on value changed.
        # This script should only check the multiplier area when their children change.
        self.check_multiplier_area()
        # print(f"Current multiplier is {self.current_multiplier}. This shouldn't be checked in update. Too bad.")

    def check_multiplier_area(self):
        multiplier = 1
        if len(self.game_object.children) > 0:
            for i in range(len(self.game_object.children)):
                card = self.game_object.children[i].get_component(CardData)
                if card:
                    if card.asmacag_card.card_type.value is AsmacagCardType.MULT2.value:
                        multiplier *= 2
                    elif card.asmacag_card.card_type.value is AsmacagCardType.DIV2.value:
                        multiplier /= 2
        self.current_multiplier = multiplier
