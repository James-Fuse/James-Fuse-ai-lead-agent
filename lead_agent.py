import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    "LPJ fuse", "LP-CC fuse", "FNQ-R fuse", "KTK fuse", "KTK-R fuse",
    "AJT fuse", "ATQR fuse", "ATDR fuse", "ATM fuse", "ATMR fuse",
    "TRM15 fuse", "FNM-15 fuse"
]
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

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
                links.append(match.group(1))
    return links

def bing_suche(begriff):
    url = f"https://www.bing.com/search?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for li in soup.find_all("li", class_="b_algo"):
        a = li.find("a")
        if a and a.get("href"):
            links.append(a["href"])
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

# === E-MAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "justin_wehrheim@yahoo.de"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Aktuelle Suchergebnisse"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.mail.yahoo.com", 587) as server:
        server.starttls()
        server.login("justin_wehrheim@yahoo.de", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gesamt_ergebnisse = {}
    for begriff in SUCHBEGRIFFE:
        print(f"\n🔍 Suche nach: {begriff}")
        results = []

        google = google_suche(begriff)
        print(f"Google: {len(google)} Treffer")
        results += google

        bing = bing_suche(begriff)
        print(f"Bing: {len(bing)} Treffer")
        results += bing

        wlw = wlw_suche(begriff)
        print(f"WLW: {len(wlw)} Treffer")
        results += wlw

        if results:
            gesamt_ergebnisse[begriff] = list(set(results))

        time.sleep(1)  # Schonfrist für die Server ;)

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
