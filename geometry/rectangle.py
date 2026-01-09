from .nodes import Node

class Rectangle:
    def __init__(self, shape_nodes: list[Node]):
        self.nodes = shape_nodes

    @property
    def center(self):
        x = sum(n.x for n in self.nodes) / len(self.nodes)
        y = sum(n.y for n in self.nodes) / len(self.nodes)
        return Node(x, y)

    @property
    def square(self):
        x = [n.x for n in self.nodes]
        y = [n.y for n in self.nodes]
        b = max(x) - min(x)
        h = max(y) - min(y)
        return abs(b * h)

    @property
    def static_moments(self):
        a = self.square
        c = self.center
        sx = a * c.y
        sy = a * c.x
        return sx, sy

    @property
    def inertia_moment(self):
        x = [n.x for n in self.nodes]
        y = [n.y for n in self.nodes]
        b = max(x) - min(x)
        h = max(y) - min(y)
        ix = b * h**3 / 12
        iy = h * b**3 / 12
        return ix, iy