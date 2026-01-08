"""
Utility functions for loading questions from JSON files.
"""

import json
from pathlib import Path

import streamlit as st

from utils.models import QuestionCollection, QuestionBank
from utils.config import QUESTIONS_PATH, QUESTIONS_CACHE_KEY


def initialize_questions_cache() -> None:
    """
    Load all questions with from questions.json and cache them in the streamlit state.
    The state will store the text to display and responses.
    """
    if QUESTIONS_CACHE_KEY in st.session_state:
        # Already initialized
        return

    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(f"Questions file not found: {QUESTIONS_PATH}")

    with open(QUESTIONS_PATH, "r") as f:
        questions_data = json.load(f)

    input_questions = QuestionBank(**questions_data)

    question_lookup = {}

    for q in input_questions.questions:
        question_lookup[q.question_id] = q

    st.session_state[QUESTIONS_CACHE_KEY] = question_lookup


def load_question_collection(json_file_path: str) -> QuestionCollection:
    """
    Load questions from a category file, validate them against the questions cache and return as a QuestionCollection
    that can be used for display or scoring.

    The category file should contain a list of question IDs. Question details
    are retrieved from the cached questions dictionary.

    Args:
        json_file_path: Path to the category JSON file containing question IDs

    Returns:
        QuestionCollection: Collection of Question objects for this category

    Raises:
        FileNotFoundError: If the category file doesn't exist
        ValueError: If the JSON is invalid or question IDs are not found
    """
    file_path = Path(json_file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Category file not found: {json_file_path}")

    # Load question IDs from category file
    with open(file_path, "r") as f:
        data = json.load(f)

    questions_collection = QuestionCollection.model_validate(data)

    # Build list of Question objects from cache
    for qid in questions_collection.question_ids:
        if qid not in st.session_state[QUESTIONS_CACHE_KEY]:
            raise ValueError(
                f"Question ID '{qid}' from {file_path} not found in questions cache. Check that all questions are defined in {QUESTIONS_PATH}"
            )

    return questions_collection
