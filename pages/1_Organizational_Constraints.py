"""
Organizational Constraints Assessment Page
"""

from utils.config import ORGANIZATIONAL_QUESTIONS_PATH
from utils.navigation import add_question_page

title = "Organizational Constraints"
intro_text = "Assessment of organizational readiness and constraints for AI/ML projects."

add_question_page(title, intro_text, ORGANIZATIONAL_QUESTIONS_PATH)
