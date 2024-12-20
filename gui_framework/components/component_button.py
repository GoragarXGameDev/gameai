from gui_framework.components import *
from gui_framework.components.component_text_renderer import TextRenderer #I should need this.

# Pygame stuff
import pygame

class Button(Component):
    def __init__(self, game_object, callback=None):
        super().__init__(game_object)
        self.callback = callback #What does this button do when pressed.
        self.is_hovered = False
        self.is_pressed = False

        # Needed components:
        self.collider = None
        self.sprite_renderer = None
        self.original_color = (255, 255, 255)
        self.text_renderer = None

    def start(self):
        super().start()
        self.collider = self.game_object.get_component(Collider)
        self.sprite_renderer = self.game_object.get_component(SpriteRenderer)
        self.text_renderer = self.game_object.get_component(TextRenderer)
        self.original_color = self.sprite_renderer.color

    def update(self, delta_time):
        super().update(delta_time)

        #Get scaled mouse position based on scene size
        mouse_pos = pygame.mouse.get_pos()[0] // self.game_object.scene.scale_factor, \
                    pygame.mouse.get_pos()[1] // self.game_object.scene.scale_factor
        #Check for hover
        self.check_hover(mouse_pos)

        #Check for clicks
        if self.is_hovered:
            self.check_pressed()

    def check_hover(self, mouse_pos):
        if self.collider.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            self.sprite_renderer.color = (
                self.original_color[0] * 0.66,
                self.original_color[1] * 0.66,
                self.original_color[2] * 0.66
            )
        else:
            self.is_hovered = False
            self.sprite_renderer.color = self.original_color

    def check_pressed(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left mouse button pressed
            if not self.is_pressed:
                self.is_pressed = True
                self.sprite_renderer.color = (
                    self.original_color[0] * 0.33,
                    self.original_color[1] * 0.33,
                    self.original_color[2] * 0.33
                )
                if self.callback is not None:
                    self.callback()
                else:
                    print("Error, no function assigned to button")
        else:
            self.is_pressed = False
