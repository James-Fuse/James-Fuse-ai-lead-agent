import os
import json
import smtplib
import time
import requests
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from datetime import datetime

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

dateipfad = "gesendete_links.json"

# Vorherige Links laden
if os.path.exists(dateipfad):
    with open(dateipfad, "r") as f:
        bekannte_links = set(json.load(f))
else:
    bekannte_links = set()

neue_links = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

def bing_search(query):
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for li in soup.select(".b_algo h2 a"):
        href = li.get("href")
        if href and href not in bekannte_links:
            results.append(href)
    return results

for begriff in suchbegriffe:
    print(f"🔍 Suche: {begriff}")
    treffer = bing_search(begriff)
    for link in treffer:
        if len(neue_links) >= 10:
            break
        neue_links.append(link)
        bekannte_links.add(link)
    time.sleep(2)  # kurze Pause für stabile Abfragen

# Max. 10 neue Leads pro Durchlauf
max_links = neue_links[:10]

if max_links:
    inhalt = "Neue Leads gefunden:\n\n" + "\n".join(max_links)
else:
    inhalt = "Keine neuen Leads gefunden – alles ist auf dem aktuellen Stand."

# E-Mail senden
msg = MIMEText(inhalt)
msg["Subject"] = f"Leads Update – {datetime.now().strftime('%Y-%m-%d %H:%M')}"
msg["From"] = "lead-agent@james-fuse.de"
msg["To"] = "info@james-fuse.de"

server = smtplib.SMTP("smtp.ionos.de", 587)
server.starttls()
server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
server.send_message(msg)
server.quit()

print("✅ E-Mail versendet.")

# Neue Links speichern
with open(dateipfad, "w") as f:
    json.dump(list(bekannte_links), f)
