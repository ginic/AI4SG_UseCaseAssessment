"""
Legal Constraints Assessment Page
"""

import streamlit as st
from utils.config import LEGAL_QUESTIONS_PATH
from utils.navigation import add_navigation_buttons
from utils.question_renderer import question_interaction_section


def main():
    st.title("Legal Constraints")
    st.write("Assessment of legal risks and constraints for AI/ML projects.")

    question_interaction_section(LEGAL_QUESTIONS_PATH)

    # Add navigation buttons
    add_navigation_buttons("Legal Constraints")


if __name__ == "__main__":
    main()
