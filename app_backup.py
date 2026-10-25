
import re
import json 
from internship_agent import load_internships, filter_internships 
from matching_agent import rank_internships 
from advisor_agent import generate_career_advice
import fitz
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 CareerPilot AI")
st.subheader("Your Intelligent Career & Internship Agent")

st.write(
    "Analyze your resume, discover your skills, "
    "and prepare for relevant career opportunities."
)

# Skills we can detect in resume text.
SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Excel": r"\bexcel\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Machine Learning": r"\bmachine learning\b",
    "Deep Learning": r"\bdeep learning\b",
    "Generative AI": r"\b(?:generative ai|gen\s*ai)\b",
    "LLMs": r"\b(?:llms?|large language models?)\b",
    "LangChain": r"\blangchain\b",
    "LangGraph": r"\blanggraph\b",
    "Natural Language Processing": r"\b(?:natural language processing|nlp)\b",
    "Data Analysis": r"\bdata analysis\b",
    "Data Visualization": r"\bdata visualization\b",
    "Statistics": r"\bstatistics\b",
    "Scikit-learn": r"\bscikit[\s-]?learn\b",
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "Streamlit": r"\bstreamlit\b",
    "Git": r"\bgit\b",
    "GitHub": r"\bgithub\b",
    "MySQL": r"\bmysql\b",
    "PowerPoint": r"\bpowerpoint\b",
    "AWS": r"\baws\b",
    "Azure": r"\bazure\b",
    "RAG": r"\brag\b",
    "REST APIs": r"\brest\s*apis?\b",
}


def extract_resume_text(pdf_bytes):
    """Extract selectable text from an uploaded PDF."""
    text_pages = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        for page in pdf:
            text_pages.append(page.get_text())

        page_count = len(pdf)

    return "\n".join(text_pages).strip(), page_count


def detect_skills(resume_text):
    """Find supported skills using case-insensitive patterns."""
    detected = []

    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, resume_text, re.IGNORECASE):
            detected.append(skill)

    return detected

candidate_skills = [] 
resume_text = ""
st.header("1. Upload Your Resume")

resume = st.file_uploader(
    "Choose your resume in PDF format",
    type=["pdf"],
)

if resume is not None:
    try:
        resume_text, page_count = extract_resume_text(
            resume.getvalue()
        )
        

        if not resume_text:
            st.warning(
                "No selectable text was found. "
                "Your PDF may be scanned or image-based. "
                "OCR support can be added later."
            )
        else:
            skills = detect_skills(resume_text)
            candidate_skills = skills 
            word_count = len(resume_text.split())

            st.success("Resume text extracted successfully!")

            st.header("2. Resume Overview")

            col1, col2, col3 = st.columns(3)
            col1.metric("Pages", page_count)
            col2.metric("Words", word_count)
            col3.metric("Skills Detected", len(skills))

            st.header("3. Candidate Skills")

            if skills:
                st.write(
                    "These skills were found in your resume text:"
                )

                skill_columns = st.columns(3)

                for index, skill in enumerate(skills):
                    with skill_columns[index % 3]:
                        st.markdown(f"- {skill}")
            else:
                st.info(
                    "No supported skills detected yet. "
                    "You can expand the skill dictionary later."
                )

            profile = {
                "resume_filename": resume.name,
                "pages": page_count,
                "word_count": word_count,
                "detected_skills": skills,
            }

            st.header("4. Candidate Profile")

            st.json(profile)

            st.download_button(
                label="Download Candidate Profile (JSON)",
                data=json.dumps(profile, indent=2),
                file_name="candidate_profile.json",
                mime="application/json",
            )

            with st.expander("View Extracted Resume Text"):
                st.text_area(
                    "Extracted text",
                    value=resume_text,
                    height=300,
                )

            st.caption(
                "Analysis is performed in this app session. "
                "This version does not save your resume to a database."
            )

    except Exception as error:
        st.error(
            "Could not read this PDF. "
            "Please check that the file is a valid, readable PDF."
        )
        st.caption(f"Technical details: {error}")

