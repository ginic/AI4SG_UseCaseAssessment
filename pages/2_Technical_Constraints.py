"""
Technical Constraints Assessment Page
"""

import streamlit as st
from utils.loader import load_questions
from utils.config import TECHNICAL_QUESTIONS_PATH, SESSION_TECHNICAL_RESPONSES


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

    except FileNotFoundError as e:
        st.error(f"Error loading questions: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
