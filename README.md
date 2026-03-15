# EE/CS Internship Tracker

Automated job tracker for **Electrical Engineering and Computer Science internships** in defense, embedded systems, biomedical, and robotics. Pulls from 60+ companies daily, scores and filters by relevance, and exports a clean Excel file with one-click apply links.

Built for EE/CS students targeting defense/aerospace startups, medical device companies, and embedded systems roles — especially those with DoD clearances or NJ/PA/NY location preferences.

---

## What It Does

- Scrapes **SimplifyJobs**, **Indeed RSS**, **Greenhouse**, and **Workday** job boards daily
- Scores each job by keyword relevance (embedded, firmware, defense, biomedical, etc.)
- Filters to internships only, drops anything older than 2 weeks
- Prioritizes NJ → PA → NY → Remote
- Exports `job_tracker.xlsx` with clickable links, dropdowns for status tracking, and color-coded rows by state
- Sends Discord alerts for high-match new jobs (score ≥ 6)
- Remembers your Applied / Status / Notes between runs

---

## Companies Tracked

**Defense & Aerospace**
Anduril, Shield AI, Rebellion Defense, Epirus, Saildrone, Hermeus, True Anomaly, Umbra, Slingshot Aerospace, Vannevar Labs, Apex Space, Ursa Major, L3Harris, BAE Systems, Northrop Grumman, Raytheon, General Dynamics, Leidos, SAIC

**Robotics & Autonomy**
Apptronik, Skydio, Gecko Robotics, Machina Labs, Covariant, Robust AI, Dusty Robotics, Symbotic, Dextrous Robotics, Viam

**Biomedical & Neurotech**
Kernel, Synchron, Hyperfine, Proprio, Avail Medsystems, Sword Health, Hinge Health, Medtronic, Johnson & Johnson, Siemens Healthineers

**Tech**
Palantir, SpaceX, OpenAI, Govini, Verkada + SimplifyJobs aggregator (500+ companies)

---

## Setup

**Requirements:** Python 3.9+

```bash
git clone https://github.com/YOUR_USERNAME/ee-cs-job-tracker
cd ee-cs-job-tracker
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

**Run:**
```bash
python main.py
```

Opens `job_tracker.xlsx` when done.

---

## Discord Alerts (Optional)

1. Create a Discord webhook in any channel (Edit Channel → Integrations → Webhooks)
2. Open `alerts.py` and paste your webhook URL:
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```
Jobs with a match score ≥ 6 will ping you automatically on each run.

---

## Automating Daily Runs

**Windows Task Scheduler:**
1. Open Task Scheduler → Create Basic Task
2. Trigger: Daily at 8:00 AM
3. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `main.py`
   - Start in: `C:\path\to\ee-cs-job-tracker`

**Mac/Linux (cron):**
```bash
crontab -e
# Add:
0 8 * * * /path/to/venv/bin/python /path/to/ee-cs-job-tracker/main.py
```

---

## Excel Columns

| Column | Description |
|---|---|
| Title | Job title |
| Company | Company name |
| Posted Date | Date job was posted |
| Days Ago | Days since posting (red if > 14) |
| State | NJ / PA / NY / Remote / etc. |
| Score | Relevance score (green ≥ 10, amber ≥ 7) |
| Source | SimplifyJobs / Indeed / Greenhouse / Workday |
| Link | One-click link to job posting |
| Applied | Yes / No dropdown |
| Priority | 1–5 dropdown |
| Resume Ver. | Track which resume version you sent |
| Cover Letter | Track if you wrote one |
| Status | Applied / Interviewing / Offer / Rejected / Too Lazy |
| Notes | Free text |

Applied/Status/Notes are **preserved between runs** — updating the Excel and re-running will not overwrite your entries.

---

## Scoring System

Jobs are scored by keyword matches in the title, company, and location:

| Keywords | Points |
|---|---|
| Embedded, firmware, medical device, DoD, defense | 5 |
| Electrical engineering, biomedical, FPGA, RTOS | 4–5 |
| Robotics, signal processing, autonomy, radar | 3–4 |
| Software engineering, Python, C++, machine learning | 2–4 |

Jobs scoring below 4 are filtered out. Discord alerts fire at score ≥ 6.

---

## Project Structure

```
ee-cs-job-tracker/
├── main.py              # Entry point
├── fetcher.py           # Pulls jobs from all sources
├── filter.py            # Scoring, filtering, sorting
├── exporter.py          # Builds job_tracker.xlsx
├── database.py          # SQLite persistence
├── sources.py           # Greenhouse + Workday scrapers
├── company_sources.py   # List of all tracked companies
├── alerts.py            # Discord webhook alerts
├── utils.py             # Deduplication
├── requirements.txt
└── README.md
```

---

## Contributing

PRs welcome. To add a company:

**Greenhouse** — add to `GREENHOUSE_BOARDS` in `company_sources.py`:
```python
{"company_name": "Your Company", "board_token": "theirtoken"},
```
Find the board token in their careers URL: `boards.greenhouse.io/BOARDTOKEN`

**Workday** — add to `WORKDAY_SOURCES`:
```python
{"company_name": "Your Company", "url": "https://company.wd5.myworkdayjobs.com/wday/cxs/company/External/jobs"}
```

---

## License

MIT
