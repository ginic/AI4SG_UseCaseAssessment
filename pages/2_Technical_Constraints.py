"""
Technical Constraints Assessment Page
"""

from utils.config import TECHNICAL_QUESTIONS_PATH
from utils.navigation import add_question_page

title = "Technical Constraints"
intro_text = "Assessment of technical capabilities and constraints for AI/ML projects."

add_question_page(title, intro_text, TECHNICAL_QUESTIONS_PATH)
