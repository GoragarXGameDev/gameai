from abc import abstractmethod
from gui_framework.components import Component

class LayoutComponent(Component):
    def __init__(self, game_object):
        super().__init__(game_object)

    @abstractmethod
    def arrange_children(self):
        pass

class HorizontalLayout(LayoutComponent):
    """
    Enforces a horizontal layout arrangement to the children of the Game Object that owns this component.
    """

    def __init__(self, game_object, container_width=0, cell_width=0,
                 padding=0, spacing_x=0, adaptable_size=False):
        super().__init__(game_object)
        self.container_width = container_width
        self.cell_width = cell_width
        self.padding = padding
        self.spacing_x = spacing_x
        self.adaptable_size = adaptable_size

    def arrange_children(self):
        num_children = len(self.game_object.children)
        if num_children == 0:
            return

        if self.adaptable_size:
            # Calculate new container size
            self.container_width = num_children * (self.cell_width + self.spacing_x) - self.spacing_x + (self.padding * 2)
            # Arrange children
            for i, child in enumerate(self.game_object.children):
                child.transform.local_position = (self.padding + (self.cell_width + self.spacing_x) * i, self.padding)

        else:
            available_space = self.container_width - (self.padding * 2)
            space_per_child = available_space / num_children
            for i, child in enumerate(self.game_object.children):
                child.transform.local_position = (self.padding + space_per_child * i, self.padding)

class VerticalLayout(LayoutComponent):
    """
    Enforces a vertical layout arrangement to the children of the Game Object that owns this component.
    """
    def __init__(self, game_object, container_width=0, cell_width=0,
                 padding=0, spacing_y=0, adaptable_size=False):
        super().__init__(game_object)
        self.container_height = container_width
        self.cell_height = cell_width
        self.padding = padding
        self.spacing_y = spacing_y
        self.adaptable_size = adaptable_size

    def arrange_children(self):
        num_children = len(self.game_object.children)
        if num_children == 0:
            return

        if self.adaptable_size:
            # Calculate new container size
            self.container_height = num_children * (self.cell_height + self.spacing_y) - self.spacing_y + (self.padding * 2)
            # Arrange children
            for i, child in enumerate(self.game_object.children):
                child.transform.local_position = (self.padding, - (self.padding + (self.cell_height + self.spacing_y) * i))

        else:
            available_space = self.container_height - (self.padding * 2)
            space_per_child = available_space / num_children
            for i, child in enumerate(self.game_object.children):
                child.transform.local_position = (self.padding, - (self.padding + space_per_child * i))


class GridLayout(LayoutComponent):
    """
        game_object: The owning game object for this layout.
        container_width (int): Width of the container.
        container_height (int): Height of the container.
        columns (int): Number of columns for grid layout. Defaults to 1.
        cell_width (int): Width of each cell in the layout.
        cell_height (int): Height of each cell in the layout.
        padding (int): Space between the container's edges and its content.
        spacing_x (int): Horizontal spacing between cells.
        spacing_y (int): Vertical spacing between cells.
        adaptable_size (bool): Whether the container should adapt its size dynamically.
    """
    def __init__(self, game_object, container_width=0, container_height=0, columns=1, cell_width=0, cell_height=0,
                 padding=0, spacing_x=0, spacing_y=0, adaptable_size=False):
        super().__init__(game_object)
        self.container_width = container_width
        self.container_height = container_height
        self.columns = columns
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.padding = padding
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.adaptable_size = adaptable_size

    def arrange_children(self):
        num_children = len(self.game_object.children)
        if num_children == 0 or self.columns <= 0:
            return

        rows = (num_children + self.columns - 1) // self.columns  # Calculate required rows
        if self.adaptable_size:
            # Calculate new container size
            container_width = self.columns * (self.cell_width + self.spacing_x) - self.spacing_x + (self.padding * 2)
            container_height = rows * (self.cell_height + self.spacing_y) - self.spacing_y + (self.padding * 2)
            self.container_width, self.container_height = container_width, container_height

        # Arrange children in grid
        for i, child in enumerate(self.game_object.children):
            col = i % self.columns
            row = i // self.columns
            x_position = self.padding + col * (self.cell_width + self.spacing_x)
            y_position = self.padding + row * (self.cell_height + self.spacing_y)
            child.transform.local_position = (x_position, y_position)

