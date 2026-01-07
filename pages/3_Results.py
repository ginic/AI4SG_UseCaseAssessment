"""
Results and Recommendations Page
"""

import streamlit as st
from utils.navigation import add_navigation_buttons
from utils.config import SESSION_TECHNICAL_RESPONSES, SESSION_ORGANIZATIONAL_RESPONSES



def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    # Stop if no questions answered
    if SESSION_TECHNICAL_RESPONSES not in st.session_state or SESSION_ORGANIZATIONAL_RESPONSES not in st.session_state:
        st.session_state[SESSION_TECHNICAL_RESPONSES] = {}
        st.write("No answers recorded yet, please go back to the previous pages")

    else:
        #Calculate the organizational score
        st.write(st.session_state[SESSION_ORGANIZATIONAL_RESPONSES])

    # Add navigation buttons
    st.markdown("---")
    add_navigation_buttons("Results")

if __name__ == "__main__":
    main()
