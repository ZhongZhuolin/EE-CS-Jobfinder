import os
import sqlite3
import time
from flask import Flask, render_template, request, jsonify

# Change to the directory containing this script so relative paths (jobs.db) work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = "jobs.db"

app = Flask(__name__)


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def days_ago(ts):
    """Return how many days ago a unix timestamp was, as an integer."""
    if not ts:
        return None
    diff = time.time() - int(ts)
    return max(0, int(diff // 86400))


def rows_to_dicts(rows):
    """Convert sqlite3.Row objects to plain dicts, adding days_ago field."""
    jobs = []
    for row in rows:
        d = dict(row)
        d["days_ago"] = days_ago(d.get("date_updated_ts"))
        jobs.append(d)
    return jobs


def query_jobs(q=None, source=None, state=None, applied=None, min_score=None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT id, title, company_name, url, date_updated, date_updated_ts,
               source, locations, match_score, active, alerted,
               applied, priority, status, notes
        FROM jobs
        ORDER BY date_updated_ts DESC, match_score DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    jobs = rows_to_dicts(rows)

    # Apply filters in Python (all filters also run client-side for instant UX,
    # but server-side filtering keeps the initial page load accurate and supports
    # the /api/jobs endpoint).
    if q:
        q_lower = q.lower()
        jobs = [j for j in jobs if q_lower in (j.get("title") or "").lower()
                or q_lower in (j.get("company_name") or "").lower()]

    if source and source != "all":
        jobs = [j for j in jobs if (j.get("source") or "").lower() == source.lower()]

    if state and state != "all":
        state_lower = state.lower()
        if state_lower == "remote":
            jobs = [j for j in jobs if "remote" in (j.get("locations") or "").lower()]
        elif state_lower == "other":
            known = {"nj", "pa", "ny", "remote"}
            def is_other(j):
                loc = (j.get("locations") or "").lower()
                return not any(k in loc for k in known)
            jobs = [j for j in jobs if is_other(j)]
        else:
            jobs = [j for j in jobs if state_lower in (j.get("locations") or "").lower()]

    if applied == "yes":
        jobs = [j for j in jobs if j.get("applied")]
    elif applied == "no":
        jobs = [j for j in jobs if not j.get("applied")]

    if min_score is not None:
        try:
            min_score_int = int(min_score)
            jobs = [j for j in jobs if (j.get("match_score") or 0) >= min_score_int]
        except (ValueError, TypeError):
            pass

    return jobs


def compute_stats(jobs):
    total = len(jobs)
    applied_count = sum(1 for j in jobs if j.get("applied"))
    week_ts = time.time() - 7 * 86400
    new_this_week = sum(1 for j in jobs if (j.get("date_updated_ts") or 0) >= week_ts)
    scores = [j.get("match_score") or 0 for j in jobs if j.get("match_score") is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    return {
        "total": total,
        "applied": applied_count,
        "new_this_week": new_this_week,
        "avg_score": avg_score,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    source = request.args.get("source", "all").strip()
    state = request.args.get("state", "all").strip()
    applied = request.args.get("applied", "all").strip()
    min_score = request.args.get("min_score", "").strip()

    jobs = query_jobs(
        q=q or None,
        source=source if source != "all" else None,
        state=state if state != "all" else None,
        applied=applied if applied != "all" else None,
        min_score=min_score if min_score else None,
    )

    # Always compute stats over ALL jobs (unfiltered) for the stats bar
    all_jobs = query_jobs()
    stats = compute_stats(all_jobs)

    filters = {
        "q": q,
        "source": source,
        "state": state,
        "applied": applied,
        "min_score": min_score,
    }

    return render_template("index.html", jobs=jobs, stats=stats, filters=filters)


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json(force=True)
    url = data.get("url")
    field = data.get("field")
    value = data.get("value")

    allowed_fields = {"applied", "priority", "status", "notes"}
    if not url or field not in allowed_fields:
        return jsonify({"ok": False, "error": "Invalid field or missing url"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    if field == "applied":
        value = 1 if str(value).lower() in ("1", "true", "yes") else 0
    elif field == "priority":
        try:
            value = int(value)
        except (ValueError, TypeError):
            value = 0

    cursor.execute(f"UPDATE jobs SET {field} = ? WHERE url = ?", (value, url))
    conn.commit()
    conn.close()

    return jsonify({"ok": True})


@app.route("/api/jobs")
def api_jobs():
    q = request.args.get("q", "").strip()
    source = request.args.get("source", "").strip()
    state = request.args.get("state", "").strip()
    applied = request.args.get("applied", "").strip()
    min_score = request.args.get("min_score", "").strip()

    jobs = query_jobs(
        q=q or None,
        source=source or None,
        state=state or None,
        applied=applied or None,
        min_score=min_score or None,
    )
    return jsonify(jobs)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
