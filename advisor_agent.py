
import os
from dotenv import load_dotenv

load_dotenv() 
from openai import OpenAI


def generate_career_advice(
    question,
    candidate_skills,
    resume_text="",
    job_context="",
):
    """Generate personalized career advice using the OpenAI API."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Set it in your terminal."
        )

    client = OpenAI(api_key=api_key)

    # Limit the supplied resume text to avoid sending an
    # unnecessarily large amount of personal information.
    resume_excerpt = resume_text[:10000]

    instructions = """
    You are CareerPilot AI, a practical career and internship advisor.

    Help users with resume improvement, internship preparation,
    skill gaps, project ideas, learning roadmaps, and applications.

    Base personalized advice on the supplied resume information.
    Never invent qualifications, work experience, or achievements.
    Clearly distinguish confirmed skills from suggested skills to learn.
    Give actionable steps and explain your recommendations.
    If information is missing, say what additional information is needed.
    """

    user_input = f"""
    CANDIDATE SKILLS:
    {", ".join(candidate_skills) if candidate_skills else "Not provided"}

    RESUME EXCERPT:
    {resume_excerpt or "No resume text supplied"}

    INTERNSHIP CONTEXT:
    {job_context or "No specific internship selected"}

    USER QUESTION:
    {question}
    """

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=instructions,
        input=user_input,
    )

    return response.output_text
