import os
import json
import smtplib
import subprocess
from email.mime.text import MIMEText
from datetime import datetime

# SerpAPI dynamisch installieren, falls nicht vorhanden
try:
    from serpapi import GoogleSearch
except ModuleNotFoundError:
    subprocess.check_call(["pip", "install", "serpapi"])
    from serpapi import GoogleSearch

# Liste der Suchbegriffe
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

# Datei zur Speicherung bereits gesendeter Links
dateipfad = "gesendete_links.json"

# Alte Links laden
if os.path.exists(dateipfad):
    with open(dateipfad, "r") as f:
        bekannte_links = set(json.load(f))
else:
    bekannte_links = set()

neue_links = []
serpapi_key = os.getenv("SERPAPI_API_KEY")

for begriff in suchbegriffe:
    print(f"🔍 Suche: {begriff}")
    params = {
        "engine": "google",
        "q": begriff,
        "hl": "de",
        "gl": "de",
        "num": "20",
        "api_key": serpapi_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link", "")
            if link and link not in bekannte_links:
                neue_links.append(f"{link}")
                bekannte_links.add(link)

# Maximal 10 neue Leads pro Durchlauf
max_links = neue_links[:10]

if max_links:
    # E-Mail vorbereiten
    inhalt = "Neue Leads gefunden:\n\n" + "\n".join(max_links)
else:
    inhalt = "Keine neuen Leads gefunden – alles ist auf dem aktuellen Stand."

msg = MIMEText(inhalt)
msg["Subject"] = f"Leads Update – {datetime.now().strftime('%Y-%m-%d %H:%M')}"
msg["From"] = "lead-agent@james-fuse.de"
msg["To"] = "info@james-fuse.de"

# E-Mail senden
server = smtplib.SMTP("smtp.ionos.de", 587)
server.starttls()
server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
server.send_message(msg)
server.quit()

print("✅ E-Mail versendet.")

# Gesendete Links speichern
with open(dateipfad, "w") as f:
    json.dump(list(bekannte_links), f)
