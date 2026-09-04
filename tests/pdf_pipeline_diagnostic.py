r"""Print PDF extraction diagnostics before and after text processing.

Run from the project root, for example:
    .\.venv\Scripts\python.exe tests\pdf_pipeline_diagnostic.py "path\to\resume.pdf" "job description text"
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.matcher import calculate_similarity
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.text_processor import clean_text


EXPECTED_PHRASES = (
    "data science",
    "machine learning",
    "data analysis",
    "power bi",
    "problem solving",
    "technical skills",
)


def phrase_results(text: str) -> dict[str, bool]:
    """Return whether each expected phrase is present in a text stage."""
    normalized_text = text.lower()
    return {phrase: phrase in normalized_text for phrase in EXPECTED_PHRASES}


def print_phrase_results(stage_name: str, text: str) -> None:
    """Print the expected-phrase status for one pipeline stage."""
    print(f"\n{stage_name}")
    for phrase, found in phrase_results(text).items():
        status = "FOUND" if found else "MISSING"
        print(f"- {phrase}: {status}")


def print_first_boundary_loss(stages: tuple[tuple[str, str], ...]) -> None:
    """Report the first stage that no longer contains an expected phrase."""
    for stage_name, text in stages:
        missing_phrases = [
            phrase for phrase, found in phrase_results(text).items() if not found
        ]
        if missing_phrases:
            print(
                f"\nFirst stage with missing word boundaries: {stage_name} "
                f"({', '.join(missing_phrases)})"
            )
            return

    print("\nFirst stage with missing word boundaries: none")


def run_diagnostic(resume_path: Path, job_description: str) -> None:
    """Trace the resume from PDF extraction through matching."""
    with resume_path.open("rb") as resume_file:
        extracted_text = extract_text_from_pdf(resume_file)

    cleaned_resume_text = clean_text(extracted_text)
    cleaned_job_description = clean_text(job_description)

    print_phrase_results("Extracted text before cleaning", extracted_text)
    print(f"\nExtracted sample:\n{extracted_text[:600]}")
    print_phrase_results("Cleaned resume text", cleaned_resume_text)
    print(f"\nCleaned sample:\n{cleaned_resume_text[:600]}")
    print_first_boundary_loss(
        (
            ("PDF extraction", extracted_text),
            ("text cleaning", cleaned_resume_text),
        )
    )
    print(f"\nDetected resume skills: {', '.join(extract_skills(cleaned_resume_text))}")
    print(f"Detected JD skills: {', '.join(extract_skills(cleaned_job_description))}")

    similarity = calculate_similarity(cleaned_resume_text, cleaned_job_description)
    print(f"Raw TF-IDF cosine similarity: {similarity:.4f}")
    print(f"Similarity percentage: {similarity:.2%}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python tests/pdf_pipeline_diagnostic.py "
            "<resume.pdf> <job description>"
        )

    run_diagnostic(Path(sys.argv[1]), sys.argv[2])
