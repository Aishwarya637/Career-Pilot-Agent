
import pandas as pd


def normalize_skill(skill):
    """Standardize skill names for consistent comparison."""
    skill = skill.strip().lower()

    aliases = {
        "llm": "llms",
        "large language models": "llms",
        "gen ai": "generative ai",
        "scikit learn": "scikit-learn",
        "scikitlearn": "scikit-learn",
        "powerbi": "power bi",
        "rest api": "rest apis",
    }

    return aliases.get(skill, skill)


def calculate_match(candidate_skills, required_skills):
    """
    Compare candidate skills with a job's required skills.
    Return score, matched skills, and missing skills.
    """
    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
        if skill.strip()
    }

    required = [
        skill.strip()
        for skill in required_skills.split(";")
        if skill.strip()
    ]

    if not required:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = [
        skill for skill in required
        if normalize_skill(skill) in candidate
    ]

    missing = [
        skill for skill in required
        if normalize_skill(skill) not in candidate
    ]

    score = round((len(matched) / len(required)) * 100)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }


def rank_internships(jobs, candidate_skills):
    """Add match details and rank internships from highest to lowest."""
    results = jobs.copy()

    if results.empty:
        results["match_score"] = pd.Series(dtype=int)
        results["matched_skills"] = pd.Series(dtype=str)
        results["missing_skills"] = pd.Series(dtype=str)
        return results

    matches = results["skills"].apply(
        lambda required: calculate_match(
            candidate_skills, required
        )
    )

    results["match_score"] = matches.apply(
        lambda result: result["match_score"]
    )

    results["matched_skills"] = matches.apply(
        lambda result: ", ".join(result["matched_skills"])
    )

    results["missing_skills"] = matches.apply(
        lambda result: ", ".join(result["missing_skills"])
    )

    return results.sort_values(
        by="match_score",
        ascending=False,
    ).reset_index(drop=True)
