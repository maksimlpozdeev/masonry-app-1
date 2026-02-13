import plotly.graph_objects as go
import numpy as np

def draw_arrow(fig, x0, y0, x1, y1, text=None):
    fig.add_shape(
        type="line",
        x0=x0, y0=y0,
        x1=x1, y1=y1,
        line=dict(width=1, color="grey"),
        label = dict(text=text, font=dict(size=16)),
    )
    for s in ["cross-thin", "line-ne"]:
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="markers",
            marker=dict(size=7, symbol=s, line=dict(width=1, color="grey")),
            showlegend=False,
            hoverinfo="skip",
        ))

def draw_shape(fig, section_nodes, style: dict):

    nodes = np.array([[n.x, n.y] for n in section_nodes])

    x = np.append(nodes[:, 0], nodes[0, 0])
    y = np.append(nodes[:, 1], nodes[0, 1])

    edgecolor = style.get("edgecolor", "black")

    line_dict = (
        dict(width=0)
        if edgecolor in (None, "none")
        else dict(color=edgecolor, width=1)
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="toself",
            fillcolor=style.get("facecolor", "rgba(0,0,0,0)"),
            line=line_dict,
            hoverinfo="skip",
            showlegend=False,
        )
    )

def draw_point(fig, node, style: dict):
    fig.add_trace(
        go.Scatter(
            x=[node.x],
            y=[node.y],
            mode="markers",
            marker=style.get("marker"),
            name=style.get("label", ""),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "x: %{x:.2f} мм<br>"
                "y: %{y:.2f} мм<extra></extra>"
            )
        )
    )

def draw_dimension(fig, params: dict):
    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    delta = 0.15 * max(a1, b1 + b2 + b3)

    vert_x = -delta
    vert_levels = [0, b3, b3 + b1, b3 + b1 + b2]
    vert_value = [b3, b1, b2]

    top_y = max(vert_levels) + delta
    top_x = [0, c2, c2 + a2]
    top_value = [c2, a2]

    bottom_y = -delta
    bottom_x = [0, c3, c3 + a3]
    bottom_value = [c3, a3]

    a1_y = bottom_y - delta

    for i, v in enumerate(vert_value):
        if v != 0:
            draw_arrow(fig, vert_x, vert_levels[i], vert_x, vert_levels[i + 1], str(v))

    for i, v in enumerate(top_value):
        if v != 0:
            draw_arrow(fig, top_x[i], top_y, top_x[i + 1], top_y, str(v))

    for i, v in enumerate(bottom_value):
        if v != 0:
            draw_arrow(fig, bottom_x[i], bottom_y, bottom_x[i + 1], bottom_y, str(v))

    draw_arrow(fig, 0, a1_y, a1, a1_y, str(a1))

def draw_notation(fig, params: dict):

    labels = {
        "b": ["b₃", "b₁", "b₂"],
        "top": ["c₂", "a₂"],
        "bottom": ["c₃", "a₃"],
    }

    a1, b1 = params["a1"], params["b1"]
    a2, b2, c2 = params["a2"], params["b2"], params["c2"]
    a3, b3, c3 = params["a3"], params["b3"], params["c3"]

    delta = 0.15 * max(a1, b1 + b2 + b3)

    vert_x = -delta
    vert_levels = [0, b3, b3 + b1, b3 + b1 + b2]

    for i, lbl in enumerate(labels["b"]):
        if vert_levels[i + 1] - vert_levels[i] != 0:
            draw_arrow(fig, vert_x, vert_levels[i], vert_x, vert_levels[i + 1], lbl)

    top_y = max(vert_levels) + delta
    top_x = [0, c2, c2 + a2]

    for i, lbl in enumerate(labels["top"]):
        if top_x[i + 1] - top_x[i] != 0:
            draw_arrow(fig, top_x[i], top_y, top_x[i + 1], top_y, lbl)

    bottom_y = -delta
    bottom_x = [0, c3, c3 + a3]

    for i, lbl in enumerate(labels["bottom"]):
        if bottom_x[i + 1] - bottom_x[i] != 0:
            draw_arrow(fig, bottom_x[i], bottom_y, bottom_x[i + 1], bottom_y, lbl)

    a1_y = bottom_y - delta
    draw_arrow(fig, 0, a1_y, a1, a1_y, "a₁")
