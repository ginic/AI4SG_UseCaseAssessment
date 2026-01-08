"""
Pydantic models for questions and question collections.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class Question(BaseModel):
    """
    Represents a single assessment question.

    Immutable fields (should not be changed after initialization):
    - question_id: Unique identifier for the question
    - question_text: The text displayed to users
    - question_type: Type of question (categorical or range)
    - answer_options: List of (option_text, score) tuples
    - description: Optional detailed description shown on mouseover

    Mutable fields (can be changed):
    - importance_score: Weight of this question in overall scoring
    - user_response: The user's answer to the question
    """

    # Immutable fields
    question_id: str
    question_text: str
    question_type: Literal["categorical", "range"] = "categorical"
    answer_options: list[tuple[str, float]]  # (option_text, score)
    description: Optional[str] = None

    # Mutable fields
    importance_score: float = Field(default=1.0, ge=0)
    user_response: Optional[str | float] = None

    model_config = {"validate_assignment": True}

    def get_response_score(self) -> Optional[float]:
        """
        Get the score associated with this question's user response.

        Returns:
            float: The score for the response, or None if no response provided
        """
        if self.user_response is None:
            return None

        if self.question_type == "range":
            # For range questions, the response itself is the score
            return float(self.user_response)

        # For categorical questions, look up the score from answer_options
        for option_text, score in self.answer_options:
            if option_text == self.user_response:
                return score

        return None


class ThresholdResponse(BaseModel):
    """
    Categorizes scores into a bucket that will decide what description of their responses
    will be displayed to the user.
    The upper and lower bound determine the scoring range that will trigger the response.
    """

    upper: int = int("inf")
    lower: int = int("-inf")
    description: str | None = None


class QuestionCollection(BaseModel):
    """
    Represents a collection of questions with scoring logic.

    Currently uses uniform weighting for question importance,
    but designed to be extensible for custom weighting strategies.
    """

    header: str | None = None
    questions: list[Question]
    threshold: list[ThresholdResponse] | None = None

    def calculate_score(self) -> float:
        """
        Calculate the overall score based on user responses and importance weights.

        Returns:
            float: Weighted average score, or 0.0 if no responses provided.
        """
        total_weighted_score = 0.0
        total_importance = 0.0

        for question in self.questions:
            response_score = question.get_response_score()
            if response_score is not None:
                total_weighted_score += response_score * question.importance_score
                total_importance += question.importance_score

        if total_importance == 0:
            return 0.0

        return total_weighted_score / total_importance

    def get_score_response(score: int) -> ThresholdResponse:
        # todo return the proper bucket for the score
        return
