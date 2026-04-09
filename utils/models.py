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

    upper: float = math.inf
    """The upper bound of the weighted score (exclusive) for triggering this threshold"""
    lower: float = -math.inf
    """The lower bound of the weighted score (inclusive) for triggering this threshold"""
    header: str
    """A short explanation that is displayed in the result badge like a header"""
    description: str | None = None
    """A detailed description that explains the context and implication of the result"""
    color: str = "blue"
    """Color of the Streamlit badge that gets displayed for this result"""


class QuestionBank(BaseModel):
    questions: list[Question]
    """A list of all questions which can be considered for scoring"""


class ScoreResult(BaseModel):
    """Represents the scoring results computed by QuestionCollection"""

    weighted_score: float = 0.0
    """The total score of question responses weighted by question importance"""
    normalized_weighted_score: float = 0.0
    """The total weighted score normalized by the weighted maxmium (if weighted score > 0) or minimum (if weighted score <= 0)"""
    raw_response_score: float = 0.0
    """The total response score without weights. This is the sum of the raw score for each question."""
    max_weighted_score: float = 0.0
    """The maximum possible weighted score for this collection (all best answers selected)."""
    min_weighted_score: float = 0.0
    """The minimum possible weighted score for this collection (all worst answers selected)."""
    question_contributions: list[tuple[str, float]] = Field(default_factory=list)
    """Per-question (question_id, raw_weighted_contribution) pairs in collection question order."""


class QuestionScoringCollection(BaseModel):
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

    def calculate_score(self, question_lookup: dict[str, Question]) -> ScoreResult:
        """Calculates the raw and weighted score of the responses to the questions

        Args:
            question_lookup: dictionary for looking up questions and responses by question id

        Returns:
            ScoreResult: the weighted, normalized weighted, raw score, and per-question contributions
        """
        total_weighted_score = 0.0
        total_response_score = 0.0
        answered: list[tuple[str, float]] = []  # (qid, normalized_weighted_contribution)

        _, max_weighted_score = self.get_extreme_score(question_lookup)
        _, min_weighted_score = self.get_extreme_score(question_lookup, is_min=True)

        for qid in self.question_ids:
            question = question_lookup[qid]
            response_score = question.get_response_score()
            if response_score is not None:
                wc = response_score * question.importance_score
                total_response_score += response_score
                total_weighted_score += wc
                if wc > 0:
                    norm_denominator = max_weighted_score
                else:
                    norm_denominator = abs(min_weighted_score)
                answered.append((qid, wc / norm_denominator))

        # If the weighted average score is greater than 0, normalize by the maximum weighted raw score
        if total_weighted_score > 0:
            weighted_norm_denominator = max_weighted_score
        else:
            # If the weighted score is less than 0, normalize by the minimum weighted score, but keep the negative sign
            weighted_norm_denominator = abs(min_weighted_score)

        return ScoreResult(
            weighted_score=total_weighted_score,
            normalized_weighted_score=total_weighted_score / weighted_norm_denominator,
            raw_response_score=total_response_score,
            max_weighted_score=max_weighted_score,
            min_weighted_score=min_weighted_score,
            question_contributions=answered,
        )

    def get_score_response(self, score: float) -> ThresholdResponse | None:
        if self.thresholds is None:
            return None

        for bucket in self.thresholds:
            # Check if the score is within the range [lower, upper)
            lower_bound = bucket.lower
            upper_bound = bucket.upper

            if lower_bound <= score < upper_bound:
                return bucket

        return None

    def get_extreme_score(self, question_lookup: dict[str, Question], is_min=False) -> tuple[float, float]:
        """Returns the maxmimum (default) or minimum (is_min=True) scores possible as the raw value or final weighted value taking into account question importance weight for this set of questions.

        Args:
            question_lookup: question_lookup: dictionary for looking up questions and responses by question id
            is_min: Set to True to return the minimum, rather than maximum values. Defaults to False.

        Returns:
            tuple[float, float]: the raw extreme value, the weighted extreme value taking into account
                question importance
        """
        final_raw_score = 0.0
        final_weighted_score = 0.0
        for qid in self.question_ids:
            question = question_lookup[qid]
            score_options = [score for _, score in question.answer_options]
            if is_min:
                extreme_response_score = min(score_options)
            else:
                extreme_response_score = max(score_options)

            final_raw_score += extreme_response_score
            final_weighted_score += extreme_response_score * question.importance_score

        return final_raw_score, final_weighted_score
