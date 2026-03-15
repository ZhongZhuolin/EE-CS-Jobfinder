import requests

DISCORD_WEBHOOK_URL = "PASTE_YOUR_DISCORD_WEBHOOK_HERE"


def send_discord_alert(job):
    """
    Send one job alert to Discord.
    """
    if DISCORD_WEBHOOK_URL == "PASTE_YOUR_DISCORD_WEBHOOK_HERE":
        print("Discord webhook not set yet. Skipping alert.")
        return

    content = (
        f"**New Job Match**\n"
        f"**Title:** {job.get('title', 'N/A')}\n"
        f"**Company:** {job.get('company_name', 'N/A')}\n"
        f"**Score:** {job.get('match_score', 0)}\n"
        f"**Date:** {job.get('date_updated', 'N/A')}\n"
        f"**Source:** {job.get('source', 'N/A')}\n"
        f"**URL:** {job.get('url', 'N/A')}"
    )

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content}, timeout=15)
        response.raise_for_status()
        print(f"Sent Discord alert for: {job.get('title')}")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")


def send_discord_alerts(jobs, min_score=6):
    """
    Alert only strong matches so you do not get spammed.
    """
    for job in jobs:
        if job.get("match_score", 0) >= min_score:
            send_discord_alert(job)