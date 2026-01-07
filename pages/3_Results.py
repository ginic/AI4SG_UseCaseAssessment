"""
Results and Recommendations Page
"""

import streamlit as st
from utils.navigation import add_navigation_buttons


def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    # Add navigation buttons
    st.markdown("---")
    add_navigation_buttons("Results")


if __name__ == "__main__":
    main()
