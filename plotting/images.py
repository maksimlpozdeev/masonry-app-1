import plotly.graph_objects as go
from .draw import (
    draw_shape,
    draw_point,
    draw_dimension,
    draw_notation,
)
def apply_layout(fig):
    fig.update_layout(
        xaxis=dict(scaleanchor="y", visible=False, constrain="domain"),
        yaxis=dict(visible=False, constrain="domain"),
        legend=dict(orientation="h", yanchor="top", y=0.0, xanchor="left", x=0.0, font=dict(size=16)),
        margin=dict(l=20, r=20, t=20, b=20)
    )

def build_image_1(show_dimension, params, shape_nodes, center):
    fig = go.Figure()

    draw_shape(fig, shape_nodes, {"facecolor": "#f0f2f6", "edgecolor": "black"})

    if show_dimension:
        draw_dimension(fig, params)
    else:
        draw_notation(fig, params)

    draw_point(fig, center, {
        "marker": dict(size=9, symbol="cross-thin", line=dict(width=2, color="grey")),
        "label": "Центр тяжести",
    })

    apply_layout(fig)
    return fig

def build_image_2(params, shape_nodes, red_nodes, center, red_center, force_node):
    fig = go.Figure()

    draw_shape(fig, shape_nodes, {"facecolor": "#d6705c", "edgecolor": None})
    draw_shape(fig, red_nodes, {"facecolor": "#f0f2f6", "edgecolor": None})
    draw_shape(fig, shape_nodes, {"facecolor": "rgba(0,0,0,0)", "edgecolor": "black"})

    draw_point(fig, center, {
        "marker": dict(size=9, symbol="cross-thin", line=dict(width=2, color="grey")),
        "label": "Центр тяжести",
    })

    draw_point(fig, red_center, {
        "marker": dict(size=9, symbol="x-thin", line=dict(width=2, color="grey")),
        "label": "Центр тяжести сжатой зоны",
    })

    draw_point(fig, force_node, {
        "marker": dict(size=8, symbol="circle-open", color="#d6705c", line=dict(width=2)),
        "label": "Точка приложения силы",
    })

    draw_dimension(fig, params)

    apply_layout(fig)
    return fig
