"""
Results and Recommendations Page
"""

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
from utils.question_renderer import build_contributions_table
from utils.visualization import render_score_bar

SCORING_CATEGORIES = [ORGANIZATION_SCORING_PATH, TECHNICAL_SCORING_PATH, LEGAL_SCORING_PATH, AMBITION_SCORING_PATH]

# Redirect to Introduction page on uninitialized app
if st.session_state.get("questions") is None:
    st.switch_page("Introduction.py")


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
                width="content",
            )

        # Show detailed breakdown
        with st.expander("Show detailed scoring breakdown"):
            question_lookup = st.session_state[QUESTIONS_CACHE_KEY]
            positive = [(qid, s) for qid, s in collection_score.question_contributions if s > 0]
            negative = [(qid, s) for qid, s in collection_score.question_contributions if s < 0]
            neutral = [(qid, s) for qid, s in collection_score.question_contributions if s == 0]

            if positive:
                st.markdown("**Responses contributing to a higher score**")
                st.dataframe(build_contributions_table(positive, question_lookup), width="content", hide_index=True)

            if negative:
                st.markdown("**Responses contributing to a lower score**")
                st.dataframe(build_contributions_table(negative, question_lookup), width="content", hide_index=True)

            if neutral:
                st.markdown("**Neutral responses**")
                st.dataframe(build_contributions_table(neutral, question_lookup), width="content", hide_index=True)

    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
