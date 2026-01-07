"""
Organizational Constraints Assessment Page
"""

import streamlit as st
from utils.loader import load_questions
from utils.config import ORGANIZATIONAL_QUESTIONS_PATH, SESSION_ORGANIZATIONAL_RESPONSES


def main():
    st.title("Organizational Constraints")
    st.write("Assessment of organizational readiness and constraints for AI/ML projects.")

    # Load organizational questions
    try:
        question_collection = load_questions(str(ORGANIZATIONAL_QUESTIONS_PATH))
        st.success(f"Loaded {len(question_collection.questions)} questions")

        # Initialize session state for organizational responses if not exists
        if SESSION_ORGANIZATIONAL_RESPONSES not in st.session_state:
            st.session_state[SESSION_ORGANIZATIONAL_RESPONSES] = {}

    except FileNotFoundError as e:
        st.error(f"Error loading questions: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
