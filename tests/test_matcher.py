"""Unit tests for TF-IDF similarity and overall ATS scoring."""

import unittest

from utils.matcher import calculate_overall_ats_score, calculate_similarity


class SimilarityTests(unittest.TestCase):
    """Verify standard cosine-similarity behavior."""

    def test_identical_text_is_one(self) -> None:
        similarity = calculate_similarity("Python data science", "Python data science")
        self.assertAlmostEqual(similarity, 1.0)

    def test_unrelated_text_is_zero(self) -> None:
        similarity = calculate_similarity(
            "Python data science", "gardening cooking vegetables"
        )
        self.assertAlmostEqual(similarity, 0.0)

    def test_related_text_is_within_score_range(self) -> None:
        similarity = calculate_similarity(
            "Python machine learning data science",
            "Python data analysis machine learning",
        )
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)
        self.assertLessEqual(similarity, 1.0)

    def test_empty_input_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_similarity("", "Python")
        with self.assertRaises(ValueError):
            calculate_similarity("Python", "")

    def test_technical_tokens_are_usable(self) -> None:
        similarity = calculate_similarity(
            "C++ C# React.js Node.js",
            "C++ C# React.js Node.js",
        )
        self.assertAlmostEqual(similarity, 1.0)


class OverallScoreTests(unittest.TestCase):
    """Verify the locked 40/60 ATS scoring formula."""

    def test_weighted_score(self) -> None:
        self.assertAlmostEqual(calculate_overall_ats_score(0.50, 0.75), 0.65)

    def test_boundary_scores(self) -> None:
        self.assertEqual(calculate_overall_ats_score(0.0, 0.0), 0.0)
        self.assertEqual(calculate_overall_ats_score(1.0, 1.0), 1.0)
