from fetcher import fetch_all_sources
from filter import filter_jobs, sort_jobs_by_score_then_date

jobs = fetch_all_sources()
filtered_jobs = filter_jobs(jobs, internships_only=True, active_only=True, min_score=4)
filtered_jobs = sort_jobs_by_score_then_date(filtered_jobs)

for job in filtered_jobs[:20]:
    print("---")
    print(f"Title:   {job.get('title')}")
    print(f"Company: {job.get('company_name')}")
    print(f"Score:   {job.get('match_score')}")
    print(f"Date:    {job.get('date_updated')}")
    print(f"Source:  {job.get('source')}")
    print(f"URL:     {job.get('url')}")