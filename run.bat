import sqlite3
from datetime import datetime, timedelta

DB_NAME = "jobs.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company_name TEXT,
            url TEXT UNIQUE,
            date_updated TEXT,
            date_updated_ts INTEGER,
            source TEXT,
            locations TEXT,
            match_score INTEGER,
            active INTEGER,
            alerted INTEGER DEFAULT 0,
            applied INTEGER DEFAULT 0,
            priority INTEGER DEFAULT 0,
            status TEXT DEFAULT '',
            notes TEXT DEFAULT ''
        )
    """)

    # Migrate old schema: drop first_seen/last_seen if they exist,
    # add new columns if missing.
    cursor.execute("PRAGMA table_info(jobs)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    if "first_seen" in existing_cols or "last_seen" in existing_cols:
        print("Migrating database schema (removing first_seen/last_seen)...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company_name TEXT,
                url TEXT UNIQUE,
                date_updated TEXT,
                date_updated_ts INTEGER,
                source TEXT,
                locations TEXT,
                match_score INTEGER,
                active INTEGER,
                alerted INTEGER DEFAULT 0,
                applied INTEGER DEFAULT 0,
                priority INTEGER DEFAULT 0,
                status TEXT DEFAULT '',
                notes TEXT DEFAULT ''
            )
        """)
        # Only copy columns that actually exist in the old table
        new_cols = {"id", "title", "company_name", "url", "date_updated",
                    "date_updated_ts", "source", "locations", "match_score",
                    "active", "alerted", "applied", "priority", "status", "notes"}
        cols_to_copy = [c for c in new_cols if c in existing_cols]
        col_list = ", ".join(cols_to_copy)
        cursor.execute(f"INSERT INTO jobs_new ({col_list}) SELECT {col_list} FROM jobs")
        cursor.execute("DROP TABLE jobs")
        cursor.execute("ALTER TABLE jobs_new RENAME TO jobs")
        print("Migration complete.")
        # Re-read columns now that the table has been rebuilt
        cursor.execute("PRAGMA table_info(jobs)")
        existing_cols = {row[1] for row in cursor.fetchall()}

    # Add any missing columns to existing schema
    for col, definition in [
        ("alerted",  "INTEGER DEFAULT 0"),
        ("applied",  "INTEGER DEFAULT 0"),
        ("priority", "INTEGER DEFAULT 0"),
        ("status",   "TEXT DEFAULT ''"),
        ("notes",    "TEXT DEFAULT ''"),
    ]:
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col} {definition}")

    conn.commit()
    conn.close()


def upsert_jobs(jobs):
    """
    Insert new jobs or update existing ones.
    Returns a list of newly inserted jobs only.
    Never overwrites applied/priority/status/notes set by the user.
    """
    conn = get_connection()
    cursor = conn.cursor()

    new_jobs = []

    for job in jobs:
        title = job.get("title", "")
        company_name = job.get("company_name", "")
        url = job.get("url", "")
        date_updated = str(job.get("date_updated", ""))
        date_updated_ts = int(job.get("date_updated_ts", 0))
        source = job.get("source", "")
        locations = (
            ", ".join(job.get("locations", []))
            if isinstance(job.get("locations", []), list)
            else str(job.get("locations", ""))
        )
        match_score = int(job.get("match_score", 0))
        active = 1 if job.get("active", True) else 0

        cursor.execute("SELECT id FROM jobs WHERE url = ?", (url,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE jobs
                SET title = ?, company_name = ?, date_updated = ?, date_updated_ts = ?,
                    source = ?, locations = ?, match_score = ?, active = ?
                WHERE url = ?
            """, (title, company_name, date_updated, date_updated_ts,
                  source, locations, match_score, active, url))
        else:
            cursor.execute("""
                INSERT INTO jobs (
                    title, company_name, url, date_updated, date_updated_ts,
                    source, locations, match_score, active, alerted,
                    applied, priority, status, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, '', '')
            """, (title, company_name, url, date_updated, date_updated_ts,
                  source, locations, match_score, active))
            new_jobs.append(job)

    conn.commit()
    conn.close()

    return new_jobs


def delete_jobs_older_than_30_days():
    conn = get_connection()
    cursor = conn.cursor()

    cutoff_ts = int((datetime.now() - timedelta(days=30)).timestamp())

    cursor.execute("""
        DELETE FROM jobs
        WHERE date_updated_ts > 0 AND date_updated_ts < ?
    """, (cutoff_ts,))

    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_count


def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, company_name, url, date_updated, date_updated_ts,
               source, locations, match_score, active, alerted,
               applied, priority, status, notes
        FROM jobs
        ORDER BY date_updated_ts DESC, match_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    jobs = []
    for row in rows:
        jobs.append({
            "title": row[0],
            "company_name": row[1],
            "url": row[2],
            "date_updated": row[3],
            "date_updated_ts": row[4],
            "source": row[5],
            "locations": row[6].split(", ") if row[6] else [],
            "match_score": row[7],
            "active": bool(row[8]),
            "alerted": bool(row[9]),
            "applied": bool(row[10]),
            "priority": row[11],
            "status": row[12] or "",
            "notes": row[13] or "",
        })

    return jobs


def mark_jobs_as_alerted(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute("UPDATE jobs SET alerted = 1 WHERE url = ?", (job.get("url", ""),))

    conn.commit()
    conn.close()


def update_job_user_data(url, applied=None, priority=None, status=None, notes=None):
    """
    Update user-tracked fields for a job by URL.
    Only updates fields that are not None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if applied is not None:
        fields.append("applied = ?")
        values.append(1 if applied else 0)
    if priority is not None:
        fields.append("priority = ?")
        values.append(int(priority))
    if status is not None:
        fields.append("status = ?")
        values.append(str(status))
    if notes is not None:
        fields.append("notes = ?")
        values.append(str(notes))

    if fields:
        values.append(url)
        cursor.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE url = ?", values)
        conn.commit()

    conn.close()