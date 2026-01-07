"""
Technical Constraints Assessment Page
"""

import streamlit as st
from utils.loader import load_questions
from utils.config import TECHNICAL_QUESTIONS_PATH, SESSION_TECHNICAL_RESPONSES
from utils.navigation import add_navigation_buttons
from utils.question_renderer import render_question_with_help


def main():
    st.title("Technical Constraints")
    st.write("Assessment of technical capabilities and constraints for AI/ML projects.")

    # Load technical questions
    try:
        question_collection = load_questions(str(TECHNICAL_QUESTIONS_PATH))
        st.success(f"Loaded {len(question_collection.questions)} questions")

        # Initialize session state for technical responses if not exists
        if SESSION_TECHNICAL_RESPONSES not in st.session_state:
            st.session_state[SESSION_TECHNICAL_RESPONSES] = {}

        # Render questions with tooltip support
        st.markdown("---")
        for i, question in enumerate(question_collection.questions):
            response = render_question_with_help(
                question=question,
                key=f"tech_q_{question.question_id}_{i}",
                session_state_key=f"{SESSION_TECHNICAL_RESPONSES}.{question.question_id}"
            )
            # Update the question's user_response
            question.user_response = response
            st.markdown("---")

    except FileNotFoundError as e:
        st.error(f"Error loading questions: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Add navigation buttons
    st.markdown("---")
    add_navigation_buttons("Technical Constraints")


if __name__ == "__main__":
    main()
