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
    threshold_boundaries = set()
    for threshold in thresholds:
        lower = max(threshold.lower, -1.0)
        threshold_boundaries.add(lower)
        upper = min(threshold.upper, 1.0)
        threshold_boundaries.add(upper)
        color = BADGE_COLOR_MAP.get(threshold.color, threshold.color)
        fig.add_trace(
            go.Bar(
                x=[upper - lower],
                base=[lower],
                y=[0],
                width=[1],  # bar spans y=-0.5 to y=0.5
                orientation="h",
                marker_color=color,
                marker_line_width=0,
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Bold section label below the bar (in the bottom margin)
        fig.add_annotation(
            x=(lower + upper) / 2,
            xref="x",
            y=0,
            yref="paper",
            text=f"<b>{threshold.header}</b>",
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=12),
        )

    fig.add_trace(
        go.Scatter(
            x=[score],
            y=[0],
            mode="markers",
            marker=dict(symbol="circle", size=36, color="DarkSlateGrey"),
            hovertemplate=f"Your score: {score:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    tick_vals = sorted(threshold_boundaries)
    fig.update_layout(
        barmode="overlay",
        height=160,
        margin=dict(l=0, r=0, t=35, b=60),
        xaxis=dict(
            # range=[-1.2, 1.2],
            showgrid=False,
            tickvals=tick_vals,
            side="top",
        ),
        yaxis=dict(
            # range=[-0.5, 0.5],
            showticklabels=False,
            showgrid=False,
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
