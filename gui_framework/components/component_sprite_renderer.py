from gui_framework.components import *

# Pygame stuff
import pygame

class SpriteRenderer(Component):
    def __init__(self, game_object, sprite=None, color=(255, 255, 255)):
        """
        Parameters:
        - game_object: The GameObject this component is attached to.
        - sprite: A single sprite image (Surface).
        - color: A pygame.Color object to tint the sprite.
        """
        super().__init__(game_object)
        self.sprite = sprite
        self.surface = self.game_object.scene.surface
        self.color = color

    def update(self, delta_time):
        """
        Draw the image at current Transform position
        """
        super().update(delta_time)
        self._render()

    def _render(self):
        if self.sprite is None:
            return
        tinted_image = self.sprite.copy()
        tinted_image.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)

        # Render at the GameObject's world position
        world_pos = self.game_object.transform.world_position
        self.surface.blit(tinted_image, world_pos)

    def set_sprite(self, sprite, color=(255, 255, 255)):
        """
        Set a single sprite image and apply the color tint.
        Parameters:
            sprite: A single sprite image (Surface).
            color: A pygame.Color object to tint the sprite.
        """
        self.sprite = sprite
        self.color = color