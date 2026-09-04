# TalentMatch AI — ATS Resume Parser & Matching Engine

TalentMatch AI is a Streamlit application for comparing a candidate resume with a job description. It accepts a PDF resume, extracts its text with `pdfplumber`, identifies supported skills, measures lexical text similarity with TF-IDF and cosine similarity, and presents an explainable ATS-style match score.

The application is designed to make its scoring components visible rather than presenting an opaque recommendation.

## Key Features

- PDF resume upload and text extraction
- Resume and job-description text cleaning
- CSV-backed skill extraction
- Canonical skills, aliases, and boundary-aware matching
- Matched and missing job-description skills
- TF-IDF and cosine-similarity text comparison
- Separate Text Similarity and Skill Match scores
- Overall ATS Match with a transparent 40/60 contribution breakdown
- Validation for missing input and unreadable PDFs
- Streamlit interface with extracted and cleaned text previews

## How Matching Works

```text
Resume PDF
  → PDF extraction
  → text cleaning
  → skill extraction
  → TF-IDF text similarity
  → skill matching
  → overall ATS score
  → Streamlit results
```

Text similarity and skill matching are separate components. Text similarity compares the resume and job-description wording, while skill matching checks which supported job-description skills are explicitly found in the resume.

## Scoring Formula

```text
Overall ATS =
0.40 × Text Similarity +
0.60 × Skill Match
```

- **Text Similarity** uses TF-IDF vectorization and cosine similarity.
- **Skill Match** is the proportion of supported job-description skills detected in the resume.
- The components remain separate and are combined only by the displayed formula.
- The score is an explainable, rules-based indicator—not an AI-generated hiring judgment.

## Skill Matching

The supported vocabulary is stored in [data/skills.csv](data/skills.csv). The extractor uses canonical skill names, explicit aliases, case-insensitive matching, multi-word normalization, and word boundaries.

Examples of intentional distinctions:

- Git ≠ GitHub
- Java ≠ JavaScript
- React ≠ React Native
- SIEM ≠ Splunk
- Networking ≠ Network Security

Matching is evidence- and vocabulary-based. The application does not claim to recognize every possible technology, framework, or professional skill; unsupported skills may not be detected.

## Project Structure

```text
ATS_Resume_Matcher/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── text_processor.py
│   ├── skill_extractor.py
│   └── matcher.py
├── data/
│   └── skills.csv
├── sample_data/
└── tests/
    ├── pdf_pipeline_diagnostic.py
    ├── test_text_processor.py
    ├── test_skill_extractor.py
    ├── test_matcher.py
    └── test_pdf_pipeline.py
```

## Technologies Used

- Python
- Streamlit
- pdfplumber
- scikit-learn

## Installation

From PowerShell in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell prevents local script activation, use this process-only fallback and then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Running the Application

```powershell
streamlit run app.py
```

Streamlit normally opens the local application in a browser.

## Usage

1. Upload a text-based PDF resume.
2. Paste the job description.
3. Click **Analyze Resume & Job Match**.
4. Review Text Similarity and Skill Match.
5. Review the Overall ATS Match and contribution breakdown.
6. Inspect matched and missing job-description skills.
7. Optionally open the extracted and cleaned text previews for transparency or troubleshooting.

## Verification / Testing

The repository includes a fictional public sample resume, `ALEX_MORGAN_SAMPLE_RESUME.pdf`, for PDF-extraction and pipeline testing. The application accepts user-provided resumes and job descriptions generally.

An Infosys Digital Specialist Engineer / Specialist Programmer job description was used only as a representative verification example during development. It is not a project requirement and is not hardcoded in the application.

Run the automated test suite with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

For PDF extraction and phrase-boundary diagnostics, run:

```powershell
.\.venv\Scripts\python.exe tests\pdf_pipeline_diagnostic.py "path\to\resume.pdf" "job description text"
```

## Limitations

- PDF extraction quality depends on the PDF's underlying text structure.
- Scanned or image-only PDFs may not contain extractable text.
- Skill matching depends on explicit evidence in the supported vocabulary.
- Unsupported skills may not be detected.
- TF-IDF is lexical rather than semantic, so it does not fully capture equivalent wording.
- The result is an ATS-style matching indicator, not a hiring decision.

## Future Improvements

Potential future work includes:

- Expanding the supported skill vocabulary
- Strengthening automated test coverage
- Improving PDF handling for more document layouts
- Adding multilingual text support
- Evaluating semantic similarity as a separate future enhancement

## License

This project is licensed under the [MIT License](LICENSE).
