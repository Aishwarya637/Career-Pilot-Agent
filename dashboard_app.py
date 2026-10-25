
import streamlit as st

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dashboard styling
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
    }

    .hero {
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #172554, #3730a3);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero p {
        color: #e0e7ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    st.title("🚀 CareerPilot AI")
    st.caption("Your intelligent career companion")
    st.divider()

    selected_page = st.radio(
        "NAVIGATION",
        [
            "Resume Scanner",
            "Job Finder",
            "Resume Optimizer",
        ],
    )

    st.divider()
    st.caption("Build your career with AI")

# Main dashboard header
st.markdown(
    """
    <div class="hero">
        <h1>Welcome to CareerPilot AI</h1>
        <p>
            Analyze your resume, discover opportunities,
            and optimize your job applications.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Page content
if selected_page == "Resume Scanner":
    import re
    import fitz
    import json

    st.header("📄 Resume Scanner")
    st.write(
        "Upload your resume to extract its text, "
        "detect skills, and create a candidate profile."
    )

    skill_patterns = {
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
        "Data Analysis": r"\bdata analysis\b",
        "Data Visualization": r"\bdata visualization\b",
        "Scikit-learn": r"\bscikit[\s-]?learn\b",
        "TensorFlow": r"\btensorflow\b",
        "PyTorch": r"\bpytorch\b",
        "Streamlit": r"\bstreamlit\b",
        "GitHub": r"\bgithub\b",
        "MySQL": r"\bmysql\b",
        "AWS": r"\baws\b",
        "Azure": r"\bazure\b",
        "REST APIs": r"\brest\s*apis?\b",
    }

    resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        key="scanner_resume",
    )

    if resume is not None:
        try:
            with fitz.open(
                stream=resume.getvalue(),
                filetype="pdf",
            ) as pdf:
                resume_text = "\n".join(
                    page.get_text() for page in pdf
                ).strip()
                page_count = len(pdf)

            if not resume_text:
                st.warning(
                    "No selectable text was found. "
                    "This PDF may be scanned or image-based."
                )
            else:
                detected_skills = [
                    skill
                    for skill, pattern in skill_patterns.items()
                    if re.search(
                        pattern, resume_text, re.IGNORECASE
                    )
                ]
                st.session_state["resume_text"] = resume_text
                st.session_state["detected_skills"] = detected_skills

                word_count = len(resume_text.split())

                word_count = len(resume_text.split())

                st.success("Resume scanned successfully!")

                col1, col2, col3 = st.columns(3)
                col1.metric("Pages", page_count)
                col2.metric("Words", word_count)
                col3.metric("Skills detected", len(detected_skills))

                st.subheader("Detected Skills")

                if detected_skills:
                    st.write(" · ".join(detected_skills))
                else:
                    st.info(
                        "No skills from the current detection "
                        "dictionary were found."
                    )

                profile = {
                    "resume_filename": resume.name,
                    "pages": page_count,
                    "word_count": word_count,
                    "detected_skills": detected_skills,
                }

                st.subheader("Candidate Profile")
                st.json(profile)

                st.download_button(
                    "Download Candidate Profile (JSON)",
                    data=json.dumps(profile, indent=2),
                    file_name="candidate_profile.json",
                    mime="application/json",
                )

                with st.expander("View extracted resume text"):
                    st.text_area(
                        "Resume text",
                        value=resume_text,
                        height=300,
                    )

        except Exception as error:
            st.error("Unable to read this PDF.")
            st.caption(f"Technical details: {error}")


elif selected_page == "Job Finder":
    from urllib.parse import urlencode

    st.header("💼 Job Finder Agent")
    st.write(
        "Discover job opportunities based on your "
        "preferred role, location, and work preferences."
    )

    with st.form("job_finder_form"):
        job_role = st.selectbox(
            "Preferred job role",
            [
                "Data Analyst",
                "Business Analyst",
                "Python Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "Generative AI Engineer",
                "AI Engineer",
                "Software Developer",
            ],
        )

        location = st.text_input(
            "Preferred location",
            value="Pune",
            placeholder="e.g. Pune, Mumbai, Remote",
        )

        job_type = st.selectbox(
            "Job type",
            [
                "Internship",
                "Full-time",
                "Part-time",
                "Entry-level",
            ],
        )

        work_mode = st.selectbox(
            "Work preference",
            [
                "Any",
                "Remote",
                "Hybrid",
                "On-site",
            ],
        )

        skills_input = st.text_input(
            "Skills (optional)",
            placeholder="e.g. Python, SQL, Excel, Power BI",
        )

        search_clicked = st.form_submit_button(
            "Find Jobs",
            type="primary",
            use_container_width=True,
        )

    if search_clicked:
        keywords = [job_role, job_type]

        if skills_input.strip():
            keywords.append(skills_input.strip())

        if work_mode != "Any":
            keywords.append(work_mode)

        query = " ".join(keywords)
        search_location = location.strip()

        st.subheader("Your Job Search")
        st.caption(
            "These links open platform searches. "
            "Individual openings and availability must be "
            "verified on the job platform."
        )

        linkedin_params = {
            "keywords": query,
            "location": search_location,
        }

        indeed_params = {
            "q": query,
            "l": search_location,
        }

        naukri_params = {
            "k": query,
            "l": search_location,
        }

        job_platforms = [
            (
                "LinkedIn Jobs",
                "https://www.linkedin.com/jobs/search/?"
                + urlencode(linkedin_params),
            ),
            (
                "Indeed",
                "https://www.indeed.com/jobs?"
                + urlencode(indeed_params),
            ),
            (
                "Naukri",
                "https://www.naukri.com/jobs?"
                + urlencode(naukri_params),
            ),
        ]

        for platform, url in job_platforms:
            with st.container(border=True):
                st.subheader(platform)
                st.link_button(
                    f"Search on {platform}",
                    url,
                    use_container_width=True,
                )

        st.success(
            f"Created job searches for {job_role} "
            f"in {search_location or 'all locations'}."
        )



elif selected_page == "Resume Optimizer":
    import re
    from collections import Counter

    st.header("📝 Resume Optimizer Agent")
    st.write(
        "Compare your resume with a job description "
        "to identify matching keywords and potential gaps."
    )

    resume_text = st.session_state.get("resume_text", "")

    if not resume_text:
        st.warning(
            "Please upload your resume on the Resume Scanner page first."
        )

    job_description = st.text_area(
        "Paste the job description",
        height=250,
        placeholder="Paste the job description here..."
    )

    if st.button("Analyze Resume Match", type="primary"):
        if not resume_text:
            st.error("Please upload your resume on Resume Scanner first.")

        elif not job_description.strip():
            st.error("Please paste a job description.")

        else:
            def get_keywords(text):
                words = re.findall(
                    r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
                    text.lower()
                )

                stop_words = {
                    "the", "and", "for", "with", "you", "your",
                    "are", "our", "this", "that", "will", "from",
                    "have", "has", "was", "were", "who", "what",
                    "when", "where", "how", "all", "any", "can",
                    "job", "role", "work", "team", "using", "required"
                }

                return set(
                    word for word in words
                    if word not in stop_words and len(word) > 2
                )

            resume_keywords = get_keywords(resume_text)
            job_keywords = get_keywords(job_description)

            matched = sorted(resume_keywords & job_keywords)
            missing = sorted(job_keywords - resume_keywords)

            score = round(
                len(matched) / len(job_keywords) * 100
            ) if job_keywords else 0

            col1, col2, col3 = st.columns(3)

            col1.metric("Keyword overlap", f"{score}%")
            col2.metric("Matching keywords", len(matched))
            col3.metric("Potential gaps", len(missing))

            st.progress(score / 100)

            st.caption(
                "This is a basic keyword-overlap estimate, "
                "not a validated ATS score."
            )

            st.subheader("✅ Matching Keywords")
            st.write(", ".join(matched) if matched else "No matches found.")

            st.subheader("⚠️ Potentially Missing Keywords")
            st.write(", ".join(missing[:40]) if missing else "No gaps detected.")

            st.subheader("💡 Suggestions")
            st.markdown(
                "- Highlight relevant projects and skills you genuinely have.\n"
                "- Use action verbs to describe your contributions.\n"
                "- Include measurable results where accurate.\n"
                "- Do not add skills or experience you do not have."
            )

            report = (
                f"CareerPilot AI - Resume Optimization Report\n\n"
                f"Keyword overlap estimate: {score}%\n\n"
                f"Matching keywords:\n{', '.join(matched)}\n\n"
                f"Potentially missing keywords:\n{', '.join(missing)}"
            )

            st.download_button(
                "Download Optimization Report",
                data=report,
                file_name="resume_optimization_report.txt",
                mime="text/plain"
            )

st.divider()
st.caption("CareerPilot AI | Your career, your next move.")
