import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib
from email.message import EmailMessage
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "Sicherung defekt Austausch",
    "Class CC Sicherung gesucht",
    "FNQ-R benötigt",
    "LPJ Angebot",
    "Sicherungslieferant gesucht",
    "Sicherung kaufen",
    "Eaton Bussmann gesucht",
    "Maschinenbauer Sicherungen",
    "Schaltanlagen Ersatzteile",
    "Bussmann fuse inquiry",
    "Anfrage Sicherung FNQ-R",
    "Industriesicherung Angebot",
    "Lieferant elektrische Sicherungen",
    "KTK-R Lagerbestand",
    "UL Sicherung Ersatz",
    "Sicherung gesucht Steuerung",
    "Automatiksicherung Anbieter",
    "CSA Sicherung bestellen",
    "Class J fuse Germany",
    "TRM15 Anfrage",
    "ATQR gebraucht",
    "ATDR sourcing",
    "AJT fuse sourcing",
    "Elektriker Sicherung Bedarf",
    "Industriebedarf Sicherungen"
]

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# === EINFACHE GOOGLE-SUCHE ===
def google_suche(begriff):
    url = f"https://www.google.com/search?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "url?q=" in href and not any(x in href for x in ["amazon", "ebay", "alibaba", "youtube", "pinterest"]):
            match = re.search(r"url\\?q=(https?://[^&]+)", href)
            if match:
                clean_url = match.group(1)
                if not any(x in clean_url.lower() for x in ["shop", "verkauf", "lieferant", "supplier", "dealer", "grosshandel"]):
                    links.append(clean_url)
    return links[:10]

# === WLW-SUCHE (DE) ===
def wlw_suche(begriff):
    url = f"https://www.wlw.de/de/suche?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/firma/" in href:
            full_url = "https://www.wlw.de" + href
            if not any(x in full_url for x in ["anbieter", "lieferant"]):
                links.append(full_url)
    return list(set(links))[:10]

# === EMAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Agent Report: potenzielle Interessenten"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    if not smtp_pass:
        print("❌ Kein EMAIL_PASSWORD gefunden.")
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("mjmix888@gmail.com", smtp_pass)
            server.send_message(msg)
        print("✅ E-Mail gesendet.")
    except Exception as e:
        print("❌ Fehler beim Senden der E-Mail:", e)

# === HAUPTFUNKTION ===
def suche_und_ausgeben():
    gesamt_ergebnisse = {}
    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {begriff}")
        results = []

        google_links = google_suche(begriff)
        print(f"Google: {len(google_links)} Treffer")
        results += google_links

        wlw_links = wlw_suche(begriff)
        print(f"WLW: {len(wlw_links)} Treffer")
        results += wlw_links

        if results:
            gefiltert = list(set(results))
            gesamt_ergebnisse[begriff] = gefiltert
        time.sleep(2)

    return gesamt_ergebnisse

# === START ===
if __name__ == "__main__":
    ergebnisse = suche_und_ausgeben()
    if ergebnisse:
        text = ""
        for begriff, links in ergebnisse.items():
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links) + "\n"
        sende_email(text)
    else:
        sende_email("❌ Heute wurden keine potenziellen Interessenten gefunden – Agent ist aktiv, aber ohne Treffer.")
