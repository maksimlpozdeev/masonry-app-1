from .nodes import Node
from .rectangle import Rectangle
import numpy as np

class Shape:
    def __init__(self, figure_nodes: list[Node], shapes: list[Rectangle]):
        self.nodes = figure_nodes
        self.shapes = shapes

    @property
    def square(self):
        total_square = sum(shape.square for shape in self.shapes)
        if total_square == 0:
            raise ValueError("⛔ Все сечение растянуто")
        return total_square

    @property
    def center(self):
        total_sx, total_sy = 0, 0
        for shape in self.shapes:
            sx, sy = shape.static_moments
            total_sx += sx
            total_sy += sy
        cx = total_sy / self.square
        cy = total_sx / self.square
        return Node(cx, cy)

    @property
    def inertia_moment(self):
        total_ix, total_iy = 0, 0
        for shape in self.shapes:
            ix, iy = shape.inertia_moment
            total_ix += ix + shape.square * (shape.center.x - self.center.x) ** 2
            total_iy += iy + shape.square * (shape.center.y - self.center.y) ** 2
        return total_ix, total_iy

    @property
    def inertia_radius(self):
        ix, iy = self.inertia_moment
        return np.sqrt(ix / self.square), np.sqrt(iy / self.square)

    def average_nodes(self, tol: float = 5.0):
        def _average_close_coords(values, tol):
            values = sorted(values)
            groups = [[values[0]]]
            for v in values[1:]:
                if abs(v - groups[-1][-1]) <= tol:
                    groups[-1].append(v)
                else:
                    groups.append([v])
            return {v: sum(g)/len(g) for g in groups for v in g}

        xs = [n.x for n in self.nodes]
        ys = [n.y for n in self.nodes]
        x_map = _average_close_coords(xs, tol)
        y_map = _average_close_coords(ys, tol)
        for n in self.nodes:
            n.x = x_map[n.x]
            n.y = y_map[n.y]


def build_shape(params: dict):
    from .nodes import Node
    from .rectangle import Rectangle

    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    nd_00 = Node(0, b3)
    nd_01 = Node(c3, b3)
    nd_02 = Node(c3, 0)
    nd_03 = Node(c3 + a3, 0)
    nd_04 = Node(c3 + a3, b3)
    nd_05 = Node(a1, b3)
    nd_06 = Node(a1, b3 + b1)
    nd_07 = Node(c2 + a2, b3 + b1)
    nd_08 = Node(c2 + a2, b3 + b1 + b2)
    nd_09 = Node(c2, b3 + b1 + b2)
    nd_10 = Node(c2, b3 + b1)
    nd_11 = Node(0, b3 + b1)

    rect_1 = Rectangle([nd_00, nd_05, nd_06, nd_11])
    rect_2 = Rectangle([nd_07, nd_08, nd_09, nd_10])
    rect_3 = Rectangle([nd_01, nd_02, nd_03, nd_04])

    return Shape(
        [nd_00, nd_01, nd_02, nd_03, nd_04,
         nd_05, nd_06, nd_07, nd_08, nd_09, nd_10, nd_11],
        [rect_1, rect_2, rect_3]
    )


def reduce_shape(params: dict, force_node: Node):

    red_shape = build_shape(params)

    dir_x = "center"
    dir_y = "center"

    if force_node.x > red_shape.center.x:
        dir_x = "left"
    if force_node.x < red_shape.center.x:
        dir_x = "right"
    if force_node.y > red_shape.center.y:
        dir_y = "bottom"
    if force_node.y < red_shape.center.y:
        dir_y = "top"

    if dir_x == "left":
        x_min = 2 * force_node.x - max([n.x for n in red_shape.nodes])
        for n in red_shape.nodes:
            if n.x < x_min:
                n.x = x_min
    if dir_x == "right":
        x_max = 2 * force_node.x - min([n.x for n in red_shape.nodes])
        for n in red_shape.nodes:
            if n.x > x_max:
                n.x = x_max
    if dir_y == "bottom":
        y_min = 2 * force_node.y - max([n.y for n in red_shape.nodes])
        for n in red_shape.nodes:
            if n.y < y_min:
                n.y = y_min
    if dir_y == "top":
        y_max = 2 * force_node.y - min([n.y for n in red_shape.nodes])
        for n in red_shape.nodes:
            if n.y > y_max:
                n.y = y_max

    step = 5
    max_iter = 1000
    i = 0
    ecc = np.sqrt((force_node.x - red_shape.center.x) ** 2 +
                  (force_node.y - red_shape.center.y) ** 2)

    while ecc > 10 and i < max_iter:
        i += 1
        for n in red_shape.nodes:
            if dir_x == "left" and force_node.x > red_shape.center.x:
                if n.x == np.min([n.x for n in red_shape.nodes]):
                    n.x += step
            if dir_x == "left" and force_node.x < red_shape.center.x:
                if n.x == np.min([n.x for n in red_shape.nodes]):
                    n.x -= step

            if dir_x == "right" and force_node.x < red_shape.center.x:
                if n.x == np.max([n.x for n in red_shape.nodes]):
                    n.x -= step
            if dir_x == "right" and force_node.x > red_shape.center.x:
                if n.x == np.max([n.x for n in red_shape.nodes]):
                    n.x += step

            if dir_y == "bottom" and force_node.y > red_shape.center.y:
                if n.y == np.min([n.y for n in red_shape.nodes]):
                    n.y += step
            if dir_y == "bottom" and force_node.y < red_shape.center.y:
                if n.y == np.min([n.y for n in red_shape.nodes]):
                    n.y -= step

            if dir_y == "top" and force_node.y < red_shape.center.y:
                if n.y == np.max([n.y for n in red_shape.nodes]):
                    n.y -= step
            if dir_y == "top" and force_node.y > red_shape.center.y:
                if n.y == np.max([n.y for n in red_shape.nodes]):
                    n.y += step

        red_shape.average_nodes(tol=5)

        ecc = np.sqrt((force_node.x - red_shape.center.x) ** 2 +
                      (force_node.y - red_shape.center.y) ** 2)
    return red_shape