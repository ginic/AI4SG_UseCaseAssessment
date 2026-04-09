"""
Visualization utilities for score display.
"""

import plotly.graph_objects as go

BADGE_COLOR_MAP = {
    "red": "#FF4B4B",
    "yellow": "#FACA2B",
    "green": "#21C354",
    "violet": "#7B61FF",
    "blue": "#1C83E1",
    "orange": "#FF8700",
}


def render_score_bar(score: float, thresholds: list) -> go.Figure:
    """Render a horizontal bar showing colored threshold intervals with a marker at the user's score."""
    fig = go.Figure()
    for threshold in thresholds:
        lower = max(threshold.lower, -1.0)
        upper = min(threshold.upper, 1.0)
        color = BADGE_COLOR_MAP.get(threshold.color, threshold.color)
        fig.add_trace(go.Bar(
            x=[upper - lower],
            base=[lower],
            y=[""],
            orientation="h",
            marker_color=color,
            marker_line_width=0,
            name=threshold.header,
            hovertemplate=f"<b>{threshold.header}</b><extra></extra>",
        ))
    fig.add_trace(go.Scatter(
        x=[score],
        y=[""],
        mode="markers+text",
        marker=dict(symbol="triangle-down", size=18, color="black"),
        text=[f"{score:.2f}"],
        textposition="top center",
        hovertemplate=f"Your score: {score:.2f}<extra></extra>",
        showlegend=False,
    ))
    fig.update_layout(
        barmode="overlay",
        height=100,
        margin=dict(l=0, r=0, t=30, b=10),
        xaxis=dict(
            range=[-1.05, 1.05],
            showgrid=False,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1<br>(challenging)", "-0.5", "0", "0.5", "1<br>(straightforward)"],
        ),
        yaxis=dict(showticklabels=False),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
