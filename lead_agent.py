import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib

# === KONFIGURATION ===
SUCHBEGRIFFE = ["KTK fuse", "KTK-R Sicherung", "LP-CC fuse", "FNQ-R fuse", "AJT fuse"]
ZIEL_SEITEN = [
    "https://www.google.com/search?q=",
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# === FUNKTIONEN ===
def google_suche(begriff):
    url = ZIEL_SEITEN[0] + requests.utils.quote(begriff)
    response = requests.get(url, headers=USER_AGENT)
    if response.status_code != 200:
        print("Fehler bei Anfrage:", response.status_code)
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    ergebnisse = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "url?q=" in href:
            match = re.search(r"url\?q=(https?://[^&]+)", href)
            if match:
                ergebnisse.append(match.group(1))
    return ergebnisse

def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "info@james-fuse.de"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Neue Lead-Ergebnisse gefunden"
    msg.set_content(inhalt)

    with smtplib.SMTP("smtp.ionos.de", 587) as server:
        server.starttls()
        server.login("info@james-fuse.de", "DEIN-APP-PASSWORT")
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gefundene_links = {}
    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {begriff}")
        treffer = google_suche(begriff)
        if treffer:
            gefundene_links[begriff] = treffer
            for link in treffer:
                print(f"➡️ {link}")
        else:
            print("Keine Ergebnisse gefunden.")
        time.sleep(2)
    return gefundene_links

if __name__ == "__main__":
    ergebnisse = suche_und_ausgeben()
    if ergebnisse:
        text = ""
        for begriff, links in ergebnisse.items():
            text += f"\n🔍 {begriff}\n" + "\n".join(f"➡️ {link}" for link in links) + "\n"
        sende_email(text)
