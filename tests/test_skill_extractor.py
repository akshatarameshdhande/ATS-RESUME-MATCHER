"""Unit tests for vocabulary-based skill extraction."""

import unittest

from utils.skill_extractor import extract_skills


class SkillExtractorTests(unittest.TestCase):
    """Verify canonical skills, aliases, and false-positive protections."""

    def test_supported_aliases_resolve_to_canonical_skills(self) -> None:
        cases = {
            "OOP": "Object-Oriented Programming",
            "OOPs": "Object-Oriented Programming",
            "DSA": "Data Structures and Algorithms",
            "Data Structures & Algorithms": "Data Structures and Algorithms",
            "REST APIs": "REST API",
            "Security Operations": "SOC Operations",
            "AI": "Artificial Intelligence",
            "LLM": "Large Language Models",
            "JWT": "JWT Authentication",
            "JWT Authentication": "JWT Authentication",
            "MERN": "MERN Stack",
            "MERN Stack": "MERN Stack",
            "React": "React",
            "React.js": "React",
            "Node": "Node.js",
            "Node.js": "Node.js",
            "Role-Based Access Control": "Role-Based Access Control",
            "Role Based Access Control": "Role-Based Access Control",
            "RBAC": "Role-Based Access Control",
        }

        for text, expected_skill in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected_skill, extract_skills(text))

    def test_ai_llm_provides_evidence_for_both_canonical_skills(self) -> None:
        detected_skills = extract_skills("AI/LLM")

        self.assertIn("Artificial Intelligence", detected_skills)
        self.assertIn("Large Language Models", detected_skills)

    def test_expanded_canonical_skills_are_detected(self) -> None:
        text = (
            "Kotlin PHP React Native Vue.js Next.js Spring Boot GraphQL SQLite Redis "
            "Matplotlib Seaborn Apache Kafka Keras OpenCV Hugging Face AWS EC2 AWS S3 "
            "AWS Lambda Jenkins Terraform GitHub Actions Pytest JUnit Selenium OWASP "
            "Penetration Testing SSH npm Maven"
        )
        expected_skills = {
            "Kotlin",
            "PHP",
            "React Native",
            "Vue.js",
            "Next.js",
            "Spring Boot",
            "GraphQL",
            "SQLite",
            "Redis",
            "Matplotlib",
            "Seaborn",
            "Apache Kafka",
            "Keras",
            "OpenCV",
            "Hugging Face",
            "AWS EC2",
            "AWS S3",
            "AWS Lambda",
            "Jenkins",
            "Terraform",
            "GitHub Actions",
            "Pytest",
            "JUnit",
            "Selenium",
            "OWASP",
            "Penetration Testing",
            "SSH",
            "npm",
            "Maven",
        }

        self.assertTrue(expected_skills.issubset(extract_skills(text)))

    def test_expanded_aliases_resolve_to_canonical_skills(self) -> None:
        cases = {
            "Postgres": "PostgreSQL",
            "sklearn": "Scikit-learn",
            "PowerBI": "Power BI",
            "GCP": "Google Cloud",
            "Amazon Web Services": "AWS",
            "K8s": "Kubernetes",
            "RESTful API": "REST API",
            "RESTful APIs": "REST API",
            "Natural Language Processing": "NLP",
            "Large Language Model": "Large Language Models",
            "LLMs": "Large Language Models",
            "C Sharp": "C#",
            "C Plus Plus": "C++",
            "Continuous Integration": "CI/CD",
            "Continuous Delivery": "CI/CD",
        }

        for text, expected_skill in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected_skill, extract_skills(text))

    def test_false_positive_protections(self) -> None:
        cases = {
            "GitHub": "Git",
            "JavaScript": "Java",
            "React Native": "React",
            "React-Native": "React",
            "Tailwind CSS": "CSS",
        }

        for text, unexpected_skill in cases.items():
            with self.subTest(text=text):
                self.assertNotIn(unexpected_skill, extract_skills(text))

    def test_react_native_remains_distinct_from_react(self) -> None:
        detected_skills = extract_skills("React Native")

        self.assertIn("React Native", detected_skills)
        self.assertNotIn("React", detected_skills)

    def test_distinct_skills_remain_distinct(self) -> None:
        cases = {
            "Git": "Git",
            "GitHub": "GitHub",
            "Java": "Java",
            "JavaScript": "JavaScript",
            "SIEM": "SIEM",
            "Splunk": "Splunk",
            "Networking": "Networking",
            "Network Security": "Network Security",
        }

        for text, expected_skill in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected_skill, extract_skills(text))
