"""
Navigation utilities for multi-page Streamlit app
"""

import streamlit as st


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
            if st.button("← Back", use_container_width=True):
                st.switch_page(previous_page["path"])

    with col3:
        # Show Next button if not on last page
        if current_index < len(PAGES) - 1:
            next_page = PAGES[current_index + 1]
            if st.button("Next →", use_container_width=True):
                st.switch_page(next_page["path"])
