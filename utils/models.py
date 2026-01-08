"""
Pydantic models for questions and question collections.
"""

import math
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
    """Question identifier string, must be there and unique to the question"""
    question_text: str
    """Text of the question that get's explained to the user"""
    question_type: Literal["categorical", "range"] = "categorical"
    """Categorical questions are displayed as multiple choice bubbles, Range questions as a slider """
    answer_options: list[tuple[str, float]]  # (option_text, score)
    """List of possible answer texts and their contribution to the score weight"""
    description: Optional[str] = None
    """Description of the question that provides additional context to the user"""

    # Mutable fields
    importance_score: float = Field(default=1.0, ge=0)
    """Weight of this question in overall scoring"""
    user_response: Optional[str | float] = None
    """The response selected by the user"""

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

    upper: int = math.inf
    """The upper bound (exclusive) for triggering this threshold"""
    lower: int = -math.inf
    """The lower bound (inclusive) for triggering this threshold"""
    header: str
    """A short explanation that is displayed in the result badge like a header"""
    description: str | None = None
    """A detailed description that explains the context and implication of the result"""
    color: str = "blue"
    """Color of the Streamlit badge that gets displayed for this result"""


class QuestionBank(BaseModel):
    questions: list[Question]
    """A list of all questions which can be considered for scoring"""


class QuestionCollection(BaseModel):
    """
    Represents a collection of questions with scoring logic.

    Currently uses uniform weighting for question importance,
    but designed to be extensible for custom weighting strategies.
    """

    header: str | None = None
    """Brief description of the purpose for these questions"""
    question_ids: list[str]
    """List of question ids to be used for scoring"""
    thresholds: list[ThresholdResponse] | None = None
    """Define the responses that are triggered for various possible scores ranges"""

    def calculate_score(self, question_lookup: dict[str, Question]) -> dict:
        """
        Calculate the overall score based on user responses and importance weights.

        Returns:
            dict: For score calculations
            - Weighted average score, or 0.0 if no responses provided.
            - Total weighted score
            - Total response score without weights
        """
        total_weighted_score = 0.0
        total_importance = 0.0
        total_response_score = 0.0

        for qid in self.question_ids:
            question = question_lookup[qid]
            response_score = question.get_response_score()
            if response_score is not None:
                total_response_score += response_score
                total_weighted_score += response_score * question.importance_score
                total_importance += question.importance_score

        if total_importance == 0:
            weighted_average_score = 0.0
        else:
            weighted_average_score = total_weighted_score / total_importance

        return {
            "weighted_average_score": weighted_average_score,
            "total_weighted_score": total_weighted_score,
            "total_response_score": total_response_score,
        }

    def get_score_response(self, score: int) -> ThresholdResponse:
        if not self.thresholds:
            return None

        for bucket in self.thresholds:
            # Check if the score is within the range [lower, upper)
            lower_bound = bucket.lower
            upper_bound = bucket.upper

            if lower_bound <= score < upper_bound:
                return bucket

        return None