else:
    st.info(
        "Upload a PDF resume to begin your analysis."
    )

st.divider()
st.caption("CareerPilot AI | Resume Intelligence Module")


st.divider()
st.header("5. Internship Discovery Agent")

try:
    jobs = load_internships()

    col1, col2 = st.columns(2)

    with col1:
        roles = ["All"] + sorted(jobs["role"].unique().tolist())
        selected_role = st.selectbox("Filter by role", roles)

    with col2:
        locations = ["All"] + sorted(
            jobs["location"].unique().tolist()
        )
        selected_location = st.selectbox(
            "Filter by location", locations
        )

    selected_skill = st.text_input(
        "Filter by required skill",
        placeholder="e.g. Python, SQL, Power BI",
    )

    filtered_jobs = filter_internships(
        jobs,
        role=selected_role,
        location=selected_location,
        skill=selected_skill,
    )

    st.metric("Matching Listings", len(filtered_jobs))

    if filtered_jobs.empty:
        st.info("No listings match these filters.")
    else:
        st.dataframe(
            filtered_jobs[
                [
                    "company",
                    "role",
                    "location",
                    "work_mode",
                    "skills",
                    "source",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        for _, job in filtered_jobs.iterrows():
            st.markdown(
                f"**{job['role']} — {job['company']}**"
            )
            st.caption(
                f"{job['location']} · {job['work_mode']} · "
                f"Skills: {job['skills']}"
            )

            url = job["apply_url"]
            if url.startswith(("https://", "http://")):
                st.markdown(f"[Open listing]({url})")
            else:
                st.caption("No valid application URL provided.")

except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load internship listings: {error}")


st.divider()
st.header("6. 🎯 Job Matching Agent")

if not candidate_skills:
    st.info(
        "Upload a readable PDF resume with detectable skills "
        "to see personalized internship matches."
    )
else:
    st.write(
        "Internships ranked by how closely their listed "
        "requirements match your detected resume skills."
    )

    try:
        all_jobs = load_internships()
        ranked_jobs = rank_internships(
            all_jobs, candidate_skills
        )

        st.metric(
            "Opportunities Analyzed",
            len(ranked_jobs),
        )

        if ranked_jobs.empty:
            st.warning("No internship listings are available.")

        for _, job in ranked_jobs.iterrows():
            with st.container(border=True):
                st.subheader(
                    f"{job['role']} — {job['company']}"
                )

                st.progress(
                    int(job["match_score"]) / 100,
                    text=f"Skill match: {job['match_score']}%",
                )

                st.caption(
                    f"{job['location']} · {job['work_mode']}"
                )

                st.write(
                    "**Matched skills:** "
                    + (job["matched_skills"] or "None detected")
                )

                st.write(
                    "**Skills to develop:** "
                    + (job["missing_skills"] or "None from this list")
                )

                url = job["apply_url"]
                if url.startswith(("https://", "http://")):
                    st.markdown(f"[View listing]({url})")

    except (FileNotFoundError, ValueError) as error:
        st.error(f"Unable to calculate matches: {error}")


st.divider()
st.header("7. 🤖 AI Career Advisor")

st.write(
    "Ask questions about your resume, skill gaps, "
    "internship preparation, or career roadmap."
)

career_question = st.text_area(
    "What would you like help with?",
    placeholder=(
        "Example: Based on my resume, what skills should "
        "I improve to get a Data Analyst internship?"
    ),
    key="career_question",
)

if st.button("Generate AI Advice", type="primary"):
    if not career_question.strip():
        st.warning("Please enter a question first.")

    else:
        # Reuse the extracted resume text if available.
        resume_context = resume_text 

        with st.spinner("CareerPilot AI is preparing your advice..."):
            try:
                answer = generate_career_advice(
                    question=career_question,
                    candidate_skills=candidate_skills,
                    resume_text=resume_context,
                )

                st.subheader("Your Personalized Career Advice")
                st.markdown(answer)

            except Exception as error:
                st.error(
                    "The AI request failed. Check your API key, "
                    "model access, and API usage limits."
                )
                st.caption(f"Technical details: {error}")
