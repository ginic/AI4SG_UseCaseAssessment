"""
Navigate and display pages in the multi-page Streamlit app
"""

from pathlib import Path

import streamlit as st

from utils.config import QUESTIONS_CACHE_KEY
from utils.question_renderer import question_interaction_section


# Define page order
PAGES = [
    {"name": "Introduction", "path": "Introduction.py"},
    {"name": "Organizational Constraints", "path": "pages/1_Organizational_Constraints.py"},
    {"name": "Technical Constraints", "path": "pages/2_Technical_Constraints.py"},
    {"name": "Legal Constraints", "path": "pages/3_Legal_Constraints.py"},
    {"name": "Results", "path": "pages/4_Results.py"},
]


def get_current_page_index(current_page_name: str) -> int:
    """Get the index of the current page in the page order."""
    for i, page in enumerate(PAGES):
        if page["name"] == current_page_name:
            return i
    return 0


def add_navigation_buttons(current_page_name: str):
    """
    Add Next and Back navigation buttons at the bottom of the page.

    Args:
        current_page_name: The name of the current page (should match PAGES list)
    """
    current_index = get_current_page_index(current_page_name)

    # Create columns for button layout
    col1, _, col3 = st.columns([1, 1, 1])

    with col1:
        # Show Back button if not on first page
        if current_index > 0:
            previous_page = PAGES[current_index - 1]
            if st.button("← Back", width="content", type="primary"):
                st.switch_page(previous_page["path"])

    with col3:
        # Show Next button if not on last page
        if current_index < len(PAGES) - 1:
            next_page = PAGES[current_index + 1]
            if st.button("Next →", width="content", type="primary"):
                st.switch_page(next_page["path"])


def add_question_page(page_title: str, page_intro_text: str, questions_path: Path):
    # Redirect to Introduction page on uninitialized app
    if st.session_state.get(QUESTIONS_CACHE_KEY) is None:
        st.switch_page("Introduction.py")

    st.title(page_title)
    st.write(page_intro_text)

    question_interaction_section(questions_path)

    # Add navigation buttons
    add_navigation_buttons(page_title)
