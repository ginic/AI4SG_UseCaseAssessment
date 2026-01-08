"""
Configuration and constants for the AI4SG Use Case Assessment application.
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Data file paths
QUESTIONS_PATH = DATA_DIR / "questions.json"

# Questions around organizational friction, financial resources and buy-in
ORGANIZATIONAL_QUESTIONS_PATH = DATA_DIR / "organizational_display_questions.json"
# Questions around data maturity and IT resources
TECHNICAL_QUESTIONS_PATH = DATA_DIR / "technical_display_questions.json"
# Questions around legal risks and constraints
LEGAL_QUESTIONS_PATH = DATA_DIR / "legal_display_questions.json"

# Used in the final scoring calculations
ORGANIZATION_SCORING_PATH = DATA_DIR / "organizational_scoring_questions.json"
TECHNICAL_SCORING_PATH = DATA_DIR / "technical_scoring_questions.json"
LEGAL_SCORING_PATH = DATA_DIR / "legal_scoring_questions.json"
AMBITION_SCORING_PATH = DATA_DIR / "ambition_scoring_questions.json"

QUESTIONS_CACHE_KEY = "questions"
