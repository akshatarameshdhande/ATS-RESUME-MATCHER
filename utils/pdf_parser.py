"""Functions for extracting text from resume PDF files."""

import re
from typing import BinaryIO

import pdfplumber


# The default horizontal tolerance can merge separately positioned words in
# some PDF layouts. A smaller tolerance keeps normal gaps as word boundaries.
WORD_BOUNDARY_TOLERANCE = 1


def extract_text_from_pdf(uploaded_file: BinaryIO) -> str:
    """Extract and clean text from every page of an uploaded PDF file.

    Raises:
        ValueError: If the PDF cannot be read or contains no readable text.
    """
    try:
        uploaded_file.seek(0)

        with pdfplumber.open(uploaded_file) as pdf:
            page_text = []

            for page in pdf.pages:
                text = page.extract_text(x_tolerance=WORD_BOUNDARY_TOLERANCE)
                if text:
                    page_text.append(text)

    except Exception as error:
        raise ValueError("Unable to read this PDF file.") from error

    extracted_text = "\n".join(page_text)
    cleaned_text = re.sub(r"\n\s*\n+", "\n\n", extracted_text).strip()

    if not cleaned_text:
        raise ValueError(
            "Unable to extract readable text from this PDF. "
            "Please upload a text-based PDF resume."
        )

    return cleaned_text
