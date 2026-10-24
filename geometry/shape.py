from .nodes import Node
from .rectangle import Rectangle
import numpy as np
from scipy.optimize import fsolve


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
    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    if a2 + c2 > a1 or a3 + c3 > a1:
        raise ValueError("некорректные размеры сечения")
    center = build_shape(params).center
    Xe = force_node.x - center.x
    Ye = force_node.y - center.y

    c2_old = c2
    c3_old = c3
    b2_old = b2
    b3_old = b3
    a2_old = a2
    a3_old = a3

    if Xe < 0 and Ye >= 0:
        c2 = a1 - a2 - c2
        c3 = a1 - a3 - c3

    elif Xe < 0 and Ye < 0:
        b2 = b3_old
        b3 = b2_old
        a2 = a3_old
        a3 = a2_old
        c2 = a1 - a3_old - c3_old
        c3 = a1 - a2_old - c2_old

    elif Xe >= 0 and Ye < 0:
        b2 = b3_old
        b3 = b2_old
        a2 = a3_old
        a3 = a2_old
        c2 = c3_old
        c3 = c2_old

    A_full = a1 * b1 + a2 * b2 + a3 * b3
    gravity_center_X = (a2 * b2 * (a2 / 2 + c2) + a1 * b1 * a1 / 2 + a3 * b3 * (a3 / 2 + c3)) / A_full
    gravity_center_Y = (a2 * b2 * (b2 / 2 + b1 + b3) + a1 * b1 * (b1 / 2 + b3) + a3 * b3 * b3 / 2) / A_full

    Xc = gravity_center_X + abs(Xe)
    Yc = gravity_center_Y + abs(Ye)

    object_1 = (a1, b1, 0, b3)  # ширина, высота, смещение по X, смещение по Y левого нижнего угла
    object_2 = (a2, b2, c2, b1 + b3)
    object_3 = (a3, b3, c3, 0)
    objects = [object_1, object_2, object_3]

    limit_x_max = a1
    limit_y_max = b1 + b2 + b3

    initial_guesses = [(max(2 * Xc - limit_x_max, 0),
                        max(2 * Yc - limit_y_max, 0))]


    def geo_params(part, position, x0, y0):
        a, b, cx, cy = objects[part - 1]
        if position == 1:    # входит полностью
            area = a * b
            s_y = area * (cx + a / 2)
            s_x = area * (cy + b / 2)
        elif position == 2:  # не входит совсем
            area = s_y = s_x = 0
        elif position == 3:  # входит правая часть
            area = (a + cx - x0) * b
            s_y = area * (a + cx + x0) / 2
            s_x = area * (cy + b / 2)
        elif position == 4:  # входит верхняя часть
            area = a * (cy + b - y0)
            s_y = area * (cx + a / 2)
            s_x = area * (y0 + cy + b) / 2
        elif position == 5:  # входит правая верхняя часть
            area = (a + cx - x0) * (cy + b - y0)
            s_y = area * (a + cx + x0) / 2
            s_x = area * (y0 + cy + b) / 2
        else:
            raise ValueError(f"Неизвестная позиция: {position}")
        return area, s_y, s_x

    def answer_is_real(part, position, x, y):
        a, b, cx, cy = objects[part - 1]
        if position == 1:
            return 0 <= x <= cx and 0 <= y <= cy
        elif position == 2:
            return x >= cx + a or y >= cy + b
        elif position == 3:
            return cx <= x <= cx + a and 0 <= y <= cy
        elif position == 4:
            return 0 <= x <= cx and cy <= y <= cy + b
        elif position == 5:
            return cx <= x <= cx + a and cy <= y <= cy + b
        else:
            raise ValueError(f"Неизвестная позиция: {position}")

    def deviation(v, i, n, m):
        x0, y0 = v
        area1, s_y1, s_x1 = geo_params(1, i, x0, y0)
        area2, s_y2, s_x2 = geo_params(2, n, x0, y0)
        area3, s_y3, s_x3 = geo_params(3, m, x0, y0)

        area = area1 + area2 + area3
        s_x = s_x1 + s_x2 + s_x3
        s_y = s_y1 + s_y2 + s_y3

        if area:
            return s_y / area - Xc, s_x / area - Yc
        return 1000, 1000

    answers = []

    for i in range(1, 6):
        for n in range(1, 6):
            for m in range(1, 6):

                for ig in initial_guesses:
                    sol, info, ier, msg = fsolve(deviation, ig, args=(i, n, m), full_output=True)
                    if ier != 1:
                        continue

                    fx, fy = float(sol[0]), float(sol[1])

                    if not (0 <= fx <= limit_x_max and 0 <= fy <= limit_y_max and fx < Xc and fy < Yc):
                        continue  # вне сечения

                    if not (answer_is_real(1, i, fx, fy)
                            and answer_is_real(2, n, fx, fy)
                            and answer_is_real(3, m, fx, fy)):
                        continue  # физически невозможно

                    dev_x, dev_y = deviation(sol, i, n, m)
                    if abs(dev_x) > 0.001 or abs(dev_y) > 0.001:
                        continue  # остановился не в корне

                    answers.append((fx, fy, i, n, m))
                    break
    if not answers:
        raise ValueError("Все сечение растянуто")
    fx, fy, i, n, m = answers[0]

    red_shape = build_shape(params)
    for nd in red_shape.nodes:
        if Xe >= 0:
            nd.x = max(nd.x, fx)
        else:
            nd.x = min(nd.x, limit_x_max - fx)

        if Ye >= 0:
            nd.y = max(nd.y, fy)
        else:
            nd.y = min(nd.y, limit_y_max - fy)
    return red_shape
