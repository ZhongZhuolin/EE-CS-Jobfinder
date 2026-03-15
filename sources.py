# sources.py
# Functions that fetch jobs from Greenhouse and Workday job boards

import requests


def fetch_greenhouse_board(board_token, company_name):
    """
    Fetch jobs from a Greenhouse job board.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch Greenhouse board {board_token}: {e}")
        return []

    jobs = []

    for job in data.get("jobs", []):
        job_data = {
            "title": job.get("title", "Unknown Title"),
            "company_name": company_name,
            "url": job.get("absolute_url", ""),
            "date_updated": job.get("updated_at", ""),
            "locations": [job.get("location", {}).get("name", "Unknown")],
            "active": True,
            "source": "Greenhouse"
        }

        jobs.append(job_data)

    print(f"Fetched {len(jobs)} jobs from Greenhouse ({company_name})")

    return jobs


def fetch_all_greenhouse(boards):
    """
    Fetch jobs from all configured Greenhouse boards.
    """
    all_jobs = []

    for board in boards:
        jobs = fetch_greenhouse_board(
            board_token=board["board_token"],
            company_name=board["company_name"]
        )

        all_jobs.extend(jobs)

    return all_jobs


def fetch_workday_jobs(source):
    """
    Fetch jobs from a Workday job endpoint.
    """
    try:
        response = requests.get(source["url"], timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch Workday jobs for {source['company_name']}: {e}")
        return []

    jobs = []

    postings = data.get("jobPostings", [])

    for job in postings:
        job_data = {
            "title": job.get("title", "Unknown Title"),
            "company_name": source["company_name"],
            "url": job.get("externalPath", ""),
            "date_updated": job.get("postedOn", ""),
            "locations": [job.get("locationsText", "Unknown")],
            "active": True,
            "source": "Workday"
        }

        jobs.append(job_data)

    print(f"Fetched {len(jobs)} jobs from Workday ({source['company_name']})")

    return jobs


def fetch_all_workday(sources):
    """
    Fetch jobs from all configured Workday sources.
    """
    all_jobs = []

    for source in sources:
        jobs = fetch_workday_jobs(source)
        all_jobs.extend(jobs)

    return all_jobs