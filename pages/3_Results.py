"""
Results and Recommendations Page
"""

import streamlit as st
from utils.navigation import add_navigation_buttons
from utils.config import SESSION_TECHNICAL_RESPONSES, SESSION_ORGANIZATIONAL_RESPONSES

def calculate_score(organizational_questions):
    score = 0
    for response in organizational_questions:
        answer_options = response.answer_options
        answer_key = response.user_response
        answer_value = next((pair[1] for pair in answer_options if pair[0] == answer_key), None)
        score += answer_value
    return score

def main():
    st.title("Assessment Results")
    st.write("Summary of your assessment and recommendations for your AI/ML project.")

    # Stop if no questions answered
    if SESSION_TECHNICAL_RESPONSES not in st.session_state or SESSION_ORGANIZATIONAL_RESPONSES not in st.session_state:
        st.session_state[SESSION_TECHNICAL_RESPONSES] = {}
        st.write("No answers recorded yet, please go back to the previous pages")

    else:
        #Calculate the organizational score
        organizational_questions = st.session_state[SESSION_ORGANIZATIONAL_RESPONSES].questions
        technical_questions = st.session_state[SESSION_TECHNICAL_RESPONSES].questions

        st.write(st.session_state[SESSION_ORGANIZATIONAL_RESPONSES])

        organizational_score = calculate_score(organizational_questions)
        technical_score = calculate_score(technical_questions)

        # TODO: Add a mechanism to store negative values

        st.write(f"ORGANIZATIONAL SCORE: {organizational_score}")
        st.write(f"TECHNICAL SCORE: {technical_score}")

    # Add navigation buttons
    st.markdown("---")
    add_navigation_buttons("Results")

if __name__ == "__main__":
    main()
