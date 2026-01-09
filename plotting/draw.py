from matplotlib.patches import Polygon

def draw_notation(ax, params: dict):
    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    vert_x = -200
    vert_levels = [0, b3, b3 + b1, b3 + b1 + b2]
    vert_labels = ['$b_3$', '$b_1$', '$b_2$']
    vert_value = [b3, b1, b2]

    top_y = max(vert_levels) + 200
    top_x = [0, c2, c2 + a2]
    top_labels = ['$c_2$', '$a_2$']
    top_value = [c2, a2]

    bottom_y = -200
    bottom_x = [0, c3, c3 + a3]
    bottom_labels = ['$c_3$', '$a_3$']
    bottom_value = [c3, a3]

    a1_y = bottom_y - 200
    a1_x = [0, a1]

    # Вертикальные
    for i, lbl in enumerate(vert_labels):
        if vert_value[i] != 0:
            ax.annotate('', (vert_x, vert_levels[i]), (vert_x, vert_levels[i + 1]),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text(vert_x + 10, (vert_levels[i] + vert_levels[i + 1]) / 2,
                    lbl, ha='left', va='center', rotation=90)

    # Верхние
    for i, lbl in enumerate(top_labels):
        if top_value[i] != 0:
            ax.annotate('', (top_x[i], top_y), (top_x[i + 1], top_y),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text((top_x[i] + top_x[i + 1]) / 2,
                    top_y - 10, lbl, ha='center', va='top')

    # Нижние
    for i, lbl in enumerate(bottom_labels):
        if bottom_value[i] != 0:
            ax.annotate('', (bottom_x[i], bottom_y), (bottom_x[i + 1], bottom_y),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text((bottom_x[i] + bottom_x[i + 1]) / 2,
                    bottom_y - 10, lbl, ha='center', va='top')

    # a1
    ax.annotate('', (a1_x[0], a1_y), (a1_x[1], a1_y),
                arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(a1 / 2, a1_y - 10, '$a_1$', ha='center', va='top')

def draw_dimension(ax, params: dict):

    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    vert_x = -200
    vert_levels = [0, b3, b3 + b1, b3 + b1 + b2]
    vert_labels = ['$b_3$', '$b_1$', '$b_2$']
    vert_value = [b3, b1, b2]

    top_y = max(vert_levels) + 200
    top_x = [0, c2, c2 + a2]
    top_labels = ['$c_2$', '$a_2$']
    top_value = [c2, a2]

    bottom_y = -200
    bottom_x = [0, c3, c3 + a3]
    bottom_labels = ['$c_3$', '$a_3$']
    bottom_value = [c3, a3]

    a1_y = bottom_y - 200
    a1_x = [0, a1]

    # Вертикальные
    for i, lbl in enumerate(vert_labels):
        if vert_value[i] != 0:
            ax.annotate('', (vert_x, vert_levels[i]), (vert_x, vert_levels[i + 1]),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text(vert_x - 10,
                    (vert_levels[i] + vert_levels[i + 1]) / 2,
                    vert_value[i], ha='right', va='center', rotation=90)

    # Верхние
    for i, lbl in enumerate(top_labels):
        if top_value[i] != 0:
            ax.annotate('', (top_x[i], top_y), (top_x[i + 1], top_y),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text((top_x[i] + top_x[i + 1]) / 2,
                    top_y + 10, top_value[i], ha='center', va='bottom')

    # Нижние
    for i, lbl in enumerate(bottom_labels):
        if bottom_value[i] != 0:
            ax.annotate('', (bottom_x[i], bottom_y), (bottom_x[i + 1], bottom_y),
                        arrowprops=dict(arrowstyle='<->', color='black'))
            ax.text((bottom_x[i] + bottom_x[i + 1]) / 2,
                    bottom_y + 10, bottom_value[i], ha='center', va='bottom')

    # a1
    ax.annotate('', (a1_x[0], a1_y), (a1_x[1], a1_y),
                arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(a1 / 2, a1_y + 10, a1, ha='center', va='bottom')

def draw_point(ax, node, style: dict):
    ax.scatter(node.x, node.y, c=style["color"], marker=style["marker"], label=style["label"])

def draw_shape(ax, section_nodes, style: dict):
    import numpy as np
    nodes_draw = np.array([[n.x, n.y] for n in section_nodes])
    ax.add_patch(Polygon(nodes_draw, closed=True, facecolor=style["facecolor"], edgecolor=style["edgecolor"]))
    ax.set_xlim(-300, max(nodes_draw[:,0]) + 300)
    ax.set_ylim(-500, max(nodes_draw[:,1]) + 300)
