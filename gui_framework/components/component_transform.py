from gui_framework.components.component import Component

class Transform(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self._local_position = [0, 0]
        self._world_position = [0, 0]  # Cached value, recalculated when needed

    def update(self, delta_time):
        super().update(delta_time)
        self._update_world_position()

    @property
    def local_position(self):
        return self._local_position

    @local_position.setter
    def local_position(self, value):
        """
        Set the local position and update the cached world position.
        """
        self._local_position = list(value)  # Override with a new list
        self._update_world_position()

    @property
    def world_position(self):
        """
        Calculate and return the world position based on the parent's world position.
        """
        if self.game_object.parent:
            parent_world_pos = self.game_object.parent.transform.world_position
            return [
                self._local_position[0] + parent_world_pos[0],
                self._local_position[1] + parent_world_pos[1],
            ]
        return self._local_position

    def set_world_position(self, value):
        """
        Set the world position and adjust the local position based on the parent's position.
        """
        if self.game_object.parent:
            parent_world_pos = self.game_object.parent.transform.world_position
            self.local_position = [
                value[0] - parent_world_pos[0],
                value[1] - parent_world_pos[1],
            ]
        else:
            self.local_position = value

    def _update_world_position(self):
        """
        Recalculate and cache the world position based on the parent's position.
        """
        if self.game_object.parent:
            parent_world_pos = self.game_object.parent.transform.world_position
            self._world_position = [
                self._local_position[0] + parent_world_pos[0],
                self._local_position[1] + parent_world_pos[1],
            ]
        else:
            self._world_position = self._local_position