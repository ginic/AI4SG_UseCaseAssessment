"""
Utility functions for loading questions from JSON files.
"""

import json
from pathlib import Path
from utils.models import QuestionCollection


def load_questions(json_file_path: str) -> QuestionCollection:
    """
    Load questions from a JSON file and parse into a QuestionCollection.

    Args:
        json_file_path: Path to the JSON file containing questions

    Returns:
        QuestionCollection: Parsed and validated question collection

    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        ValueError: If the JSON is invalid or doesn't match the schema
    """
    file_path = Path(json_file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Question file not found: {json_file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    return QuestionCollection(**data)
