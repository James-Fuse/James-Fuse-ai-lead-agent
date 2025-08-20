import os
from datetime import datetime
from typing import List, Dict

from .storage import write_csv
from .emailer import send_email

def collect_leads() -> List[Dict]:
    # Platzhalter für echte Scraper
    leads = [
        {
            "company": "Testfirma GmbH",
            "website": "https://www.beispiel.de",
            "contact_name": "Max Mustermann",
            "email": "info@beispiel.de",
            "phone": "+49 123 456789",
            "source": "Demo",
            "note": "Dies ist nur ein Testeintrag"
        }
    ]
    return leads

def main():
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    recipients_env = os.getenv("RECIPIENTS", "info@james-fuse.de")
    recipients = [x.strip() for x in recipients_env.split(",") if x.strip()]
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    leads = collect_leads()

    csv_path = "/tmp/leads.csv"
    write_csv(leads, csv_path)

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    subject = f"[Lead-Agent] {len(leads)} neue Leads – {ts}"
    body = (
        f"Hi Justin,\n\n"
        f"Heute {len(leads)} Treffer. Die CSV hängt an.\n"
        f"Später bauen wir Bund, TED, eBay usw. dazu.\n\n"
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
