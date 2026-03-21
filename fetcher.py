# fetcher.py
# This file's only job: go to the internet and return raw job data

import requests
from sources import (
    fetch_all_greenhouse, fetch_all_workday,
    fetch_all_lever, fetch_all_ashby, fetch_remoteok,
)
from company_sources import GREENHOUSE_BOARDS, WORKDAY_SOURCES, LEVER_BOARDS, ASHBY_BOARDS



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


def fetch_all_sources():
    """
    Fetch jobs from all configured sources and return one combined list.
    """
    all_jobs = []

    all_jobs.extend(fetch_simplify_jobs())
    all_jobs.extend(fetch_all_greenhouse(GREENHOUSE_BOARDS))
    all_jobs.extend(fetch_all_lever(LEVER_BOARDS))
    all_jobs.extend(fetch_all_ashby(ASHBY_BOARDS))
    all_jobs.extend(fetch_remoteok())
    all_jobs.extend(fetch_all_workday(WORKDAY_SOURCES))

    print(f"Fetched {len(all_jobs)} total jobs from all sources")
    return all_jobs