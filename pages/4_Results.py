"""
Results and Recommendations Page
"""

import plotly.graph_objects as go
import streamlit as st
from utils.config import (
    ORGANIZATION_SCORING_PATH,
    TECHNICAL_SCORING_PATH,
    LEGAL_SCORING_PATH,
    AMBITION_SCORING_PATH,
    QUESTIONS_CACHE_KEY,
)
from utils.loader import load_question_collection
from utils.navigation import add_navigation_buttons

SCORING_CATEGORIES = [ORGANIZATION_SCORING_PATH, TECHNICAL_SCORING_PATH, LEGAL_SCORING_PATH, AMBITION_SCORING_PATH]

BADGE_COLOR_MAP = {
    "red": "#FF4B4B",
    "yellow": "#FACA2B",
    "green": "#21C354",
    "violet": "#7B61FF",
    "blue": "#1C83E1",
    "orange": "#FF8700",
}

# Redirect to Introduction page on uninitialized app
if st.session_state.get("questions") is None:
    st.switch_page("Introduction.py")


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


def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    for scoring_category in SCORING_CATEGORIES:
        question_collection = load_question_collection(str(scoring_category))
        collection_score = question_collection.calculate_score(st.session_state[QUESTIONS_CACHE_KEY])

        st.subheader(question_collection.header)

        score_bucket = question_collection.get_score_response(collection_score.normalized_weighted_score)
        if score_bucket:
            st.badge(score_bucket.header, color=score_bucket.color, width="stretch")
            st.write(score_bucket.description)
        else:
            st.error(f"Score '{collection_score}' is out of bounds. Please check score thresholds")

        if question_collection.thresholds:
            st.plotly_chart(
                render_score_bar(collection_score.normalized_weighted_score, question_collection.thresholds),
                use_container_width=True,
            )

        # Show detailed breakdown
        with st.expander("Show detailed scoring breakdown"):
            scored_questions = []
            for qid in question_collection.question_ids:
                q = st.session_state[QUESTIONS_CACHE_KEY][qid]
                response_score = q.get_response_score()
                if response_score is not None:
                    scored_questions.append((q, response_score * q.importance_score))

            positive = [(q, wc) for q, wc in scored_questions if wc > 0]
            negative = [(q, wc) for q, wc in scored_questions if wc < 0]

            if positive:
                st.markdown("**Responses contributing positively**")
                for q, _ in positive:
                    st.write(f"{q.question_text}")
                    st.write(f"- Your answer: {q.user_response}")

            if negative:
                st.markdown("**Responses contributing negatively**")
                for q, _ in negative:
                    st.write(f"{q.question_text}")
                    st.write(f"- Your answer: {q.user_response}")

    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
