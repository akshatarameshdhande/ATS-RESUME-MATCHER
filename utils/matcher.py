"""TF-IDF and cosine-similarity functions for ATS Resume Matcher."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_processor import clean_for_similarity


# Keep common technical terms intact instead of letting the default tokenizer
# discard punctuation from C++, C#, Node.js, and React.js.
TECHNICAL_TOKEN_PATTERN = r"(?u)[a-z]\+\+|[a-z]#|[a-z0-9]+(?:\.[a-z0-9]+)*"
TEXT_SIMILARITY_WEIGHT = 0.40
SKILL_MATCH_WEIGHT = 0.60


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """Return cosine similarity using boundary-preserving TF-IDF text."""
    cleaned_resume_text = clean_for_similarity(resume_text)
    cleaned_job_description = clean_for_similarity(job_description)

    if not cleaned_resume_text or not cleaned_job_description:
        raise ValueError("Both resume and job description text are required.")

    try:
        # TF-IDF converts important words in both documents into numeric vectors.
        vectorizer = TfidfVectorizer(token_pattern=TECHNICAL_TOKEN_PATTERN)
        text_vectors = vectorizer.fit_transform(
            [cleaned_resume_text, cleaned_job_description]
        )
    except ValueError as error:
        raise ValueError("The text does not contain enough useful terms to compare.") from error

    # Cosine similarity measures how closely the two text vectors point together.
    similarity = cosine_similarity(text_vectors[0:1], text_vectors[1:2])[0][0]

    return float(similarity)


def calculate_overall_ats_score(
    text_similarity: float, skill_match_ratio: float
) -> float:
    """Combine text and skill scores with transparent, fixed weights."""
    return (
        text_similarity * TEXT_SIMILARITY_WEIGHT
        + skill_match_ratio * SKILL_MATCH_WEIGHT
    )
