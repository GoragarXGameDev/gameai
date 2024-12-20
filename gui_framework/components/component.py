class Component:
    """
    A Component is a class that is stored in a Game Object.
    """
    def __init__(self, game_object):
        self.game_object = game_object  # Owner of this component.
        self.enabled = True             # Only enabled components can execute their start/update functions

    def start(self):
        """
        Called as soon as the Game Object that stores this component is created
        """
        if not self.enabled:
            return
        pass

    def update(self, delta_time):
        """
        Called every frame
        """
        if not self.enabled:
            pass