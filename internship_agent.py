
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "internships.csv"

REQUIRED_COLUMNS = [
    "company",
    "role",
    "location",
    "work_mode",
    "skills",
    "source",
    "apply_url",
]


def load_internships():
    """Load listings and remove duplicate opportunities."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Internship dataset not found: {DATA_PATH}"
        )

    jobs = pd.read_csv(DATA_PATH)

    missing = set(REQUIRED_COLUMNS) - set(jobs.columns)
    if missing:
        raise ValueError(
            f"Missing CSV columns: {', '.join(sorted(missing))}"
        )

    for column in REQUIRED_COLUMNS:
        jobs[column] = jobs[column].fillna("").astype(str).str.strip()

    # Prefer the URL to identify duplicate listings.
    jobs["_url_key"] = jobs["apply_url"].str.lower().str.rstrip("/")

    has_url = jobs["_url_key"] != ""

    with_url = jobs[has_url].drop_duplicates(
        subset=["_url_key"],
        keep="first",
    )

    without_url = jobs[~has_url].drop_duplicates(
        subset=["company", "role", "location"],
        keep="first",
    )

    jobs = pd.concat([with_url, without_url]).sort_index()

    return jobs.drop(columns=["_url_key"]).reset_index(drop=True)


def filter_internships(
    jobs,
    role="All",
    location="All",
    skill="",
):
    """Filter opportunities by role, location, and skill."""
    result = jobs.copy()

    if role != "All":
        result = result[
            result["role"].str.contains(
                role, case=False, na=False, regex=False
            )
        ]

    if location != "All":
        result = result[
            result["location"].str.contains(
                location, case=False, na=False, regex=False
            )
        ]

    if skill.strip():
        result = result[
            result["skills"].str.contains(
                skill.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ]

    return result.reset_index(drop=True)
