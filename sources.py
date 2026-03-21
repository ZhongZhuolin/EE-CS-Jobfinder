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


def _parse_workday_response(data, source):
    jobs = []
    for job in data.get("jobPostings", []):
        jobs.append({
            "title": job.get("title", "Unknown Title"),
            "company_name": source["company_name"],
            "url": job.get("externalPath", ""),
            "date_updated": job.get("postedOn", ""),
            "locations": [job.get("locationsText", "Unknown")],
            "active": True,
            "source": "Workday"
        })
    return jobs


def _careers_page_url(api_url):
    """Derive the public careers page URL from a Workday CXS API URL."""
    # https://foo.wd5.myworkdayjobs.com/wday/cxs/foo/SiteName/jobs
    #   -> https://foo.wd5.myworkdayjobs.com/en-US/SiteName
    parts = api_url.split("/")
    base = f"{parts[0]}//{parts[2]}"
    site_name = parts[6] if len(parts) > 6 else "External"
    return f"{base}/en-US/{site_name}"


def _post_workday(session, api_url, csrf_token=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    }
    if csrf_token:
        headers["X-Calypso-CSRF-Token"] = csrf_token
    payload = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}
    response = session.post(api_url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def _fetch_workday_plain(source):
    """
    Try fetching a Workday source with a plain POST (no browser).
    Returns job list on success, None if CSRF is required (422), [] on other failure.
    """
    session = requests.Session()
    try:
        data = _post_workday(session, source["url"])
        jobs = _parse_workday_response(data, source)
        print(f"Fetched {len(jobs)} jobs from Workday ({source['company_name']})")
        return jobs
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 422:
            return None  # Signal: needs CSRF / browser
        print(f"Failed to fetch Workday jobs for {source['company_name']}: {e}")
        return []
    except Exception as e:
        print(f"Failed to fetch Workday jobs for {source['company_name']}: {e}")
        return []


def _fetch_workday_playwright_batch(sources):
    """
    Fetch jobs from Workday sources that require CSRF using a single Playwright
    browser instance (one browser, one page per company).
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium")
        print(f"Skipping {len(sources)} Workday sources that require CSRF.")
        return []

    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for source in sources:
            jobs = _fetch_single_playwright(browser, source)
            all_jobs.extend(jobs)

        browser.close()

    return all_jobs


def _fetch_single_playwright(browser, source):
    """
    Use a Playwright browser page to get the CSRF token, then POST to the API.
    """
    api_url = source["url"]
    careers_url = _careers_page_url(api_url)

    try:
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(careers_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1500)  # Allow cookies to settle

        cookies = context.cookies()
        context.close()

        csrf_token = None
        cookie_jar = {}
        for c in cookies:
            cookie_jar[c["name"]] = c["value"]
            if c["name"] == "CALYPSO_CSRF_TOKEN":
                csrf_token = c["value"]

        if not csrf_token:
            print(f"No CSRF token for {source['company_name']} — skipping")
            return []

        session = requests.Session()
        requests.utils.add_dict_to_cookiejar(session.cookies, cookie_jar)

        data = _post_workday(session, api_url, csrf_token)
        jobs = _parse_workday_response(data, source)
        print(f"Fetched {len(jobs)} jobs from Workday ({source['company_name']})")
        return jobs

    except Exception as e:
        print(f"Failed to fetch Workday jobs for {source['company_name']}: {e}")
        return []


def fetch_lever_board(board_token, company_name):
    """Fetch jobs from a Lever job board (free public API)."""
    url = f"https://api.lever.co/v0/postings/{board_token}?mode=json"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        postings = response.json()
    except Exception as e:
        print(f"Failed to fetch Lever board {board_token}: {e}")
        return []

    jobs = []
    for p in postings:
        jobs.append({
            "title": p.get("text", "Unknown Title"),
            "company_name": company_name,
            "url": p.get("hostedUrl", ""),
            "date_updated": p.get("createdAt", ""),
            "locations": [p.get("categories", {}).get("location", "Unknown")],
            "active": True,
            "source": "Lever",
        })
    print(f"Fetched {len(jobs)} jobs from Lever ({company_name})")
    return jobs


def fetch_all_lever(boards):
    all_jobs = []
    for board in boards:
        all_jobs.extend(fetch_lever_board(board["board_token"], board["company_name"]))
    return all_jobs


def fetch_ashby_board(board_token, company_name):
    """Fetch jobs from an Ashby job board (free public API)."""
    url = f"https://api.ashbyhq.com/posting-api/job-board/{board_token}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch Ashby board {board_token}: {e}")
        return []

    jobs = []
    for p in data.get("jobPostings", []):
        loc = p.get("locationName") or p.get("location") or "Unknown"
        jobs.append({
            "title": p.get("title", "Unknown Title"),
            "company_name": company_name,
            "url": p.get("jobUrl", ""),
            "date_updated": p.get("publishedDate", ""),
            "locations": [loc],
            "active": p.get("isListed", True),
            "source": "Ashby",
        })
    print(f"Fetched {len(jobs)} jobs from Ashby ({company_name})")
    return jobs


def fetch_all_ashby(boards):
    all_jobs = []
    for board in boards:
        all_jobs.extend(fetch_ashby_board(board["board_token"], board["company_name"]))
    return all_jobs


def fetch_remoteok():
    """Fetch remote tech jobs from RemoteOK (free, no auth)."""
    try:
        response = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch RemoteOK: {e}")
        return []

    jobs = []
    for p in data:
        if not isinstance(p, dict) or not p.get("position"):
            continue
        jobs.append({
            "title": p.get("position", "Unknown"),
            "company_name": p.get("company", "Unknown"),
            "url": p.get("url", ""),
            "date_updated": p.get("date", ""),
            "locations": ["Remote"],
            "active": True,
            "source": "RemoteOK",
        })
    print(f"Fetched {len(jobs)} jobs from RemoteOK")
    return jobs


def fetch_all_workday(sources):
    """
    Fetch jobs from all Workday sources.
    - First attempts a plain POST (fast, works for some companies).
    - Sources that return 422 (need CSRF) are batched into a single
      Playwright browser run.
    """
    all_jobs = []
    needs_browser = []

    for source in sources:
        result = _fetch_workday_plain(source)
        if result is None:
            needs_browser.append(source)
        else:
            all_jobs.extend(result)

    if needs_browser:
        print(f"\nUsing browser to fetch {len(needs_browser)} Workday sources that require CSRF...")
        all_jobs.extend(_fetch_workday_playwright_batch(needs_browser))

    return all_jobs
