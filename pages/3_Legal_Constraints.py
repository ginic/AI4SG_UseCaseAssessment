"""
Legal Constraints Assessment Page
"""

from utils.config import LEGAL_QUESTIONS_PATH
from utils.navigation import add_question_page

title = "Legal Constraints"
intro_text = "Assessment of legal risks and constraints for AI/ML projects."

add_question_page(title, intro_text, LEGAL_QUESTIONS_PATH)
