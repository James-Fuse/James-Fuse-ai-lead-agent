# Erweiterter Lead-Agent für James Fuse & Beyond GmbH
# Ziel: kontinuierliche Lead-Suche über mehrere Plattformen mit Speicher der letzten Ergebnisse

import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib
import os
import json
from email.message import EmailMessage
from datetime import datetime

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "FNQ-R fuse", "LP-CC fuse", "KTK-R fuse", "FNM-15 fuse", "LPJ fuse",
    "Bussmann Sicherungen kaufen", "Industriesicherung gesucht", "Class CC Sicherung", "UL fuse kaufen",
    "Sicherungsbedarf Schaltschränke", "Sicherung für Sondermaschinen", "fuse supplier germany",
    "ATQR fuse", "ATDR fuse", "AJT fuse", "TRM15 fuse", "midget fuse 600V"
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
ARCHIV_DATEI = "lead_verlauf.json"
MAX_TREFFER_PRO_SEITE = 20

# === HELFER ===
def lade_verlauf():
    if os.path.exists(ARCHIV_DATEI):
        with open(ARCHIV_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_verlauf(verlauf):
    with open(ARCHIV_DATEI, "w") as f:
        json.dump(verlauf, f, indent=2)

# === SUCHE ===
def google_suche(begriff):
    links = []
    for start in range(0, MAX_TREFFER_PRO_SEITE * 2, 10):
        url = f"https://www.google.com/search?q={requests.utils.quote(begriff)}&start={start}"
        r = requests.get(url, headers=USER_AGENT)
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "url?q=" in href:
                match = re.search(r"url\\?q=(https?://[^&]+)", href)
                if match:
                    links.append(match.group(1))
        time.sleep(1)
    return links

def wlw_suche(begriff):
    url = f"https://www.wlw.de/de/suche?q={requests.utils.quote(begriff)}"
    r = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(r.text, "html.parser")
    return ["https://www.wlw.de" + a["href"] for a in soup.find_all("a", href=True) if "/firma/" in a["href"]]

def ebay_kleinanzeigen_suche(begriff):
    url = f"https://www.ebay-kleinanzeigen.de/s-suche.html?keywords={requests.utils.quote(begriff)}"
    r = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(r.text, "html.parser")
    return ["https://www.ebay-kleinanzeigen.de" + a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("/s-anzeige/")]

def alibaba_suche(begriff):
    url = f"https://german.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={requests.utils.quote(begriff)}"
    r = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(r.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("https://german.alibaba.com/product-detail/")]

# === EMAIL ===
def sende_email(text):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Neue Treffer gefunden"
    msg.set_content(text)

    pw = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", pw)
        server.send_message(msg)

# === HAUPTLOGIK ===
def suche_und_filter():
    alt = lade_verlauf()
    neu = {}
    neue_treffer = {}

    for begriff in SUCHBEGRIFFE:
        links = set()
        links.update(google_suche(begriff))
        links.update(wlw_suche(begriff))
        links.update(ebay_kleinanzeigen_suche(begriff))
        links.update(alibaba_suche(begriff))

        gefiltert = [l for l in links if l not in alt.get(begriff, [])]
        if gefiltert:
            neue_treffer[begriff] = gefiltert
        neu[begriff] = list(links)

    speichere_verlauf(neu)
    return neue_treffer

# === AUSFÜHRUNG ===
if __name__ == "__main__":
    treffer = suche_und_filter()
    if treffer:
        mail = "🚀 Neue Leads gefunden:\n\n"
        for begriff, links in treffer.items():
            mail += f"🔍 {begriff}\n" + "\n".join(f"➡️ {l}" for l in links) + "\n\n"
        sende_email(mail)
    else:
        sende_email("❌ Es wurden keine neuen Leads gefunden.")
