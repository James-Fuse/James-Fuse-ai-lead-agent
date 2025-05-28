import os
import json
import smtplib
from email.mime.text import MIMEText
from serpapi import GoogleSearch

# Lead-Suchbegriffe
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

# Bisher bekannte Links laden oder leere Menge starten
bekannte_links = set()
if os.path.exists("bekannte_links.json"):
    with open("bekannte_links.json", "r") as f:
        bekannte_links = set(json.load(f))

# Neue Ergebnisse sammeln
unique_links = []

for begriff in suchbegriffe:
    print(f"🔍 Suche: {begriff}")
    params = {
        "engine": "google",
        "q": begriff,
        "hl": "de",
        "location": "Germany",
        "num": 20,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if link and link not in bekannte_links:
                unique_links.append(link)
                bekannte_links.add(link)
                if len(unique_links) >= 10:
                    break
    if len(unique_links) >= 10:
        break

# Links speichern, um Duplikate zu vermeiden
with open("bekannte_links.json", "w") as f:
    json.dump(list(bekannte_links), f)

# Nur wenn neue Links gefunden wurden, E-Mail senden
if unique_links:
    body = """Hier sind neue potenzielle Kunden:\n\n""" + "\n".join(unique_links)

    msg = MIMEText(body)
    msg['Subject'] = 'Neue Lead-Ergebnisse'
    msg['From'] = "lead-agent@james-fuse.de"
    msg['To'] = "info@james-fuse.de"

    server = smtplib.SMTP("smtp.ionos.de", 587)
    server.starttls()
    server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()
