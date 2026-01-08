"""
Results and Recommendations Page
"""

import streamlit as st
from utils.loader import load_questions
from utils.config import ORGANIZATION_SCORING_PATH, TECHNICAL_SCORING_PATH, SESSION_ORGANIZATIONAL_RESPONSES, SESSION_TECHNICAL_RESPONSES
from utils.navigation import add_navigation_buttons


def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    # Load scoring question collections
    org_questions = load_questions(str(ORGANIZATION_SCORING_PATH))
    tech_questions = load_questions(str(TECHNICAL_SCORING_PATH))

    # Populate user responses from session state
    for q in org_questions.questions:
        response = st.session_state.get(f"{SESSION_ORGANIZATIONAL_RESPONSES}.{q.question_id}")
        q.user_response = response
    for q in tech_questions.questions:
        response = st.session_state.get(f"{SESSION_TECHNICAL_RESPONSES}.{q.question_id}")
        q.user_response = response

    # Calculate scores
    org_score = org_questions.calculate_score()
    tech_score = tech_questions.calculate_score()

    st.subheader("Organizational Score")
    st.write(f"{org_score:.2f} (weighted average)")
    st.subheader("Technical Score")
    st.write(f"{tech_score:.2f} (weighted average)")

    # Show detailed breakdown
    with st.expander("Show detailed scoring breakdown"):
        st.write("Organizational Questions:")
        for q in org_questions.questions:
            st.write(f"{q.question_text}")
            st.write(f"- Your answer: {q.user_response}")
            st.write(f"- Score: {q.get_response_score()} (Importance: {q.importance_score})")
        st.write("Technical Questions:")
        for q in tech_questions.questions:
            st.write(f"{q.question_text}")
            st.write(f"- Your answer: {q.user_response}")
            st.write(f"- Score: {q.get_response_score()} (Importance: {q.importance_score})")

    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
