import os
from datetime import datetime
from typing import List, Dict

from .storage import write_csv
from .emailer import send_email

def collect_leads() -> List[Dict]:
    """
    Dummy-Sammler: hier kannst du später Bund, TED, eBay usw. einbauen.
    Aktuell gibt er nur einen Test-Lead zurück.
    """
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

    # Leads sammeln
    leads = collect_leads()

    # CSV-Datei erzeuge
