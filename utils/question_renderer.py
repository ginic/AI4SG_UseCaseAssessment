"""
Utility functions for rendering questions in Streamlit with tooltip support.
"""

import streamlit as st
from utils.models import Question
from typing import Optional


def render_question(
    question: Question,
    key: str,
    session_state_key: str
) -> Optional[str | float]:
    """
    Render a question with optional tooltip description.

    Args:
        question: The Question object to render
        key: Unique key for the Streamlit widget
        session_state_key: Session state key to store the response

    Returns:
        The user's response (str for categorical, float for range)
    """
    # Display question text with optional description tooltip
    if question.description:
        st.markdown(
            f"""
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1rem; font-weight: 500;">{question.question_text}</span>
                <span style="color: #808495; margin-left: 8px; cursor: help;" title="{question.description}">ⓘ</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"**{question.question_text}**")

    # Render appropriate input widget based on question type
    if question.question_type == "categorical":
        # Extract option texts for the radio buttons
        option_texts = [option[0] for option in question.answer_options]

        # Get current value from session state or use default
        current_value = st.session_state.get(session_state_key, None)
        index = option_texts.index(current_value) if current_value in option_texts else 0

        response = st.radio(
            label="Select an option",
            options=option_texts,
            index=index,
            key=key,
            label_visibility="collapsed"
        )

    elif question.question_type == "range":
        # For range questions, determine min/max from answer_options
        scores = [score for _, score in question.answer_options]
        min_val = min(scores)
        max_val = max(scores)

        current_value = st.session_state.get(session_state_key, min_val)

        response = st.slider(
            label="Select a value",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(current_value),
            key=key,
            label_visibility="collapsed"
        )

    else:
        st.error(f"Unknown question type: {question.question_type}")
        return None

    # Store response in session state
    st.session_state[session_state_key] = response

    return response


def render_question_with_help(
    question: Question,
    key: str,
    session_state_key: str
) -> Optional[str | float]:
    """
    Alternative rendering method using Streamlit's native help parameter.
    This displays a small help icon next to the label.

    Args:
        question: The Question object to render
        key: Unique key for the Streamlit widget
        session_state_key: Session state key to store the response

    Returns:
        The user's response (str for categorical, float for range)
    """
    # Render appropriate input widget based on question type
    if question.question_type == "categorical":
        # Extract option texts for the radio buttons
        option_texts = [option[0] for option in question.answer_options]

        # Get current value from session state or use default
        current_value = st.session_state.get(session_state_key, None)
        index = option_texts.index(current_value) if current_value in option_texts else 0

        response = st.radio(
            label=question.question_text,
            options=option_texts,
            index=index,
            key=key,
            help=question.description  # Built-in Streamlit tooltip
        )

    elif question.question_type == "range":
        # For range questions, determine min/max from answer_options
        scores = [score for _, score in question.answer_options]
        min_val = min(scores)
        max_val = max(scores)

        current_value = st.session_state.get(session_state_key, min_val)

        response = st.slider(
            label=question.question_text,
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(current_value),
            key=key,
            help=question.description  # Built-in Streamlit tooltip
        )

    else:
        st.error(f"Unknown question type: {question.question_type}")
        return None

    # Store response in session state
    st.session_state[session_state_key] = response

    return response
