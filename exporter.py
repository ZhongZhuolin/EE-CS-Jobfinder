from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from zipfile import BadZipFile
from datetime import datetime
from filter import get_state_label
import os

EXCEL_FILE = "job_tracker.xlsx"

HEADERS = [
    "Title", "Company", "Posted Date", "Days Ago", "State",
    "Score", "Source", "Locations", "Link",
    "Applied", "Priority", "Resume Ver.", "Cover Letter", "Status", "Notes"
]

COL = {h: i + 1 for i, h in enumerate(HEADERS)}


def format_posted_date(job):
    ts = job.get("date_updated_ts", 0)
    if ts and ts > 0:
        try:
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        except Exception:
            pass
    raw = str(job.get("date_updated", "")).strip()
    return datetime.fromtimestamp(int(raw)).strftime("%Y-%m-%d") if raw.isdigit() else raw


def days_since_posted(job):
    ts = job.get("date_updated_ts", 0)
    if ts and ts > 0:
        try:
            return (datetime.now() - datetime.fromtimestamp(ts)).days
        except Exception:
            pass
    raw = str(job.get("date_updated", "")).strip()
    if raw.isdigit():
        try:
            return (datetime.now() - datetime.fromtimestamp(int(raw))).days
        except Exception:
            pass
    return ""


def load_existing_manual_data(ws):
    manual_data = {}
    headers = {}
    for col in range(1, ws.max_column + 1):
        val = ws.cell(row=1, column=col).value
        if val:
            headers[str(val).strip()] = col

    required = ["Link", "Applied", "Priority", "Resume Ver.", "Cover Letter", "Status", "Notes"]
    if not all(k in headers for k in required):
        return manual_data

    for row in range(2, ws.max_row + 1):
        url_val = ws.cell(row=row, column=headers["Link"]).value
        if not url_val:
            continue
        url_str = str(url_val).strip()
        if url_str.upper().startswith('=HYPERLINK('):
            try:
                url_str = url_str.split('"')[1]
            except IndexError:
                pass
        manual_data[url_str] = {
            "Applied":       ws.cell(row=row, column=headers["Applied"]).value or "",
            "Priority":      ws.cell(row=row, column=headers["Priority"]).value or "",
            "Resume Ver.":   ws.cell(row=row, column=headers["Resume Ver."]).value or "",
            "Cover Letter":  ws.cell(row=row, column=headers["Cover Letter"]).value or "",
            "Status":        ws.cell(row=row, column=headers["Status"]).value or "",
            "Notes":         ws.cell(row=row, column=headers["Notes"]).value or "",
        }
    return manual_data


def export_jobs_to_excel(jobs):
    manual_data = {}
    if os.path.exists(EXCEL_FILE):
        try:
            old_wb = load_workbook(EXCEL_FILE)
            manual_data = load_existing_manual_data(old_wb.active)
        except BadZipFile:
            print(f"{EXCEL_FILE} is corrupt — recreating.")
        except Exception as e:
            print(f"Could not read existing workbook: {e}")

    wb = Workbook()
    ws = wb.active
    ws.title = "Jobs"

    header_fill = PatternFill("solid", start_color="1F3864")
    header_font = Font(bold=True, color="FFFFFF", name="Arial", size=10)
    center      = Alignment(horizontal="center", vertical="center")

    for col_idx, header in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
    ws.row_dimensions[1].height = 22

    STATE_FILLS = {
        "NJ":     PatternFill("solid", start_color="E2EFDA"),
        "PA":     PatternFill("solid", start_color="DDEEFF"),
        "NY":     PatternFill("solid", start_color="FFF2CC"),
        "Remote": PatternFill("solid", start_color="F3E5F5"),
    }
    ALT_FILL    = PatternFill("solid", start_color="F7F9FC")
    thin_border = Border(bottom=Side(style="thin", color="D0D0D0"))

    for row_idx, job in enumerate(jobs, 2):
        url   = str(job.get("url", "")).strip()
        saved = manual_data.get(url, {})
        state = get_state_label(job)

        applied_val  = saved.get("Applied",  "") or ("Yes" if job.get("applied") else "No")
        priority_val = saved.get("Priority", job.get("priority", "") or "")
        status_val   = saved.get("Status",   job.get("status",  "") or "")
        notes_val    = saved.get("Notes",    job.get("notes",   "") or "")
        link_formula = f'=HYPERLINK("{url}","Open")' if url else ""

        row_data = [
            job.get("title", ""),
            job.get("company_name", ""),
            format_posted_date(job),
            days_since_posted(job),
            state,
            job.get("match_score", 0),
            job.get("source", ""),
            ", ".join(job.get("locations", [])) if isinstance(job.get("locations", []), list) else str(job.get("locations", "")),
            link_formula,
            applied_val, priority_val,
            saved.get("Resume Ver.", ""), saved.get("Cover Letter", ""),
            status_val, notes_val,
        ]

        row_fill = STATE_FILLS.get(state, ALT_FILL if row_idx % 2 == 0 else None)

        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font      = Font(name="Arial", size=9)
            cell.alignment = Alignment(vertical="center")
            cell.border    = thin_border
            if row_fill:
                cell.fill = row_fill

            if col_idx == COL["Link"]:
                cell.font = Font(name="Arial", size=9, color="1155CC", underline="single")
                cell.alignment = center

            if col_idx == COL["Score"]:
                score = job.get("match_score", 0)
                cell.alignment = center
                if score >= 10:
                    cell.font = Font(name="Arial", size=9, bold=True, color="1A6B2A")
                elif score >= 7:
                    cell.font = Font(name="Arial", size=9, bold=True, color="7B4F00")
                else:
                    cell.font = Font(name="Arial", size=9, color="555555")

            if col_idx == COL["Days Ago"]:
                cell.alignment = center
                try:
                    if int(value) > 14:
                        cell.font = Font(name="Arial", size=9, color="C00000")
                except (TypeError, ValueError):
                    pass

            if col_idx in (COL["State"], COL["Source"], COL["Posted Date"],
                           COL["Applied"], COL["Priority"]):
                cell.alignment = center

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    col_widths = {
        "Title": 38, "Company": 22, "Posted Date": 13, "Days Ago": 9,
        "State": 8, "Score": 7, "Source": 13, "Locations": 28,
        "Link": 10, "Applied": 10, "Priority": 9, "Resume Ver.": 13,
        "Cover Letter": 13, "Status": 16, "Notes": 30,
    }
    for header, width in col_widths.items():
        ws.column_dimensions[get_column_letter(COL[header])].width = width

    max_row = ws.max_row

    def add_dv(formula, col_letter):
        dv = DataValidation(type="list", formula1=formula, allow_blank=True, showDropDown=False)
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}2:{col_letter}{max_row}")

    add_dv('"Yes,No"',                                        get_column_letter(COL["Applied"]))
    add_dv('"1,2,3,4,5"',                                     get_column_letter(COL["Priority"]))
    add_dv('"Applied,Interviewing,Offer,Rejected,Too Lazy"',  get_column_letter(COL["Status"]))

    try:
        wb.save(EXCEL_FILE)
        print(f"Saved {EXCEL_FILE} ({len(jobs)} jobs)")
    except PermissionError:
        print(f"Could not save {EXCEL_FILE} — close it in Excel first.")