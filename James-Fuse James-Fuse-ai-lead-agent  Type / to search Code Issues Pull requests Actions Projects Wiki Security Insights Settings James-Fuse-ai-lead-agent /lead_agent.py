# AI Lead Agent: Suche nach Unternehmen, die nach bestimmten Sicherungen suchen

import requests
from bs4 import BeautifulSoup
import re
import time

# === KONFIGURATION ===
SUCHBEGRIFFE = ["KTK fuse", "KTK-R Sicherung", "LP-CC fuse", "FNQ-R fuse", "AJT fuse"]
ZIEL_SEITEN = [
    "https://www.google.com/search?q=",
    # weitere Suchmaschinen oder Branchenportale können ergänzt werden
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
            match = re.search(r"url\?q=(https?://[^"]+)&", href)
            if match:
                ergebnisse.append(match.group(1))
    return ergebnisse

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
        time.sleep(2)  # Vermeidet zu viele Anfragen auf einmal
    return gefundene_links

# Starte die Suche
if __name__ == "__main__":
    suche_und_ausgeben()
