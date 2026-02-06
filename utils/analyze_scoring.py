#!/usr/bin/env python3
"""
Analyze scoring configurations to determine min and max possible scores.

This script reads all questions from questions.json and specified scoring configuration
files, then calculates and displays the minimum and maximum possible scores for
each scoring configuration based on the weighted average scoring method.

Usage:
    python -m utils.analyze_scoring data/*_scoring_questions.json
    python -m utils.analyze_scoring --questions --scoring_configs /questions.json data/organizational_scoring_questions.json

Arguments:
    scoring_configs: One or more scoring configuration JSON files to analyze

Options:
    --questions PATH: Path to questions.json (default: data/questions.json)
"""

import argparse
from pathlib import Path

from utils.models import QuestionBank, QuestionScoringCollection


def main():
    """Main function to analyze scoring configurations."""
    parser = argparse.ArgumentParser(description="Analyze scoring configurations and display min/max possible scores")
    parser.add_argument(
        "--questions",
        type=Path,
        help="Path to questions.json (default: data/questions.json)",
    )
    parser.add_argument(
        "--scoring_configs",
        type=Path,
        nargs="+",
        help="One or more scoring configuration JSON files to analyze",
    )

    args = parser.parse_args()

    questions_path = args.questions
    scoring_configs = args.scoring_configs

    # Load all questions using Pydantic
    print(f"Loading questions from: {questions_path}")
    question_bank = QuestionBank.model_validate_json(questions_path.read_text())
    question_lookup = {q.question_id: q for q in question_bank.questions}
    print(f"Loaded {len(question_lookup)} questions\n")

    print(f"Analyzing {len(scoring_configs)} scoring configuration(s)\n")
    print("=" * 80)

    # Analyze each scoring config
    for config_path in scoring_configs:
        print(f"\nScoring Config: {config_path.name}")
        print("-" * 80)

        question_collection = QuestionScoringCollection.model_validate_json(config_path.read_text())

        # Display header if available
        if question_collection.header:
            print("Header:", question_collection.header)

        print(f"Number of questions: {len(question_collection.question_ids)}")

        # Calculate min and max scores
        min_raw_score, min_weighted_score = question_collection.get_extreme_score(question_lookup, is_min=True)

        max_raw_score, max_weighted_score = question_collection.get_extreme_score(question_lookup)

        print("\nMinimum Scores:")
        print("  Minimum weighted score:", min_weighted_score)
        print("  Minimum raw score (without importance weighting):", min_raw_score)
        print("  Normalized minimum weighted score:", min_weighted_score / abs(min_weighted_score))

        print("\nMaximum Scores:")
        print("  Maximum weighted score:", max_weighted_score)
        print("  Maximum raw score (without importance weighting):", max_raw_score)
        print("  Normalized maximum weighed score:", max_weighted_score / abs(max_weighted_score))

        # Display thresholds if available
        if question_collection.thresholds:
            increasing_order_thresholds = sorted(question_collection.thresholds, key=lambda x: x.lower)
            print(f"\nThresholds ({len(question_collection.thresholds)}):")
            for i, threshold in enumerate(increasing_order_thresholds, 1):
                print(f"  Threshold {i}, Header:", threshold.header)
                print("\tLower bound (inclusive):", threshold.lower)
                print("\tUpper bound (exclusive):", threshold.upper)
                print("\tColor:", threshold.color)

        print("=" * 80)


if __name__ == "__main__":
    main()
