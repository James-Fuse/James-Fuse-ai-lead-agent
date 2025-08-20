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
    recipients = [x.strip() for x in recipients_env.split(",") if x.strip()]
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    leads = collect_leads()

    # CSV schreiben (auch wenn keine Treffer, damit Anhang existiert)
    csv_path = "/tmp/leads.csv"
    if leads:
        write_csv(leads, csv_path)
    else:
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("note\nkeine Treffer\n")

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    subject = f"[Lead-Agent] {len(leads)} neue Leads – {ts}"
    body = (
        f"Hi Justin,\n\n"
        f"Heute {len(leads)} Treffer. Die CSV hängt an.\n"
        f"Quelle: Website-Scanner (targets.txt) mit Keywords aus SEARCH_TERMS_JSON.\n\n"
        f"LG\nDein Lead-Agent"
    )

    send_email(
        sender=smtp_user,
        password=smtp_pass,
        recipients=recipients,
        subject=subject,
        body=body,
        attachments=[csv_path],
        smtp_host=smtp_host,
        smtp_port=smtp_port,
    )

if __name__ == "__main__":
    main()
