"""
Results and Recommendations Page
"""

import streamlit as st
from utils.config import ORGANIZATION_SCORING_PATH, TECHNICAL_SCORING_PATH, AMBITION_SCORING_PATH, QUESTIONS_CACHE_KEY
from utils.loader import load_question_collection
from utils.navigation import add_navigation_buttons


def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    for scoring_category in [ORGANIZATION_SCORING_PATH, TECHNICAL_SCORING_PATH, AMBITION_SCORING_PATH]:
        question_collection = load_question_collection(str(scoring_category))
        collection_score = question_collection.calculate_score(st.session_state[QUESTIONS_CACHE_KEY])

        st.subheader(question_collection.header)
        st.write(f"{collection_score['weighted_average_score']:.2f} (weighted average)")
        st.write(f"{collection_score['total_response_score']:.2f} (total score)")
        # Show detailed breakdown
        with st.expander("Show detailed scoring breakdown"):
            st.write(question_collection.header)
            for qid in question_collection.question_ids:
                q = st.session_state[QUESTIONS_CACHE_KEY][qid]
                st.write(f"{q.question_text}")
                st.write(f"- Your answer: {q.user_response}")
                st.write(f"- Score: {q.get_response_score()} (Importance: {q.importance_score})")

    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
