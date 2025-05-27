import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os
import json

SUCHBEGRIFFE = [
    "Sicherung kaufen", "Class CC Sicherung gesucht", "Sicherung gesucht Steuerung",
    "Industriesicherung Bedarf", "Maschinenbauer Sicherungen", "Schaltanlagen Ersatzteile",
    "Sicherungslieferant gesucht", "Elektriker Sicherung Bedarf", "CSA Sicherung bestellen",
    "UL Sicherung Ersatz", "Lieferant elektrische Sicherungen", "Sicherung defekt Austausch"
]

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

ARCHIV_DATEI = "versendete_leads.json"

def google_suche(begriff):
    url = f"https://www.google.com/search?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "url?q=" in href:
            match = re.search(r"url\\?q=(https?://[^&]+)", href)
            if match:
                links.append(match.group(1))
    return links

def wlw_suche(begriff):
    url = f"https://www.wlw.de/de/suche?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/firma/" in href:
            links.append("https://www.wlw.de" + href)
    return links

def lade_bekannte_links():
    if os.path.exists(ARCHIV_DATEI):
        with open(ARCHIV_DATEI, "r") as f:
            return set(json.load(f))
    return set()

def speichere_bekannte_links(link_set):
    with open(ARCHIV_DATEI, "w") as f:
        json.dump(list(link_set), f)

def sende_email(text):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "🎯 Neue Leads aus der aktuellen Suche"
    msg.set_content(text)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

def suche_leads():
    bekannte_links = lade_bekannte_links()
    neue_links = set()
    ergebnisse = {}

    for begriff in SUCHBEGRIFFE:
        print(f"🔍 Suche: {begriff}")
        links = wlw_suche(begriff) + google_suche(begriff)
        links = [link for link in links if link not in bekannte_links]
        if links:
            unique = list(dict.fromkeys(links))  # Duplikate entfernen
            ergebnisse[begriff] = unique[:3]  # Nur 3 pro Begriff nehmen
            neue_links.update(ergebnisse[begriff])
        time.sleep(1)

    return ergebnisse, bekannte_links, neue_links

if __name__ == "__main__":
    ergebnisse, bekannte_links, neue_links = suche_leads()
    if neue_links:
        text = ""
        anzahl = 0
        for begriff, links in ergebnisse.items():
            if anzahl >= 10:
                break
            beitrag = f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links)
            text += beitrag + "\n"
            anzahl += len(links)
        sende_email(text)
        bekannte_links.update(new_links)
        speichere_bekannte_links(bekannte_links)
    else:
        sende_email("❌ Keine neuen Leads gefunden – Agent aktiv, aber keine neuen Ergebnisse.")
