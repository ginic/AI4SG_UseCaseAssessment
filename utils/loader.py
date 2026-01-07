"""
Utility functions for loading questions from JSON files.
"""

import json
from pathlib import Path
from utils.models import QuestionCollection, Question
from utils.config import QUESTIONS_PATH


# Cache for all questions - dictionary mapping question_id to Question object
_QUESTIONS_CACHE = {}


def initialize_questions_cache() -> None:
    """
    Load all questions from questions.json and cache them as Question objects.
    This should be called once at application startup.

    Raises:
        FileNotFoundError: If the questions file doesn't exist
        ValueError: If the questions data is invalid
    """
    global _QUESTIONS_CACHE

    if _QUESTIONS_CACHE:
        # Already initialized
        return

    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(f"Questions file not found: {QUESTIONS_PATH}")

    with open(QUESTIONS_PATH, 'r') as f:
        questions_data = json.load(f)

    if not isinstance(questions_data, list):
        raise ValueError(f"Expected questions.json to contain a list of questions")

    # Build cache of Question objects indexed by question_id
    for question_data in questions_data:
        try:
            question = Question(**question_data)
            _QUESTIONS_CACHE[question.question_id] = question
        except Exception as e:
            raise ValueError(f"Invalid question data for {question_data.get('question_id', 'unknown')}: {e}")


def get_questions_cache() -> dict[str, Question]:
    """
    Get the cached questions dictionary.
    Initializes the cache if not already done.

    Returns:
        dict: Dictionary mapping question_id to Question object
    """
    if not _QUESTIONS_CACHE:
        initialize_questions_cache()

    return _QUESTIONS_CACHE


def load_questions(json_file_path: str) -> QuestionCollection:
    """
    Load questions from a category file and return as a QuestionCollection.

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
    with open(file_path, 'r') as f:
        data = json.load(f)

    question_ids = data.get("questions", [])

    if not isinstance(question_ids, list):
        raise ValueError(f"Expected 'questions' to be a list in {json_file_path}")

    # Get cached questions
    questions_cache = get_questions_cache()

    # Build list of Question objects from cache
    questions = []
    for question_id in question_ids:
        if question_id not in questions_cache:
            raise ValueError(f"Question ID '{question_id}' not found in questions cache")

        questions.append(questions_cache[question_id])

    return QuestionCollection(questions=questions)
