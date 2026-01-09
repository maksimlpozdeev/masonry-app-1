import matplotlib.pyplot as plt
from .draw import draw_dimension, draw_notation, draw_point, draw_shape
from matplotlib.patches import Patch

def build_image_1(show_dimension: bool, show_notation: bool,
                  params: dict, shape_nodes, center):
    fig, ax = plt.subplots(figsize=(6,6))
    style = {"facecolor": "#f0f2f6", "edgecolor": "black"}
    draw_shape(ax, shape_nodes, style)
    if show_dimension:
        draw_dimension(ax, params)
    if show_notation:
        draw_notation(ax, params)
    draw_point(ax, center, {"marker":"+","color":"grey","label":"Центр тяжести"})
    ax.legend(loc="lower left", bbox_to_anchor=(0,-0.15), frameon=False)
    ax.set_aspect('equal')
    ax.axis("off")
    return fig

def build_image_2(shape_nodes, red_nodes, center, red_center, force_node):
    fig, ax = plt.subplots(figsize=(6,6))
    draw_shape(ax, shape_nodes, {"facecolor":"#E3533680","edgecolor":"none"})
    draw_shape(ax, red_nodes, {"facecolor":"#f0f2f6","edgecolor":"none"})
    draw_shape(ax, shape_nodes, {"facecolor":"none","edgecolor":"black"})
    draw_point(ax, center, {"marker":"+","color":"grey","label":"Центр тяжести"})
    draw_point(ax, red_center, {"marker":"+","color":"black","label":"Центр тяжести сжатой зоны"})
    draw_point(ax, force_node, {"marker":".","color":"#E35336","label":"Точка приложения силы"})
    # Легенда
    handles, labels = ax.get_legend_handles_labels()
    handles.append(Patch(facecolor="#f0f2f6", edgecolor="none"))
    labels.append("Сжатая зона")
    handles.append(Patch(facecolor="#E3533680", edgecolor="none"))
    labels.append("Растянутая зона")
    ax.legend(handles=handles, labels=labels, loc="lower left", bbox_to_anchor=(0,-0.15), frameon=False)
    ax.set_aspect('equal')
    ax.axis("off")
    return fig
