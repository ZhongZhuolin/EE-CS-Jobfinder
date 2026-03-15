from datetime import datetime

TARGET_KEYWORDS = {
    # General CS / Software
    "software": 3, "software engineer": 4, "software engineering": 4,
    "backend": 3, "frontend": 2, "full stack": 2, "full-stack": 2,
    "developer": 2, "programmer": 2, "computer science": 2,
    "machine learning": 3, "ai": 2, "data engineer": 3, "data science": 2,
    "python": 3, "c++": 4, "java": 2,

    # Medical / Healthtech
    "medical software": 5, "healthtech": 4, "health tech": 4,
    "clinical software": 4, "biomedical software": 5, "digital health": 4,
    "medical device software": 5, "rehabilitation software": 5,
    "medical device": 5, "biomedical": 4, "rehabilitation": 4,
    "assistive technology": 4,

    # Embedded / Firmware
    "embedded": 5, "embedded systems": 5, "embedded software": 5,
    "firmware": 5, "rtos": 4, "microcontroller": 4, "fpga": 4,
    "dsp": 4, "hardware software": 3, "systems engineer": 2,

    # Defense / Aerospace
    "defense": 5, "dod": 5, "department of defense": 5, "aerospace": 4,
    "missile": 4, "radar": 4, "satellite": 4, "avionics": 4,
    "government": 2, "national security": 4, "military": 3,
    "space systems": 4, "cleared": 3, "secret clearance": 5,

    # EE / Hardware
    "electrical engineer": 5, "electrical engineering": 5, "electronics": 3,
    "pcb": 3, "circuit": 3, "signal processing": 4, "controls": 3,
    "controls engineer": 4, "power systems": 3, "communications": 3, "rf": 3,

    # Robotics / Autonomy
    "robotics": 4, "autonomy": 4, "autonomous systems": 4,
    "sensor fusion": 4, "computer vision": 3,
}

EXCLUDE_KEYWORDS = [
    "accounting", "sales", "marketing", "human resources", "hr ",
    "recruiter", "finance intern", "business analyst", "supply chain",
    "mechanical only", "civil engineer", "chemist",
]


def job_text(job):
    title       = str(job.get("title", ""))
    company     = str(job.get("company_name", ""))
    locations   = job.get("locations", [])
    source      = str(job.get("source", ""))
    description = str(job.get("description", ""))
    loc_text    = " ".join(locations) if isinstance(locations, list) else str(locations)
    return f"{title} {company} {loc_text} {source} {description}".lower()


def is_likely_internship(job):
    title = str(job.get("title", "")).lower()
    return any(w in title for w in ["intern", "internship", "co-op", "coop", "student"])


def get_job_score(job):
    text = job_text(job)
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return -1
    return sum(pts for kw, pts in TARGET_KEYWORDS.items() if kw in text)


def is_relevant_job(job, min_score=3):
    return get_job_score(job) >= min_score


# ── Date parsing ──────────────────────────────────────────────────────────────

def parse_date(date_value):
    if not date_value:
        return datetime.min
    if isinstance(date_value, (int, float)):
        try:
            return datetime.fromtimestamp(date_value)
        except Exception:
            return datetime.min
    text = str(date_value).strip()
    if text.isdigit():
        try:
            return datetime.fromtimestamp(int(text))
        except Exception:
            return datetime.min
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%m/%d/%Y",
    ]:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return datetime.min


def add_date_timestamps(jobs):
    for job in jobs:
        parsed = parse_date(job.get("date_updated", ""))
        job["date_updated_ts"] = 0 if parsed == datetime.min else int(parsed.timestamp())
    return jobs


# ── Location ──────────────────────────────────────────────────────────────────

STATE_MAP = {
    "new jersey": "NJ", " nj": "NJ",
    "pennsylvania": "PA", " pa": "PA",
    "new york": "NY", " ny": "NY",
    "california": "CA", " ca": "CA",
    "texas": "TX", " tx": "TX",
    "virginia": "VA", " va": "VA",
    "maryland": "MD", " md": "MD",
    "massachusetts": "MA", " ma": "MA",
    "washington": "WA", " wa": "WA",
    "colorado": "CO", " co": "CO",
    "georgia": "GA", " ga": "GA",
    "florida": "FL", " fl": "FL",
    "ohio": "OH", " oh": "OH",
    "michigan": "MI", " mi": "MI",
    "illinois": "IL", " il": "IL",
    "north carolina": "NC", " nc": "NC",
    "arizona": "AZ", " az": "AZ",
    "connecticut": "CT", " ct": "CT",
}


def get_state_label(job):
    """
    Return the actual state abbreviation, 'Remote', or '' (blank) — never 'Other'.
    """
    locations = job.get("locations", [])
    if isinstance(locations, str):
        locations = [locations]
    text = " " + " ".join(locations).lower() + " "

    if "remote" in text:
        return "Remote"

    for phrase, abbr in STATE_MAP.items():
        if phrase in text:
            return abbr

    return ""   # unknown — leave blank rather than 'Other'


def location_priority(job):
    """NJ=4, PA=3, NY=2, Remote=1, everything else=0."""
    state = get_state_label(job)
    return {"NJ": 4, "PA": 3, "NY": 2, "Remote": 1}.get(state, 0)


# ── Filter & sort ─────────────────────────────────────────────────────────────

def filter_jobs(jobs, internships_only=True, active_only=True, min_score=4):
    filtered = []
    for job in jobs:
        if active_only and not job.get("active", True):
            continue
        if internships_only and not is_likely_internship(job):
            continue
        score = get_job_score(job)
        if score >= min_score:
            job["match_score"] = score
            filtered.append(job)
    return filtered


def sort_jobs_by_recent_state_score(jobs):
    """Newest first, then NJ/PA/NY/Remote priority, then match score."""
    return sorted(
        jobs,
        key=lambda j: (
            j.get("date_updated_ts", 0),
            location_priority(j),
            j.get("match_score", 0),
        ),
        reverse=True,
    )


# keep old name as alias so nothing breaks
sort_jobs_by_score_then_date = sort_jobs_by_recent_state_score