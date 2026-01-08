"""
Utility functions for rendering questions in Streamlit with tooltip support.
"""

import streamlit as st
from typing import Optional

from utils.loader import load_question_collection
from utils.config import QUESTIONS_CACHE_KEY


def render_question_with_help(question_id: str) -> Optional[str | float]:
    """
    Renders display of the question object with a help tooltip.
    Returns the response currently selected by the user

    Args:
        question: The Question object to render

    Returns:
        The user's response (str for categorical, float for range)
    """
    # Get current value from session state or use default
    question = st.session_state[QUESTIONS_CACHE_KEY].get(question_id, None)
    current_value = question.user_response

    # Render appropriate input widget based on question type
    if question.question_type == "categorical":
        # Extract option texts for the radio buttons
        option_texts = [option[0] for option in question.answer_options]

        index = option_texts.index(current_value) if current_value in option_texts else 0

        response = st.radio(
            label=question.question_text,
            options=option_texts,
            index=index,
            help=question.description,  # Built-in Streamlit tooltip
        )

    elif question.question_type == "range":
        # For range questions, determine min/max from answer_options
        scores = [score for _, score in question.answer_options]
        min_val = min(scores)
        max_val = max(scores)

        response = st.slider(
            label=question.question_text,
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(current_value),
            help=question.description,  # Built-in Streamlit tooltip
        )

    else:
        st.error(f"Unknown question type: {question.question_type}")
        return None

    # Store response in session state
    return response


def question_interaction_section(question_collection_path):
    question_collection = load_question_collection(str(question_collection_path))

    # Render questions with tooltip support
    st.markdown("---")
    for qid in question_collection.question_ids:
        response = render_question_with_help(qid)
        st.session_state[QUESTIONS_CACHE_KEY][qid].user_response = response
        st.markdown("---")
