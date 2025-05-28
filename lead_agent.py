import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from serpapi import GoogleSearch

# Keywords
keywords = [
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

# SerpAPI Key aus Umgebungsvariable
serpapi_key = os.getenv("SERPAPI_KEY")
if not serpapi_key:
    raise Exception("SERPAPI_KEY Umgebungsvariable nicht gesetzt")

# Gesehene Links lokal speichern, um Dopplungen zu vermeiden
seen_links_file = "seen_links.txt"
if not os.path.exists(seen_links_file):
    open(seen_links_file, 'w').close()

with open(seen_links_file, "r") as f:
    seen_links = set(line.strip() for line in f.readlines())

new_links = []

# Suche starten
for keyword in keywords:
    print(f"🔍 Suche: {keyword}")
    params = {
        "q": keyword,
        "location": "Germany",
        "hl": "de",
        "gl": "de",
        "api_key": serpapi_key,
        "num": 20
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link")
            if link and link not in seen_links:
                new_links.append((keyword, link))
                seen_links.add(link)

# E-Mail vorbereiten
if new_links:
    body = "Hier sind neue potenzielle Kunden:\n"
    grouped = {}
    for keyword, link in new_links:
        if keyword not in grouped:
            grouped[keyword] = []
        grouped[keyword].append(link)

    for keyword, links in grouped.items():
        body += f"\n🔍 {keyword}\n"
        for link in links[:3]:  # max. 3 pro Kategorie
            body += f"➡️ {link}\n"

    msg = MIMEMultipart()
    msg['From'] = "lead-agent@james-fuse.de"
    msg['To'] = "info@james-fuse.de"
    msg['Subject'] = "Neue potenzielle Kunden für Sicherungen"
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.ionos.de", 465)
        server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
        print("✉️ E-Mail erfolgreich gesendet")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")
else:
    print("❌ Keine neuen Links gefunden.")

# Neue Links speichern
with open(seen_links_file, "a") as f:
    for _, link in new_links:
        f.write(link + "\n")
