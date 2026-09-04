"""Dictionary-based skill extraction for ATS Resume Matcher."""

import csv
import re
from pathlib import Path


SKILLS_FILE = Path(__file__).resolve().parent.parent / "data" / "skills.csv"

# These are intentional technical-name equivalents. There is deliberately no
# GitHub-to-Git mapping: the two skills remain distinct.
SKILL_ALIASES = {
    "C++": ("C Plus Plus",),
    "C#": ("C Sharp",),
    "React": ("React.js", "ReactJS"),
    "Node.js": ("Node", "NodeJS"),
    "PostgreSQL": ("Postgres",),
    "Power BI": ("PowerBI",),
    "Scikit-learn": ("sklearn",),
    "AWS": ("Amazon Web Services",),
    "Google Cloud": ("GCP",),
    "Kubernetes": ("K8s",),
    "Data Structures and Algorithms": ("DSA", "Data Structures & Algorithms"),
    "Object-Oriented Programming": ("OOP", "OOPs"),
    "REST API": ("REST APIs", "RESTful API", "RESTful APIs"),
    "NLP": ("Natural Language Processing",),
    "CI/CD": ("Continuous Integration", "Continuous Delivery"),
    "JWT Authentication": ("JWT",),
    "MERN Stack": ("MERN",),
    "Role-Based Access Control": ("Role Based Access Control", "RBAC"),
    "SOC Operations": ("Security Operations",),
    "Artificial Intelligence": ("AI",),
    "Large Language Models": ("LLM", "Large Language Model", "LLMs"),
}

# Skill phrases may be written with spaces, hyphens, or common punctuation
# between words. Treat only those separators as interchangeable; this is not
# fuzzy matching and does not make unrelated skill names equivalent.
PHRASE_SEPARATOR_PATTERN = r"[\s\-_/.,:;&]+"


def load_skills() -> list[str]:
    """Load unique skills from the project's CSV file."""
    if not SKILLS_FILE.exists():
        raise ValueError("The skills data file could not be found.")

    try:
        with SKILLS_FILE.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or "skill" not in reader.fieldnames:
                raise ValueError("The skills data file must contain a 'skill' column.")

            skills = []
            seen_skills = set()

            for row in reader:
                skill = row["skill"].strip()
                skill_key = skill.lower()

                if skill and skill_key not in seen_skills:
                    skills.append(skill)
                    seen_skills.add(skill_key)

    except OSError as error:
        raise ValueError("The skills data file could not be read.") from error

    if not skills:
        raise ValueError("The skills data file is empty.")

    return skills


def skill_in_text(skill: str, text: str) -> bool:
    """Check for a complete skill name instead of a partial word match."""
    escaped_skill = re.escape(skill.lower())

    # Allow formatting variants such as "role-based", "role based", and
    # "role_based" for multi-word skill names without merging their words.
    escaped_skill = re.sub(
        r"\\[ -]",
        lambda _match: PHRASE_SEPARATOR_PATTERN,
        escaped_skill,
    )

    if skill.lower() == "c":
        pattern = r"(?<!\w)c(?![\w+#])"
    elif skill.lower() == "css":
        # Tailwind CSS is its own skill and must not imply standalone CSS.
        pattern = r"(?<!tailwind )(?<!tailwind-)(?<!tailwind_)(?<!tailwind\.)(?<!\w)css(?!\w)"
    elif skill.lower() == "git":
        # Do not infer Git from GitHub, including the hyphenated spelling.
        pattern = r"(?<!\w)git(?![\w-]*hub\b)(?!\w)"
    elif skill.lower() == "react":
        # React Native is a distinct skill and must not be counted as React.
        pattern = rf"(?<!\w)react(?!{PHRASE_SEPARATOR_PATTERN}native\b)(?!\w)"
    else:
        pattern = rf"(?<!\w){escaped_skill}(?!\w)"

    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def extract_skills(cleaned_text: str) -> list[str]:
    """Return unique skills from the CSV that appear in cleaned text."""
    if not cleaned_text.strip():
        return []

    detected_skills = []
    for skill in load_skills():
        names_to_check = (skill, *SKILL_ALIASES.get(skill, ()))
        if any(skill_in_text(name, cleaned_text) for name in names_to_check):
            detected_skills.append(skill)

    return detected_skills


def calculate_skill_match(
    resume_skills: list[str], job_skills: list[str]
) -> tuple[list[str], list[str], float]:
    """Return matched skills, missing JD skills, and the match ratio from 0 to 1."""
    resume_skill_keys = {skill.lower() for skill in resume_skills}
    matched_skills = [skill for skill in job_skills if skill.lower() in resume_skill_keys]
    missing_skills = [
        skill for skill in job_skills if skill.lower() not in resume_skill_keys
    ]
    skill_match_ratio = len(matched_skills) / len(job_skills) if job_skills else 0.0

    return matched_skills, missing_skills, skill_match_ratio
