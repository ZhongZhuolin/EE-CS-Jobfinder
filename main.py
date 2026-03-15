from fetcher import fetch_all_sources
from filter import filter_jobs, sort_jobs_by_recent_state_score, add_date_timestamps
from utils import dedupe_jobs
from database import (
    create_tables,
    upsert_jobs,
    delete_jobs_older_than_30_days,
    get_all_jobs,
    mark_jobs_as_alerted
)

from exporter import export_jobs_to_excel
from alerts import send_discord_alerts


def main():
    print("Starting job tracker...\n")

    create_tables()

    jobs = fetch_all_sources()
    print(f"Raw jobs fetched: {len(jobs)}")

    jobs = dedupe_jobs(jobs)
    print(f"After dedupe: {len(jobs)}")
    
    jobs = filter_jobs(
    jobs,
    internships_only=True,
    active_only=True,
    min_score=4
    )

    jobs = add_date_timestamps(jobs)
    jobs = sort_jobs_by_recent_state_score(jobs)


    

    new_jobs = upsert_jobs(jobs)
    print(f"New jobs added this run: {len(new_jobs)}")

    deleted_count = delete_jobs_older_than_30_days()
    print(f"Old jobs deleted (>30 days): {deleted_count}")

    all_jobs = get_all_jobs()
    export_jobs_to_excel(all_jobs)
    print("Updated job_tracker.xlsx")

    send_discord_alerts(new_jobs, min_score=6)
    mark_jobs_as_alerted(new_jobs)

    print("\nDone.")


if __name__ == "__main__":
    main()