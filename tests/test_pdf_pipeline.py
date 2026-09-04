"""Integration checks for the representative PDF extraction pipeline."""

import unittest
from pathlib import Path

from utils.pdf_parser import extract_text_from_pdf


REPRESENTATIVE_RESUME = (
    Path(__file__).resolve().parents[1]
    / "sample_data"
    / "ALEX_MORGAN_SAMPLE_RESUME.pdf"
)


class RepresentativePdfPipelineTests(unittest.TestCase):
    """Verify that the representative resume remains readable and spaced."""

    def test_representative_pdf_extracts_expected_text(self) -> None:
        with REPRESENTATIVE_RESUME.open("rb") as resume_file:
            extracted_text = extract_text_from_pdf(resume_file)

        self.assertTrue(extracted_text.strip())
        self.assertIn("ALEX MORGAN", extracted_text)
        self.assertIn("Data Structures", extracted_text)
        self.assertIn("Splunk", extracted_text)

    def test_representative_pdf_has_no_known_concatenation_artifacts(self) -> None:
        with REPRESENTATIVE_RESUME.open("rb") as resume_file:
            extracted_text = extract_text_from_pdf(resume_file).lower()

        for artifact in (
            "datascienceengineering",
            "machinelearning",
            "problemsolving",
        ):
            self.assertNotIn(artifact, extracted_text)
