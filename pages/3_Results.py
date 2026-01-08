"""
Results and Recommendations Page
"""

import streamlit as st
from utils.config import SESSION_ORGANIZATIONAL_RESPONSES, SESSION_TECHNICAL_RESPONSES
from utils.navigation import add_navigation_buttons


def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    if SESSION_TECHNICAL_RESPONSES not in st.session_state or SESSION_ORGANIZATIONAL_RESPONSES not in st.session_state:
        st.session_state[SESSION_TECHNICAL_RESPONSES] = {}
        st.write("No answers recorded yet, please go back to the previous pages")

    else:
        # Fetch questions from state
        #st.write(st.session_state[SESSION_ORGANIZATIONAL_RESPONSES])
        org_question_collection = st.session_state[SESSION_ORGANIZATIONAL_RESPONSES]
        tech_question_collection = st.session_state[SESSION_TECHNICAL_RESPONSES]

        # question_collection = st.session_state[SESSION_RESPONSES]

        # TODO: Ambition questions
        # ambition_questions = load_questions(str(AMBITION_SCORING_PATH))

        # total_responses = SESSION_ORGANIZATIONAL_RESPONSES + SESSION_TECHNICAL_RESPONSES

        # Calculate scores
        org_score = org_question_collection.calculate_score()
        tech_score = tech_question_collection.calculate_score()

        org_weighted_avg_score = org_score["weighted_average_score"]
        tech_weighted_avg_score = tech_score["weighted_average_score"]

        org_response_score = org_score["total_response_score"]
        tech_response_score = tech_score["total_response_score"]

        st.subheader("Organizational Score")
        st.write(f"{org_weighted_avg_score:.2f} (weighted average)")
        st.write(f"{org_response_score:.2f} (total score)")
        st.subheader("Technical Score")
        st.write(f"{tech_weighted_avg_score:.2f} (weighted average)")
        st.write(f"{tech_response_score:.2f} (total score)")

        # Show detailed breakdown
        with st.expander("Show detailed scoring breakdown"):
            st.write("Organizational Questions:")
            for q in org_question_collection.questions:
                st.write(f"{q.question_text}")
                st.write(f"- Your answer: {q.user_response}")
                st.write(f"- Score: {q.get_response_score()} (Importance: {q.importance_score})")
            st.write("Technical Questions:")
            for q in org_question_collection.questions:
                st.write(f"{q.question_text}")
                st.write(f"- Your answer: {q.user_response}")
                st.write(f"- Score: {q.get_response_score()} (Importance: {q.importance_score})")

    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
