import requests
from bs4 import BeautifulSoup
import re
import time
from email.message import EmailMessage
import smtplib
import os

# === KONFIGURATION ===
SUCHBEGRIFFE = [
    # Suchintention: Kaufinteresse / Bedarf
    "FNQ-R-1-1/2 kaufen", "FNQ-R-2-1/2 gesucht", "FNQ-R-4 Bedarf", "LP-CC-5 Anfrage",
    "FNM-15 benötigt", "Industriesicherung Anfrage", "Class CC Sicherung gesucht",
    "UL Sicherung bestellen", "Bussmann Sicherung gesucht", "Sicherung für Schaltschrank kaufen",
    "KTK-R benötigt", "KTK Sicherung kaufen", "Midget Fuse gesucht", "Ersatz für FNQ-R-1-1/2",
    "Sicherung für Steuerung benötigt", "Sicherung Maschinenbau kaufen",
    "Zeitverzögerte Sicherung gesucht", "Sicherung Steuerungstechnik Bedarf",
    "Angebot FNQ-R Sicherungen", "Bezugsquelle Bussmann Sicherungen",
    "Suche Sicherung FNQ-R", "Suche Class CC Sicherung", "FNQ-R Preis gesucht",
    "Bussmann FNQ-R Lieferant gesucht", "Suche FNM-15 mit CE", "UL/CSA Sicherung Anfrage",
    "Wer liefert FNQ-R", "Eaton Sicherung dringend gesucht", "Sicherung kaufen Industriebedarf",
    "Sicherungsbedarf Schaltschrank", "Einkauf FNQ-R gesucht", "FNQ-R Bedarf kurzfristig",
    "Lieferung Sicherung dringend", "Sicherungen gesucht für Steuerung",
    "FNQ-R Angebot gewünscht", "Anfrage Industrie-Sicherungen", "Einkäufer sucht Sicherungen",
    "Nachfrage FNQ-R Fuse", "Bezugsquelle LP-CC-5 Sicherung"
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
        if href and "url?q=" in href and not any(block in href for block in ["amazon", "ebay", "rexel", "mcmaster", "newark", "eaton", "wlw.de/firma", "facebook", "youtube"]):
            match = re.search(r"url\?q=(https?://[^&]+)", href)
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
            href = a["href"]
            if not any(block in href for block in ["amazon", "ebay", "rexel", "mcmaster", "newark", "eaton", "wlw.de/firma", "facebook", "youtube"]):
                links.append(href)
    return links

def wlw_suche(begriff):
    url = f"https://www.wlw.de/de/suche?q={requests.utils.quote(begriff)}"
    response = requests.get(url, headers=USER_AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/firma/" in href and not "james-fuse" in href:
            links.append("https://www.wlw.de" + href)
    return links

# === E-MAIL-VERSAND ===
def sende_email(inhalt):
    msg = EmailMessage()
    msg["From"] = "mjmix888@gmail.com"
    msg["To"] = "info@james-fuse.de"
    msg["Subject"] = "Lead-Report: Aktuelle Interessenten"
    msg.set_content(inhalt)

    smtp_pass = os.environ.get("EMAIL_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mjmix888@gmail.com", smtp_pass)
        server.send_message(msg)

# === HAUPTAUSFÜHRUNG ===
def suche_und_ausgeben():
    gesamt_er_
