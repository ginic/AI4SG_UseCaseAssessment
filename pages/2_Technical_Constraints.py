"""
Technical Constraints Assessment Page
"""

import streamlit as st
from utils.config import TECHNICAL_QUESTIONS_PATH
from utils.navigation import add_navigation_buttons
from utils.question_renderer import question_interaction_section


def main():
    st.title("Technical Constraints")
    st.write("Assessment of technical capabilities and constraints for AI/ML projects.")

    try:
        question_interaction_section(TECHNICAL_QUESTIONS_PATH)
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Add navigation buttons
    add_navigation_buttons("Technical Constraints")


if __name__ == "__main__":
    main()
