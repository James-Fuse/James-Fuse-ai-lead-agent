import os
from datetime import datetime
from typing import List, Dict

from .storage import write_csv
from .emailer import send_email
from .sources.website_scanner import run as run_website_scan  # nutzt targets.txt

def collect_leads() -> List[Dict]:
    """Sammelt echte Leads über den Website-Scanner (targets.txt + SEARCH_TERMS_JSON)."""
    keywords_json = os.getenv("SEARCH_TERMS_JSON", '[]')
    leads: List[Dict] = []
    try:
        leads += run_website_scan(keywords_json, targets_path="targets.txt")
    except Exception as e:
        print(f"[website_scanner] Fehler: {e}")
    return leads

def main():
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    recipients_env = os.getenv("RECIPIENTS", "info@james-fuse.de")
    recipients = [x.strip() for x in recipients_env.spl_]()
