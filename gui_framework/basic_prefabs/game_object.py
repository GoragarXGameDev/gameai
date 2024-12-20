from gui_framework.components import Transform
from gui_framework.scenes.scene import Scene

class GameObject:
    """
    A Game Object is an object that exists in a Scene.
    This class is the base class of all game entities.
    Game Objects store Components. Components execute behaviours.
    """
    def __init__(self, scene:Scene, name="", parent=None):
        # General data
        self.name = self.__class__.__name__ if name == "" else name
        self.is_active = True

        self.parent = parent
        if parent:
            parent.add_child(self)              # If a parent was passed as parameter, add this object as a child of the given parent.
        self.children = []                      # Game Objects children of this Game Object
        self.scene = scene                      # Where this object 'exists'

        # Components
        self.components = []                    # A Dictionary would increase performance, but components had to be Serialized/Hashed
        self.transform = Transform(self)        # Quick access to any GameObject's transform.
        self.components.append(self.transform)  # By default, all GameObjects have a Transform.

        self.scene.add_game_object_to_scene(self)
        self.start()

    def start(self):
        """
        Calls the start function of all components of this Game Object
        """
        if not self.is_active:
            return
        for component in self.components:
            component.start()

    def update(self, delta_time):
        """
        Calls the update function of all components of this Game Object
        """
        if not self.is_active:
            return
        for component in self.components:
            component.update(delta_time)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component_type):
        """
        Returns the first instance found of a given component type.
        If no component of that type is found, returns None
        """
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def destroy(self):
        """
        Removes this object from the scene
        """
        self.scene.remove_game_object(self)

    def __str__(self):
        component_names = [comp.__class__.__name__ for comp in self.components]
        return f"{self.name}: {self.__class__.__name__} w/ components: {component_names}"