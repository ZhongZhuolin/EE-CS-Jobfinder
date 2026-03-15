# utils.py

def normalize_text(text):
    """
    Lowercase and strip text so comparisons are cleaner.
    """
    return str(text).strip().lower()


def dedupe_jobs(jobs):
    """
    Remove duplicate jobs based on title + company + URL.

    Returns a new list with duplicates removed.
    """
    seen = set()
    unique_jobs = []

    for job in jobs:
        key = (
            normalize_text(job.get("title", "")),
            normalize_text(job.get("company_name", "")),
            normalize_text(job.get("url", ""))
        )

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs