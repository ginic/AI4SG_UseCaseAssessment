"""
Configuration and constants for the AI4SG Use Case Assessment application.
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Data file paths
ORGANIZATIONAL_QUESTIONS_PATH = DATA_DIR / "organizational_questions.json"
TECHNICAL_QUESTIONS_PATH = DATA_DIR / "technical_questions.json"

# Session state keys
SESSION_ORGANIZATIONAL_RESPONSES = "organizational_responses"
SESSION_TECHNICAL_RESPONSES = "technical_responses"
