import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from serpapi import GoogleSearch

# Suchbegriffe
suchbegriffe = [
    "Sicherung kaufen",
    "Class CC Sicherung gesucht",
    "Sicherung gesucht Steuerung",
    "Industriesicherung Bedarf",
    "Maschinenbauer Sicherungen",
    "Schaltanlagen Ersatzteile",
    "Sicherungslieferant gesucht",
    "Elektriker Sicherung Bedarf",
    "CSA Sicherung bestellen",
    "UL Sicherung Ersatz",
    "Lieferant elektrische Sicherungen",
    "Sicherung defekt Austausch"
]

# Ergebnisse speichern
neue_links = set()
bekannte_links_path = "bekannte_links.txt"

# Lade bekannte Links
if os.path.exists(bekannte_links_path):
    with open(bekannte_links_path, "r") as file:
        bekannte_links = set(file.read().splitlines())
else:
    bekannte_links = set()

# SerpAPI Key (aus Umgebungsvariable)
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Ergebnisse suchen
for begriff in suchbegriffe:
    print(f"🔍 Suche: {begriff}")
    params = {
        "q": begriff,
        "location": "Germany",
        "hl": "de",
        "gl": "de",
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": "20"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if link and link not in bekannte_links:
                neue_links.add(link)

# E-Mail versenden (wenn neue Links vorhanden)
if neue_links:
    email_sender = "lead-agent@james-fuse.de"
    email_receiver = "info@james-fuse.de"
    email_password = os.getenv("EMAIL_PASSWORD")

    subject = "Neue Leads für Sicherungen gefunden"
    body = "Hier sind neue potenzielle Kunden:
\n\n" + "\n".join(list(neue_links)[:10])

    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.strato.de", 465) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            print("📧 E-Mail erfolgreich gesendet!")
    except smtplib.SMTPAuthenticationError:
        print("❌ Fehler: E-Mail-Zugangsdaten sind ungültig.")
else:
    print("ℹ️ Keine neuen Leads gefunden.")

# Neue Links zur Liste hinzufügen
bekannte_links.update(neue_links)
with open(bekannte_links_path, "w") as file:
    file.write("\n".join(bekannte_links))
