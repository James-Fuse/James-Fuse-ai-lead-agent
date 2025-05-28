import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from serpapi import GoogleSearch

# Stichworte definieren
suche_keywords = [
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

# API-Key von SerpAPI (Google Suche)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Lead-Historie
CACHE_DATEI = "versendete_leads.json"
if os.path.exists(CACHE_DATEI):
    with open(CACHE_DATEI, "r") as f:
        bekannte_links = set(json.load(f))
else:
    bekannte_links = set()

neue_gesamt = []

# Durchsuche jede Anfrage
for keyword in suche_keywords:
    params = {
        "engine": "google",
        "q": keyword,
        "location": "Germany",
        "hl": "de",
        "api_key": SERPAPI_API_KEY,
        "num": 10
    }
    suche = GoogleSearch(params)
    ergebnisse = suche.get_dict()

    neue_links = []
    for ergebnis in ergebnisse.get("organic_results", []):
        link = ergebnis.get("link")
        if link and link not in bekannte_links:
            neue_links.append(link)

    neue_links = neue_links[:10]  # Begrenze auf max. 10
    if neue_links:
        neue_gesamt.append(f"\n\U0001F50D {keyword}")
        neue_gesamt.extend([f"➔ {l}" for l in neue_links])
        bekannte_links.update(neue_links)

# Ergebnisse speichern
with open(CACHE_DATEI, "w") as f:
    json.dump(list(bekannte_links), f)

# E-Mail senden
def sende_email(text):
    absender = "info@james-fuse.de"
    empfaenger = "info@james-fuse.de"
    betreff = "Neue potenzielle Kunden (max 10 Leads pro Suche)"

    msg = MIMEMultipart()
    msg["From"] = absender
    msg["To"] = empfaenger
    msg["Subject"] = betreff

    msg.attach(MIMEText(text, "plain"))

    server = smtplib.SMTP("smtp.ionos.de", 587)
    server.starttls()
    server.login(absender, os.getenv("EMAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()

# Wenn neue Leads vorhanden, E-Mail senden
if neue_gesamt:
    inhalt = "\n".join(neue_gesamt)
else:
    inhalt = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nKeine neuen Leads gefunden."

sende_email(inhalt)
