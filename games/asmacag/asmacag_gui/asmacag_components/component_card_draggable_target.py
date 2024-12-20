from games.asmacag.asmacag_gui.asmacag_components.component_card_data import CardData
from gui_framework.components import DraggableTarget

class CardDraggableTarget(DraggableTarget):
    """
    DraggableTarget that only accepts specific types of AsmacagCards.
    """
    def __init__(self, game_object, accepted_card_types, width=0, height=0, max_objects=6):
        """
        :param accepted_card_types: A set of AsmacagCardType values that are accepted by this target.
        """
        super().__init__(game_object, width=width, height=height, max_objects=max_objects)
        self.accepted_card_types = accepted_card_types

    def snap(self, other_game_object):
        """
        Snaps the other_game_object to this target if its card type is valid.
        """
        card_data = other_game_object.get_component(CardData)
        if card_data is None:
            return

        if card_data.asmacag_card.card_type.value in self.accepted_card_types:
            if other_game_object not in self.game_object.children and len(self.game_object.children) < self.max_objects:
                print(f"Snapping {other_game_object.name} to {self.game_object.name}.")
                self.game_object.add_child(other_game_object)
                self.layout.arrange_children()
        else:
            print(f"Object {other_game_object.name} is not a valid card type for this target.")