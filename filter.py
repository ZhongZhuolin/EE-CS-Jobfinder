from datetime import datetime

TARGET_KEYWORDS = {
    # ── General CS / Software ──────────────────────────────────────────────────
    "software": 3, "software engineer": 4, "software engineering": 4,
    "backend": 3, "frontend": 2, "full stack": 2, "full-stack": 2,
    "developer": 2, "programmer": 2, "computer science": 2,
    "swe": 4, "sde": 4, "site reliability": 3, "sre": 3,
    "platform engineer": 3, "infrastructure": 2, "devops": 3,
    "cloud": 2, "distributed systems": 3, "systems programming": 3,
    "api": 2, "microservices": 2, "kubernetes": 2, "docker": 2,
    "python": 3, "c++": 4, "java": 2, "golang": 2, "rust": 3,
    "typescript": 2, "javascript": 2,

    # ── AI / ML / Data ─────────────────────────────────────────────────────────
    "machine learning": 4, "deep learning": 4, "neural network": 3,
    "artificial intelligence": 3, "ai/ml": 4, "ml engineer": 4,
    "nlp": 3, "natural language processing": 3, "llm": 4,
    "generative ai": 4, "reinforcement learning": 3,
    "computer vision": 3, "data engineer": 4, "data science": 3,
    "data analyst": 2, "data platform": 3, "analytics engineer": 3,
    "ai": 2, "ml": 2, "mlops": 4, "feature engineering": 3,

    # ── Banking / FinTech ──────────────────────────────────────────────────────
    "fintech": 4, "financial technology": 4, "financial software": 4,
    "banking technology": 4, "payments": 3, "payment systems": 4,
    "fraud detection": 4, "risk engineering": 3, "quantitative": 3,
    "capital markets": 3, "trading systems": 4, "algorithmic trading": 4,
    "regulatory technology": 3, "regtech": 3, "anti-money laundering": 3,

    # ── Medical / Healthtech ───────────────────────────────────────────────────
    "medical software": 5, "healthtech": 4, "health tech": 4,
    "clinical software": 4, "biomedical software": 5, "digital health": 4,
    "medical device software": 5, "rehabilitation software": 5,
    "medical device": 5, "biomedical": 4, "rehabilitation": 4,
    "assistive technology": 4, "health informatics": 4, "bioinformatics": 4,
    "electronic health records": 4, "ehr": 3, "telemedicine": 3,

    # ── Embedded / Firmware ────────────────────────────────────────────────────
    "embedded": 5, "embedded systems": 5, "embedded software": 5,
    "firmware": 5, "rtos": 4, "microcontroller": 4, "fpga": 4,
    "dsp": 4, "hardware software": 3, "systems engineer": 2,

    # ── Defense / Aerospace ────────────────────────────────────────────────────
    "defense": 5, "dod": 5, "department of defense": 5, "aerospace": 4,
    "missile": 4, "radar": 4, "satellite": 4, "avionics": 4,
    "government": 2, "national security": 4, "military": 3,
    "space systems": 4, "cleared": 3, "secret clearance": 5,

    # ── EE / Hardware ──────────────────────────────────────────────────────────
    "electrical engineer": 5, "electrical engineering": 5, "electronics": 3,
    "pcb": 3, "circuit": 3, "signal processing": 4, "controls": 3,
    "controls engineer": 4, "power systems": 3, "communications": 3, "rf": 3,

    # ── Robotics / Autonomy ────────────────────────────────────────────────────
    "robotics": 4, "autonomy": 4, "autonomous systems": 4,
    "sensor fusion": 4,

    # ── Cybersecurity ──────────────────────────────────────────────────────────
    "cybersecurity": 3, "security engineer": 3, "information security": 3,
    "penetration testing": 3, "cryptography": 3,

    # ── Government / Intel / Classified ───────────────────────────────────────
    "intelligence": 3, "signals intelligence": 4, "sigint": 4,
    "geoint": 4, "counter-terrorism": 3, "classified": 3,
    "top secret": 5, "ts/sci": 5, "security clearance": 5,
    "government contractor": 3, "federal": 2, "ic": 2,
    "mission systems": 3, "c4isr": 4, "command and control": 3,

    # ── Non-Tech Industries that hire SWEs ────────────────────────────────────
    "fleet management": 2, "iot": 2, "telematics": 3,
    "supply chain software": 3, "logistics software": 3,
    "insurance technology": 3, "insurtech": 3,
    "automotive software": 3, "connected vehicle": 3, "adas": 4,
    "smart grid": 3, "energy software": 3, "scada": 4,
    "retail technology": 2, "e-commerce": 2,
    "edtech": 2, "legal tech": 2, "proptech": 2,
}

