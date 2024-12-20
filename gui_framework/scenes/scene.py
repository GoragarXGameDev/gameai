import pygame

class Scene:
    """
    Stores GameObjects in a list. It has a size (width, height),
    can be scaled using scale_factor, and creates a pygame.Surface to draw sprites.
    """
    def __init__(self, name, width:int, height:int, margin:int, scale_factor:int=1):
        #General data
        self.name = name
        self.is_active = False
        self.game_objects = []  # List of GameObjects in the scene

        #Rendering surface
        self.width = width
        self.height = height
        self.margin = margin
        self.scale_factor = scale_factor
        self.surface = pygame.Surface((self.width, self.height))

    def add_game_object_to_scene(self, game_object):
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object):
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)

    def update(self, delta_time):
        for obj in self.game_objects:
            obj.update(delta_time)