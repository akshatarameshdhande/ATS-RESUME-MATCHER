"""Unit tests for text-cleaning helpers."""

import unittest

from utils.text_processor import clean_for_similarity, clean_text


class CleanTextTests(unittest.TestCase):
    """Verify display and similarity text normalization."""

    def test_empty_text_is_safe(self) -> None:
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_for_similarity(""), "")

    def test_normal_text_is_lowercased_without_losing_boundaries(self) -> None:
        self.assertEqual(clean_text("Hello, WORLD!"), "hello, world!")

    def test_similarity_cleaner_normalizes_hyphenated_phrases(self) -> None:
        cleaned = clean_for_similarity(
            "Data-driven problem-solving machine-learning"
        )
        self.assertEqual(cleaned, "data driven problem solving machine learning")

    def test_similarity_cleaner_never_concatenates_words(self) -> None:
        cleaned = clean_for_similarity(
            "data science engineering machine learning problem solving"
        )

        for phrase in (
            "data science engineering",
            "machine learning",
            "problem solving",
        ):
            self.assertIn(phrase, cleaned)

        for artifact in (
            "datascienceengineering",
            "machinelearning",
            "problemsolving",
        ):
            self.assertNotIn(artifact, cleaned)
