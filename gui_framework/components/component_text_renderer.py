from gui_framework.components import *

# Pygame stuff
import pygame

class TextRenderer(Component):
    def __init__(self, game_object, width=0, height=0,
                 text="", font_name="Arial", font_size=16, color=(255, 255, 255),
                 v_alignment="center", h_alignment="center"):
        super().__init__(game_object)
        self.surface = game_object.scene.surface
        self.width = width
        self.height = height

        self.text = text
        self.color = color

        self.font_name = font_name
        self.font_size = font_size
        pygame.font.init()
        self.font = pygame.font.SysFont(self.font_name,  self.font_size)

        self.v_alignment = v_alignment
        self.h_alignment = h_alignment

    def set_font_size(self, size:int):
        self.font_size = size
        self.font = pygame.font.SysFont(self.font_name,  self.font_size)

    def update(self, delta_time):
        super().update(delta_time)
        self.render_text()

    def render_text(self):
        # Render text as a surface
        text_surface = self.font.render(self.text, True, self.color)  # White text
        text_width, text_height = text_surface.get_size()

        # Determine horizontal position
        if self.h_alignment == "left":
            x = 0
        elif self.h_alignment == "center":
            x = (self.width - text_width) // 2
        elif self.h_alignment == "right":
            x = self.width - text_width
        else:
            raise ValueError("Invalid horizontal alignment. Use 'left', 'center', or 'right'.")

        # Determine vertical position
        if self.v_alignment == "top":
            y = 0
        elif self.v_alignment == "center":
            y = (self.height - text_height) // 2
        elif self.v_alignment == "bottom":
            y = self.height - text_height
        else:
            raise ValueError("Invalid vertical alignment. Use 'top', 'center', or 'bottom'.")

        # Blit text to screen
        self.surface.blit(text_surface, (x + self.game_object.transform.local_position[0],
                                         y + self.game_object.transform.local_position[1]))