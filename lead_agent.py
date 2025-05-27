import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os
import json

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "Sicherung kaufen", "Class CC Sicherung gesucht", "Sicherung gesucht Steuerung",
    "Industriesicherung Bedarf", "Maschinenbauer Sicherungen", "Schaltanlagen Ersatzteile",
    "Sicherungslieferant gesucht", "Elektriker Sicherung Bedarf", "CSA Sicherung bestellen",
    "UL Sicherung Ersatz", "Lieferant elektrische Sicherungen", "Sicherung defekt Austausch"
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BEKANNTE_DATEI = "bekannte_links.json"
MAX_LEADS = 10

# === DATEI LADEN UND SPEICHERN ===
def lade_bekannte_links():
    if os.path.exists(BEKANNTE_DATEI):
        with open(BEKANNTE_DATEI, "r") as f:
            return set(json.load(f))
    return set()

def speichere_bekannte_links(links):
    with open(BEKANNTE_DATEI, "w") as f:
        json.dump(list(links), f)

# === WLW-SUCHE ===
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

# === E-MAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Neue potenzielle Kunden"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_filter():
    bekannte_links = lade_bekannte_links()
    neue_links = set()
    ausgabe = ""

    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche: {begriff}")
        links = wlw_suche(begriff)
        ungefiltert = [l for l in links if l not in bekannte_links and not l.startswith("https://www.wlw.de/de/firma/james-fuse")]

        if ungefiltert:
            neue_links.update(ungefiltert)
            ausgabe += f"\n🔍 {begriff}\n"
            for link in ungefiltert[:MAX_LEADS]:
                ausgabe += f"➡️ {link}\n"

        time.sleep(1)

    speichere_bekannte_links(bekannte_links.union(neue_links))

    if ausgabe.strip():
        sende_email(ausgabe)
    else:
        sende_email("❌ Es wurden keine neuen potenziellen Kunden gefunden.")

if __name__ == "__main__":
    suche_und_filter()
