import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "FNQ-R fuse kaufen", "LP-CC fuse gesucht", "KTK Sicherung Anfrage",
    "KTK-R fuse Anfrage", "AJT fuse benötigt", "ATQR fuse Anfrage",
    "ATDR fuse kaufen", "ATM Sicherung gesucht", "ATMR fuse Bedarf",
    "TRM15 fuse Bedarf", "FNM-15 fuse gesucht",
    "Industriesicherung benötigt", "Midget fuse Anfrage",
    "UL zertifizierte Sicherung kaufen", "CSA Sicherung gesucht", "CE fuse Bedarf"
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# === SUCH-FUNKTION (Google) ===
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
                if not any(x in ziel for x in ["bussmann", "rexel", "newark", "mcmaster", "amazon", "ebay", "alibaba", "lieferant", "supplier", "verkauf", "angebot"]):
                    links.append(ziel)
    return links

# === E-MAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Aktuelle Suchergebnisse"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    if not smtp_pass:
        print("❌ Fehler: EMAIL_PASSWORD ist nicht gesetzt oder leer!")
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("mjmix888@gmail.com", smtp_pass)
            server.send_message(msg)
            print("✅ E-Mail erfolgreich gesendet.")
    except Exception as e:
        print(f"❌ Fehler beim Senden der E-Mail: {e}")

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gesamt_ergebnisse = {}
    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {begriff}")
        results = google_suche(begriff)
        print(f"Google: {len(results)} Treffer")
        if results:
            gesamt_ergebnisse[begriff] = list(set(results))
        time.sleep(1)  # Schutz vor zu schneller Anfrage
    return gesamt_ergebnisse

if __name__ == "__main__":
    ergebnisse = suche_und_ausgeben()
    if ergebnisse:
        text = ""
        for begriff, links in ergebnisse.items():
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links) + "\n"
        sende_email(text)
    else:
        sende_email("❌ Heute wurden keine Leads gefunden – Agent aktiv, aber keine Treffer.")
