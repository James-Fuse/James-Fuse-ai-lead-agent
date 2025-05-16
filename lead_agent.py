import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    # Bussmann-Typen
    "LPJ fuse anfrage", "LP-CC fuse supplier needed", "FNQ-R fuse gesucht", "KTK fuse lieferant",
    "KTK-R fuse rfq", "FNM-15 Sicherung anfrage", "FNQ-R Sicherung Bedarf", "LP-CC fuse beschaffung",
    "Bussmann Sicherungen gesucht", "Eaton class J fuse supplier",

    # Mersen-Typen
    "ATQR fuse request", "ATDR Sicherungen Bedarf", "AJT Sicherung Lieferant", "TRM15 fuse anfrage",
    "ATM fuse rfq", "ATMR Sicherung gesucht",

    # Allgemeine Bedarfsausdrücke
    "Sicherungslieferant gesucht", "Lieferant für elektrische Sicherungen",
    "Anfrage für Industriesicherungen", "Steuerungstechnik Sicherung Bedarf",
    "Sicherungen für Schaltschrank kaufen", "Sicherungen Maschinenbauer gesucht",
    "Angebot Sicherungen FNQ-R", "Industriesicherungen Beschaffung",

    # Zertifikatsbezogene Suchen
    "UL fuse purchase request", "CSA Sicherungen Bedarf", "CE zertifizierte Sicherungen anfrage",
    "UL CSA CE fuse lieferant", "600V UL listed Sicherungen gesucht",

    # Ausschreibungsspezifisch / ENGLISCH
    "fuse procurement tender", "supplier needed for control cabinet fuse",
    "we are looking for class cc fuses", "time delay fuse sourcing",
    "need FNQ-R fuse for production", "Bussmann fuse sourcing inquiry",
    "rfq industrial fuse", "looking for UL-certified fuse supplier",
    "rfq time delay class cc fuse", "need supplier for fuse with CE marking"
]

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BLOCKLIST_DOMAINS = ["amazon.com", "eaton.com", "rexel", "digikey", "newark", "mcmaster", "james-fuse"]
MATCH_KEYWORDS = ["anfrage", "gesucht", "bedarf", "request", "supplier", "lieferant", "rfq", "looking for"]

# === SUCH-FUNKTIONEN ===
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
                ziel = match.group(1)
                if not any(domain in ziel for domain in BLOCKLIST_DOMAINS):
                    links.append(ziel)
    return links

# === E-MAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Firmen mit Sicherungsbedarf"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gesamt_ergebnisse = {}
    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {begriff}")
        results = google_suche(begriff)
        gefiltert = []
        for link in results:
            try:
                r = requests.get(link, headers=USER_AGENT, timeout=5)
                if any(keyword in r.text.lower() for keyword in MATCH_KEYWORDS):
                    gefiltert.append(link)
            except Exception:
                continue
        if gefiltert:
            gesamt_ergebnisse[begriff] = gefiltert
        time.sleep(1)
    return gesamt_ergebnisse

if __name__ == "__main__":
    ergebnisse = suche_und_ausgeben()
    if ergebnisse:
        text = ""
        for begriff, links in ergebnisse.items():
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links) + "\n"
        sende_email(text)
    else:
        sende_email("❌ Heute wurden keine interessierten Firmen gefunden – Agent aktiv, aber keine echten Leads.")
