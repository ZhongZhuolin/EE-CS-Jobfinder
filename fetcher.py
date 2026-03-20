# fetcher.py
# This file's only job: go to the internet and return raw job data

import requests
import feedparser
from sources import fetch_all_greenhouse, fetch_all_workday

from company_sources import GREENHOUSE_BOARDS, WORKDAY_SOURCES



# The URL of the SimplifyJobs JSON file on GitHub
SIMPLIFY_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json"


def fetch_simplify_jobs():
    """
    Downloads the SimplifyJobs listings.json file and returns it
    as a Python list of dictionaries.

    Returns: list of job dicts, or empty list if something fails
    """
    print("Fetching jobs from SimplifyJobs GitHub...")

    try:
        response = requests.get(SIMPLIFY_URL, timeout=20)
        response.raise_for_status()
        jobs = response.json()

        print(f"Successfully fetched {len(jobs)} total job listings")
        return jobs

    except requests.RequestException as e:
        print(f"Failed to fetch SimplifyJobs data: {e}")
        return []


def fetch_indeed_rss(query="electrical engineering internship"):
    """
    Fetches job listings from Indeed's RSS feed for a given search query.

    Returns: list of job dicts in same format as simplify jobs
    """
    url = f"https://www.indeed.com/rss?q={query.replace(' ', '+')}&sort=date"

    print(f"Fetching Indeed RSS feed for: {query}")

    feed = feedparser.parse(url)

    jobs = []

    for entry in feed.entries:
        job = {
            "title": entry.get("title", "Unknown Title"),
            "company_name": entry.get("author", "Unknown Company"),
            "url": entry.get("link", ""),
            "date_updated": entry.get("published", ""),
            "locations": [entry.get("location", "Unknown")],
            "active": True,
            "source": "Indeed"
        }
        jobs.append(job)

    print(f"Fetched {len(jobs)} jobs from Indeed for '{query}'")
    return jobs


def fetch_all_sources():
    """
    Fetch jobs from all configured sources and return one combined list.
    """
    all_jobs = []

    # Existing source: Simplify
    all_jobs.extend(fetch_simplify_jobs())

    # Existing source: Indeed RSS
    indeed_queries = [
        # CS / Software
        "software engineer internship",
        "backend engineer internship",
        "computer science internship",
        "systems software internship",
        "devops engineer internship",
        "cloud engineer internship",
        "cybersecurity internship",
        # AI / ML / Data
        "machine learning internship",
        "data science internship",
        "data engineering internship",
        "ai engineer internship",
        "mlops internship",
        "nlp engineer internship",
        # Banking / FinTech
        "fintech software internship",
        "banking technology internship",
        "financial software engineer internship",
        "payments engineering internship",
        "capital one software internship",
        "fraud detection engineer internship",
        # MedTech
        "medical device software internship",
        "medical software internship",
        "healthtech software internship",
        "biomedical software internship",
        "digital health engineering internship",
        # Embedded / EE / Defense
        "embedded systems internship",
        "firmware internship",
        "electrical engineering internship",
        "defense software internship",
        "avionics internship",
        "fpga internship",
        # Government / Defense contractors
        "government software internship",
        "dod software internship",
        "cleared software engineer internship",
        "defense contractor internship",
        "signals intelligence internship",
        "systems engineer defense internship",
        "radar software internship",
        "national security software internship",
        "booz allen internship",
        "leidos internship",
        "saic internship",
        # Non-tech companies
        "software engineer internship insurance",
        "software engineer internship automotive",
        "software developer internship retail",
        "data engineer internship energy",
        "software engineer internship telecom",
    ]

    for query in indeed_queries:
        all_jobs.extend(fetch_indeed_rss(query))

    # New sources: Greenhouse + Workday
    all_jobs.extend(fetch_all_greenhouse(GREENHOUSE_BOARDS))
    all_jobs.extend(fetch_all_workday(WORKDAY_SOURCES))

    print(f"Fetched {len(all_jobs)} total jobs from all sources")
    return all_jobs