import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os
import json
from datetime import datetime

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "Sicherung gesucht", "Sicherung kaufen", "Class CC Sicherung gesucht", "Industriesicherung Bedarf",
    "Lieferant elektrische Sicherungen", "UL Sicherung Ersatz", "Steuerung Sicherung",
    "Schaltanlagen Ersatzteile", "Elektriker Sicherung Bedarf", "Industriebedarf Sicherungen",
    "CSA Sicherung bestellen", "Maschinenbauer Sicherungen", "Sicherungslieferant gesucht",
    "Class J fuse Germany"
]

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
LEAD_LOG_FILE = "sent_leads_log.json"

# === LOGIK FÜR EINMALIGE LEADS ===
def lade_bekannte_links():
    if os.path.exists(LEAD_LOG_FILE):
        with open(LEAD_LOG_FILE, "r") as f:
            return set(json.load(f))
    return set()

def speichere_links(links):
    bekannte = lade_bekannte_links()
    bekannte.update(links)
    with open(LEAD_LOG_FILE, "w") as f:
        json.dump(list(bekannte), f)

# === SUCH-FUNKTIONEN ===
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
    msg["Subject"] = "🔍 Neue potenzielle Kunden für Sicherungen (max. 10 Leads)"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_filter():
    bekannte_links = lade_bekannte_links()
    neue_leads = {}
    alle_neuen_links = set()

    for begriff in SUCHBEGRIFFE:
        print(f"🔍 Suche nach: {begriff}")
        results = wlw_suche(begriff)
        neue = [link for link in results if link not in bekannte_links and "/produkte/" not in link.lower() and not re.search(r"lieferant|anbieter|shop|verkauf", link.lower())]
        if neue:
            neue_leads[begriff] = neue
            alle_neuen_links.update(neue)
        time.sleep(1)

    return neue_leads, list(alle_neuen_links)

if __name__ == "__main__":
    leads, neue_links = suche_und_filter()

    if leads:
        text = ""
        gesendet = 0
        for begriff, links in leads.items():
            ungefiltert = [l for l in links if gesendet < 10]
            if not ungefiltert:
                continue
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in ungefiltert) + "\n"
            gesendet += len(ungefiltert)
            if gesendet >= 10:
                break
        speichere_links(neue_links[:10])
        sende_email(text)
    else:
        sende_email("❌ Keine neuen Leads mit Bedarf an Sicherungen gefunden.")