EXCLUDE_KEYWORDS = [
    "accounting", "sales", "marketing", "human resources", "hr ",
    "recruiter", "finance intern", "business analyst", "supply chain",
    "mechanical only", "civil engineer", "chemist", "legal", "paralegal",
    "graphic design", "copywriter", "content writer", "social media",
]

# Countries/cities clearly outside the US — used to filter non-US postings
NON_US_LOCATIONS = [
    "canada", "ontario", "toronto", "vancouver", "montreal", "british columbia",
    "alberta", "calgary", "ottawa",
    "united kingdom", "england", "scotland", "london", "manchester",
    "germany", "berlin", "munich", "frankfurt", "hamburg",
    "france", "paris", "lyon",
    "india", "bangalore", "hyderabad", "mumbai", "delhi", "pune", "chennai",
    "australia", "sydney", "melbourne", "brisbane",
    "singapore",
    "netherlands", "amsterdam",
    "ireland", "dublin",
    "spain", "madrid", "barcelona",
    "poland", "warsaw", "krakow",
    "sweden", "stockholm",
    "brazil", "são paulo", "sao paulo",
    "mexico", "mexico city",
    "china", "beijing", "shanghai", "shenzhen",
    "japan", "tokyo",
    "south korea", "seoul",
    "taiwan", "taipei",
    "israel", "tel aviv",
    "switzerland", "zurich",
    "austria", "vienna",
    "portugal", "lisbon",
    "italy", "milan", "rome",
    "denmark", "copenhagen",
    "finland", "helsinki",
    "norway", "oslo",
    "belgium", "brussels",
    "czech republic", "prague",
    "hungary", "budapest",
    "romania", "bucharest",
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


def is_us_or_remote(job):
    """Return True if job is in the US or explicitly remote. Exclude known non-US locations."""
    locations = job.get("locations", [])
    if isinstance(locations, str):
        locations = [locations]
    if not locations or locations == ["Unknown"]:
        return True  # don't filter unknowns — benefit of the doubt

    text = " ".join(locations).lower()

    # Remote is always fine
    if "remote" in text:
        return True

    # Explicitly filter out known non-US locations
    for place in NON_US_LOCATIONS:
        if place in text:
            return False

    return True  # default: keep it


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
    """Return the actual state abbreviation, 'Remote', or '' (blank)."""
    locations = job.get("locations", [])
    if isinstance(locations, str):
        locations = [locations]
    text = " " + " ".join(locations).lower() + " "

    if "remote" in text:
        return "Remote"

    for phrase, abbr in STATE_MAP.items():
        if phrase in text:
            return abbr

    return ""


def location_priority(job):
    """NJ=4, PA=3, NY=2, Remote=1, everything else=0."""
    state = get_state_label(job)
    return {"NJ": 4, "PA": 3, "NY": 2, "Remote": 1}.get(state, 0)


# ── Filter & sort ─────────────────────────────────────────────────────────────

def filter_jobs(jobs, internships_only=True, active_only=True, min_score=4, us_only=True):
    filtered = []
    for job in jobs:
        if active_only and not job.get("active", True):
            continue
        if internships_only and not is_likely_internship(job):
            continue
        if us_only and not is_us_or_remote(job):
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
