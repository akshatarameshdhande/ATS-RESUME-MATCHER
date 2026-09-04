"""ATS Resume Matcher Streamlit homepage."""

import streamlit as st

from utils.matcher import (
    SKILL_MATCH_WEIGHT,
    TEXT_SIMILARITY_WEIGHT,
    calculate_overall_ats_score,
    calculate_similarity,
)
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import calculate_skill_match, extract_skills
from utils.text_processor import clean_text


st.set_page_config(page_title="ATS Resume Matcher", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
        .ats-score-card {
            background: linear-gradient(135deg, #0f3d56 0%, #176b87 100%);
            border-radius: 12px;
            color: white;
            padding: 1.5rem;
            text-align: center;
        }
        .ats-score-card p { margin: 0; }
        .ats-score-card .score-label {
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .ats-score-card .score-value {
            font-size: 3rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0.4rem 0;
        }
        .ats-score-card .score-detail {
            color: #d9edf7;
            font-size: 0.85rem;
        }
        .skill-list {
            line-height: 1.7;
            margin: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ATS Resume Matcher")
st.subheader("Smart Resume & Job Matching")
st.write(
    "Compare a candidate's resume with a job description using TF-IDF, cosine "
    "similarity, and skill matching."
)
st.info(
    "Upload your resume, enter a job description, and click "
    "Analyze Resume & Job Match to view the comparison."
)

with st.form("resume_match_form"):
    st.divider()
    st.subheader("Upload Your Resume")
    st.write("Upload your resume in PDF format to begin the analysis.")
    uploaded_resume = st.file_uploader("Choose a resume PDF", type=["pdf"])

    st.divider()
    st.subheader("Job Description")
    st.write("Paste the job description for the position you are applying for.")
    job_description = st.text_area(
        "Enter the job description",
        height=250,
        placeholder="Paste the job description here...",
    )
    analyze_submitted = st.form_submit_button(
        "🔍 Analyze Resume & Job Match",
        type="primary",
        use_container_width=True,
    )

if analyze_submitted:
    if uploaded_resume is None:
        st.warning("Please upload a resume PDF before analyzing the match.")
    elif not job_description.strip():
        st.warning("Please enter a job description before analyzing the match.")
    else:
        try:
            resume_text = extract_text_from_pdf(uploaded_resume)
        except ValueError as error:
            st.error(str(error))
        else:
            cleaned_resume_text = clean_text(resume_text)
            cleaned_job_description = clean_text(job_description)

            if not cleaned_resume_text or not cleaned_job_description:
                st.warning("Please provide readable resume and job description text.")
            else:
                st.session_state.analysis_result = {
                    "resume_text": resume_text,
                    "cleaned_resume_text": cleaned_resume_text,
                    "cleaned_job_description": cleaned_job_description,
                }

if "analysis_result" in st.session_state:
    analysis_result = st.session_state.analysis_result
    resume_text = analysis_result["resume_text"]
    cleaned_resume_text = analysis_result["cleaned_resume_text"]
    cleaned_job_description = analysis_result["cleaned_job_description"]

    st.success("Resume text extracted and cleaned successfully.")

    skill_match_ratio = 0.0
    resume_skills = []
    job_skills = []
    matched_skills = []
    missing_skills = []
    skill_extraction_available = False

    try:
        resume_skills = extract_skills(cleaned_resume_text)
        job_skills = extract_skills(cleaned_job_description)
    except ValueError as error:
        st.error(f"Skill extraction is unavailable: {error}")
    else:
        matched_skills, missing_skills, skill_match_ratio = calculate_skill_match(
            resume_skills,
            job_skills,
        )
        skill_extraction_available = True

    try:
        similarity = calculate_similarity(cleaned_resume_text, cleaned_job_description)
    except ValueError as error:
        st.warning(f"Unable to calculate text similarity: {error}")
    else:
        overall_score = calculate_overall_ats_score(similarity, skill_match_ratio)

        st.divider()
        st.subheader("Match Results")
        st.caption("Scores are calculated from independent text and skill comparisons.")

        score_column, overall_column = st.columns([1.15, 1])
        with score_column:
            text_metric_column, skill_metric_column = st.columns(2)
            with text_metric_column:
                st.metric("Text Similarity", f"{similarity:.0%}")
                st.caption(f"Raw cosine similarity: {similarity:.2f}")
            with skill_metric_column:
                st.metric("Skill Match", f"{skill_match_ratio:.0%}")
                st.caption("Matched job-description skills")

        with overall_column:
            st.markdown(
                f"""
                <div class="ats-score-card">
                    <p class="score-label">OVERALL ATS MATCH</p>
                    <p class="score-value">{overall_score:.0%}</p>
                    <p class="score-detail">40% text similarity + 60% skill match</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        contribution_column, formula_column = st.columns(2)
        with contribution_column:
            st.caption("Score contributions")
            st.write(
                f"Text Similarity (40%): **{similarity * TEXT_SIMILARITY_WEIGHT:.1%}**"
            )
            st.write(
                f"Skill Match (60%): **{skill_match_ratio * SKILL_MATCH_WEIGHT:.1%}**"
            )
        with formula_column:
            st.caption("Calculation")
            st.write(
                f"**{overall_score:.1%}** = "
                f"({similarity:.1%} × 40%) + ({skill_match_ratio:.1%} × 60%)"
            )

        if similarity >= 0.70:
            explanation = "The resume and job description have strong textual similarity."
        elif similarity >= 0.40:
            explanation = "The resume and job description have moderate textual similarity."
        else:
            explanation = "The resume and job description have low textual similarity."
        st.write(explanation)

    if skill_extraction_available:
        st.divider()
        st.subheader("Skill Details")
        resume_column, job_column = st.columns(2)
        with resume_column:
            st.markdown("**Detected Resume Skills**")
            if resume_skills:
                st.markdown(
                    f'<p class="skill-list">{", ".join(resume_skills)}</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.warning("No listed skills were detected in the resume.")

        with job_column:
            st.markdown("**Detected Job Description Skills**")
            if job_skills:
                st.markdown(
                    f'<p class="skill-list">{", ".join(job_skills)}</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.warning("No listed skills were detected in the job description.")

        matched_column, missing_column = st.columns(2)
        with matched_column:
            st.markdown("**Matched Skills**")
            if matched_skills:
                st.success(", ".join(matched_skills))
            else:
                st.info("No job-description skills matched the resume.")

        with missing_column:
            st.markdown("**Missing JD Skills**")
            if missing_skills:
                st.warning(", ".join(missing_skills))
            else:
                st.success("All detected job-description skills appear in the resume.")

    st.divider()
    with st.expander("View analysis input text", expanded=False):
        st.caption("These previews are retained for transparency and troubleshooting.")
        preview_limit = 3000

        st.markdown("**Extracted Resume Text**")
        st.text(resume_text[:preview_limit])
        if len(resume_text) > preview_limit:
            st.caption("Preview limited to the first 3,000 characters.")

        st.markdown("**Cleaned Resume Text**")
        st.text(cleaned_resume_text[:preview_limit])
        if len(cleaned_resume_text) > preview_limit:
            st.caption("Preview limited to the first 3,000 characters.")

        st.markdown("**Cleaned Job Description**")
        st.text(cleaned_job_description[:preview_limit])
        if len(cleaned_job_description) > preview_limit:
            st.caption("Preview limited to the first 3,000 characters.")
