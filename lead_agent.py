import os
import smtplib
from email.mime.text import MIMEText
from serpapi import GoogleSearch
from datetime import datetime
import json

# SerpAPI key aus Umgebungsvariable holen
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Bisherige Leads speichern/laden
leads_datei = "bekannte_leads.json"
if os.path.exists(leads_datei):
    with open(leads_datei, "r") as f:
        bekannte_links = set(json.load(f))
else:
    bekannte_links = set()

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

neue_links = []

# Google-Suche durchführen
for begriff in suchbegriffe:
    print(f"🔍 Suche: {begriff}")
    params = {
        "q": begriff,
        "location": "Germany",
        "hl": "de",
        "gl": "de",
        "api_key": SERPAPI_API_KEY,
        "engine": "google"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if link and link not in bekannte_links:
                neue_links.append(link)
                bekannte_links.add(link)
            if len(neue_links) >= 10:
                break
    if len(neue_links) >= 10:
        break

# Nur wenn neue Leads gefunden wurden
if neue_links:
    with open(leads_datei, "w") as f:
        json.dump(list(bekannte_links), f)

    # E-Mail senden
    absender = "lead-agent@james-fuse.de"
    empfaenger = "info@james-fuse.de"
    betreff = "Neue potenzielle Kunden für Sicherungen"
    body = "Hier sind neue potenzielle Kunden:\n\n" + "\n".join(f"- {link}" for link in neue_links)

    msg = MIMEText(body)
    msg["Subject"] = betreff
    msg["From"] = absender
    msg["To"] = empfaenger

    server = smtplib.SMTP("smtp.ionos.de", 587)
    server.starttls()
    server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()
else:
    print("Keine neuen Leads gefunden.")
