# lead_agent_combined.py
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time
import json

# Beispielhafte Ergebnisstruktur (diese würde in der Praxis aus echten Scrapes generiert werden)
results = {
    "timestamp": datetime.now().isoformat(),
    "unternehmenswebsites": [
        {"firma": "Elektro Müller GmbH", "url": "https://www.wlw.de/de/firma/elektro-mueller-gmbh-123456", "grund": "Website erwähnt UL Sicherung"}
    ],
    "forenbeitraege": [],
    "ausschreibungen": [],
    "neugründungen": [],
    "kleinanzeigen": [],
    "jobanzeigen": []
}

# Email-Inhalt
body_text = "Sehr geehrte Damen und Herren,\n\n"
body_text += "mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann. Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten.\n\n"
body_text += "Unsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards. Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen. Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich.\n\n"
body_text += "Viele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen. Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen. Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit.\n\n"
body_text += "Ich würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen. Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment.\n\n"
body_text += "Vielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.\n\n"
body_text += "Mit freundlichen Grüßen,\n\nJustin James\nManaging Director | James Fuse & Beyond GmbH\nGeorg-Pingler-Straße 15\n61462 Königstein im Taunus, Germany\nPhone: +49 6174 9699645\nEmail: info@james-fuse.de\nWebsite: www.james-fuse.de"

# Funktion zum Versenden der E-Mail mit Lead-Infos
msg = EmailMessage()
msg["Subject"] = "Neue potenzielle Leads zur Kontaktaufnahme"
msg["From"] = "lead-agent@james-fuse.de"
msg["To"] = "info@james-fuse.de"
msg.set_content(body_text)

# SMTP Login mit Umgebungsvariablen
email_password = os.getenv("EMAIL_PASSWORD")
if email_password is None:
    raise ValueError("EMAIL_PASSWORD Umgebungsvariable nicht gesetzt")

with smtplib.SMTP("smtp.ionos.de", 587) as server:
    server.starttls()
    server.login("lead-agent@james-fuse.de", email_password)
    server.send_message(msg)

print("✅ Email gesendet mit potenziellen Leads und Kontakttext.")
