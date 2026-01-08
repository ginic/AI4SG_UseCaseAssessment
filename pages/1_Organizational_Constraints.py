"""
Organizational Constraints Assessment Page
"""

import streamlit as st

from utils.config import ORGANIZATIONAL_QUESTIONS_PATH
from utils.navigation import add_navigation_buttons
from utils.question_renderer import question_interaction_section

# Redirect to Introduction page on uninitialized app
if st.session_state.get("questions") is None:
    st.switch_page("Introduction.py")

def main():
    st.title("Organizational Constraints")
    st.write("Assessment of organizational readiness and constraints for AI/ML projects.")

    # Load organizational questions
    try:
        question_interaction_section(ORGANIZATIONAL_QUESTIONS_PATH)

    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Add navigation buttons
    add_navigation_buttons("Organizational Constraints")


if __name__ == "__main__":
    main()
