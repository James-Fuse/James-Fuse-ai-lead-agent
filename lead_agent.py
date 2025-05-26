import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "sicherung kaufen", "sicherung gesucht", "steuerung sicherung", "industriesicherung bedarf",
    "elektriker sicherung bedarf", "maschinenbauer sicherungen", "schaltanlagen ersatzteile",
    "sicherungslieferant gesucht", "ul sicherung ersatz", "csa sicherung bestellen",
    "lieferant elektrische sicherungen", "class cc sicherung gesucht", "class j fuse germany"
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Nur Leads mit diesen Begriffen melden
LEAD_FILTER = [
    "sicherung kaufen", "sicherung gesucht", "steuerung sicherung", "industriesicherung bedarf",
    "elektriker sicherung bedarf", "maschinenbauer sicherungen", "schaltanlagen ersatzteile",
    "sicherungslieferant gesucht", "ul sicherung ersatz", "csa sicherung bestellen",
    "lieferant elektrische sicherungen", "class cc sicherung gesucht", "class j fuse germany"
]

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
    msg["Subject"] = "Lead-Report: Neue potenzielle Kunden"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gefundene_leads = {}
    for keyword in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {keyword}")
        links = wlw_suche(keyword)
        print(f"WLW: {len(links)} Treffer")

        if links and any(filterwort in keyword.lower() for filterwort in LEAD_FILTER):
            gefundene_leads[keyword] = list(set(links))

        time.sleep(1)  # Schonfrist

    return gefundene_leads

if __name__ == "__main__":
    ergebnisse = suche_und_ausgeben()
    if ergebnisse:
        text = ""
        for begriff, links in ergebnisse.items():
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links) + "\n"
        sende_email(text)
    else:
        sende_email("❌ Keine passenden Leads gefunden – Agent aktiv, aber keine konkreten Interessenten entdeckt.")
