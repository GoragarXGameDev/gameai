from gui_framework.components import *
from gui_framework.components.component_layouts import HorizontalLayout

# Pygame stuff
import pygame

class Draggable(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.was_mouse_button_pressed = None
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.collider = None

    def start(self):
        """
        Requires Component: Collider. If the object has no collider, it will add one.
        """
        super().start()
        self.collider = self.game_object.get_component(Collider)
        if self.collider is None:
            print(f"GameObject {self.game_object.name} has no Collider!")


    def update(self, delta_time):
        super().update(delta_time)
        mouse_pos = (
            pygame.mouse.get_pos()[0] // self.game_object.scene.scale_factor,
            pygame.mouse.get_pos()[1] // self.game_object.scene.scale_factor,
        )
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            if not self.is_dragging:
                if self.collider and self.collider.rect.collidepoint(mouse_pos):
                    self._begin_drag(mouse_pos)
            else:
                self._drag(mouse_pos)
        else:
            if self.is_dragging and self.was_mouse_button_pressed:  # Only call when button was released
                self._on_end_drag()
                self.is_dragging = False  # Reset dragging state

        self.was_mouse_button_pressed = mouse_buttons[0]

    def _begin_drag(self, at_position: tuple[int, int]):
        # Make sure no other object is being dragged before starting this one
        for obj in self.game_object.scene.game_objects:
            draggable = obj.get_component(Draggable)
            if draggable and draggable.is_dragging:
                return  # Another object is being dragged, stop this drag
        self.is_dragging = True

        # Darken the sprite of the object being dragged
        sprite_renderer = self.game_object.get_component(SpriteRenderer)
        if sprite_renderer is not None:
            sprite_renderer.color = (200, 200, 200)

        # Set the dragged object as the last active objects, therefore ensuring it's drawn on top of everything.
        # I hope list.remove and list.append do not have a cost of O(n).
        self.game_object.scene.game_objects.remove(self.game_object)
        self.game_object.scene.game_objects.append(self.game_object)

        # Calculate offset to keep initial click position on the object
        self.offset_x = self.game_object.transform.world_position[0] - at_position[0]
        self.offset_y = self.game_object.transform.world_position[1] - at_position[1]

    def _drag(self, to_position: tuple[int, int]):
        # Calculate new position based on the mouse's position and offset
        new_x = to_position[0] + self.offset_x
        new_y = to_position[1] + self.offset_y
        new_pos = (new_x, new_y)

        # Update the GameObject's position
        self.game_object.transform.set_world_position(new_pos)

    def _on_end_drag(self):
        self.is_dragging = False

        # Set sprite to full brightness
        sprite_renderer = self.game_object.get_component(SpriteRenderer)
        if sprite_renderer is not None:
            sprite_renderer.color = (255, 255, 255)

        # Check for DraggableTarget areas
        for obj in self.game_object.scene.game_objects:
            draggable_target = obj.get_component(DraggableTarget)
            if draggable_target is not None:
                if self.collider.collides_with(draggable_target.collider):  # Check for collision
                    draggable_target.snap(self.game_object)
                    return  # As soon as the object has snapped, stop further checks


class DraggableTarget(Component):
    """
    When an Object with a Draggable component ends its drag, it checks for collisions with
    Objects with a DraggableTarget component. If the collision is successful, the Draggable will
    become a child of the DraggableTarget, snapping to it.
    """
    def __init__(self, game_object, width=0, height=0, max_objects=1):
        super().__init__(game_object)
        self.collider = self.game_object.get_component(Collider)
        self.layout = self.game_object.get_component(HorizontalLayout)
        self.width = width
        self.height = height
        self.max_objects = max_objects  # Maximum number of objects this DropArea can hold

    def start(self):
        """
        Requires Component: Collider. If the object has no collider, it will add one.
        """
        super().start()
        if self.collider is None:
            print(f"GameObject {self.game_object.name} with DraggableTarget component has no Collider!")
        if self.layout is None:
            print(f"GameObject {self.game_object.name} with DraggableTarget component has no Layout!")

    def update(self, delta_time):
        super().update(delta_time)
        # Remove any objects that are being dragged again
        for other_game_object in self.game_object.children[:]:
            draggable = other_game_object.get_component(Draggable)
            if draggable and draggable.is_dragging:
                print(f"Un-snapping {other_game_object.name} from {self.game_object.name} because it is being dragged.")
                self.game_object.remove_child(other_game_object)
                self.layout.arrange_children()

    def snap(self, other_game_object):
        """
        Parents Draggable to DraggableTarget, then calls LayoutComponent.arrange_children()
        """
        if other_game_object not in self.game_object.children and len(self.game_object.children) < self.max_objects:
            print(f"Snapping {other_game_object.name} to {self.game_object.name}.")
            self.game_object.add_child(other_game_object)
            self.layout.arrange_children()