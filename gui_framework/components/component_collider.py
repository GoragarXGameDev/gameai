# Components needed for this component to work
from gui_framework.components import *

# Pygame stuff
import pygame
from pygame.rect import Rect

visualize_colliders = False

class Collider(Component):
    def __init__(self, game_object, width=0, height=0):
        super().__init__(game_object)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)  # Initialize collider as a pygame.Rect

    def start(self):
        self.match_transform_position()

    def update(self, delta_time):
        super().update(delta_time)
        self.match_transform_position()
        if visualize_colliders:
            pygame.draw.rect(self.game_object.scene.surface, (0, 255, 0), self.rect, 1)

    def match_transform_position(self):
        """
        Matches collider position to transform position
        """
        self.rect.topleft = self.game_object.transform.world_position[0], self.game_object.transform.world_position[1]

    def collides_with(self, other_collider:Rect):
        """
        Returns true if a given Rect overlaps with this object's Rect
        Parameters:
            other_collider (Rect): Rect to compare with
        """
        return self.rect.colliderect(other_collider)