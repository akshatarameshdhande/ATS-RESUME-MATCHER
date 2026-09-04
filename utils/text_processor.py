"""Simple text-cleaning functions for TalentMatch AI."""

import re


def clean_text(text: str) -> str:
    """Return lowercase text with normalized spacing and useful characters kept."""
    cleaned_text = text.lower()

    # Keep email, URL, date, and common resume punctuation intact for display
    # and dictionary-based skill extraction.
    cleaned_text = re.sub(r"[^a-z0-9\s@+#./:;,&()|!?'=~_\-]", " ", cleaned_text)
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    lines = [line.strip() for line in cleaned_text.splitlines()]
    cleaned_text = "\n".join(lines)
    cleaned_text = re.sub(r"\n\s*\n+", "\n\n", cleaned_text)

    return cleaned_text.strip()


def clean_for_similarity(text: str) -> str:
    """Normalize text for TF-IDF while preserving technical terms and boundaries."""
    cleaned_text = text.lower().replace("-", " ")
    # Keep +, #, and dots so C++, C#, Node.js, and React.js remain meaningful
    # TF-IDF terms. Other punctuation becomes a separator, never a deletion.
    cleaned_text = re.sub(r"[^a-z0-9\s+#.]", " ", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    return cleaned_text.strip()
