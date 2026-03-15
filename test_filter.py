from fetcher import fetch_all_sources
from filter import filter_jobs, sort_jobs_by_score_then_date
from utils import dedupe_jobs

jobs = fetch_all_sources()
print(f"Raw jobs fetched: {len(jobs)}")

jobs = dedupe_jobs(jobs)
print(f"After dedupe: {len(jobs)}")

filtered_jobs = filter_jobs(
    jobs,
    internships_only=True,
    active_only=True,
    min_score=4
)

filtered_jobs = sort_jobs_by_score_then_date(filtered_jobs)

print(f"After filter: {len(filtered_jobs)}\n")

for job in filtered_jobs[:20]:
    print("---")
    print(f"Title:   {job.get('title')}")
    print(f"Company: {job.get('company_name')}")
    print(f"Score:   {job.get('match_score')}")
    print(f"Date:    {job.get('date_updated')}")
    print(f"Source:  {job.get('source')}")
    print(f"URL:     {job.get('url')}")