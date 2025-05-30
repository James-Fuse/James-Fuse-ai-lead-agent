import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔍 Deine Suchbegriffe
SUCHBEGRIFFE = [
    "Sicherung kaufen",
    "Class CC Sicherung gesucht",
    "Sicherung gesucht Steuerung",
    "Industriesicherung Bedarf",
    "Maschinenbauer Sicherungen",
    "Schaltanlagen Ersatzteile",
    "Sicherungslieferant gesucht",
    "Elektriker Sicherung Bedarf",
    "CSA Sicherung bestellen",
    "UL Sicherung Ersatz",
    "Lieferant elektrische Sicherungen",
    "Sicherung defekt Austausch"
]

# ✅ Bekannte Links speichern
BEKANNTE_LINKS_DATEI = "bekannte_links.txt"

# 📩 E-Mail-Konfiguration
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = os.getenv("EMAIL_PASSWORD")  # Das App-spezifische Passwort von Gmail

def lade_bekannte_links():
    if not os.path.exists(BEKANNTE_LINKS_DATEI):
        return set()
    with open(BEKANNTE_LINKS_DATEI, "r") as f:
        return set(line.strip() for line in f.readlines())

def speichere_links(links):
    with open(BEKANNTE_LINKS_DATEI, "a") as f:
        for link in links:
            f.write(link + "\n")

def mock_suche(begriff):
    # ✨ Hier ist nur ein Mock – ersetze das später mit echter Websuche
    base_url = "https://www.wlw.de/de/firma/"
    return [f"{base_url}{begriff.replace(' ', '-').lower()}-firma{i}" for i in range(1, 4)]

def sende_email(betreff, inhalt):
    print("📧 Sende E-Mail...")

    msg = MIMEMultipart()
    msg["From"] = ABSENDER
    msg["To"] = EMPFÄNGER
    msg["Subject"] = betreff
    msg.attach(MIMEText(inhalt, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(ABSENDER, PASSWORT)
        server.sendmail(ABSENDER, EMPFÄNGER, msg.as_string())

def main():
    bekannte_links = lade_bekannte_links()
    neue_links = set()
    ergebnisse = ""

    for begriff in SUCHBEGRIFFE:
        print(f"🔍 Suche: {begriff}")
        gefundene = mock_suche(begriff)
        for link in gefundene:
            if link not in bekannte_links:
                neue_links.add(link)
                ergebnisse += f"{begriff}\n➡️ {link}\n\n"
            if len(neue_links) >= 10:
                break
        if len(neue_links) >= 10:
            break

    if neue_links:
        sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)
        speichere_links(neue_links)
        print("✅ E-Mail versendet mit neuen Leads.")
    else:
        sende_email("Lead-Agent hat keine neuen Firmen gefunden", "Der Lead-Agent hat bei der aktuellen Suche keine neuen Firmen gefunden.")
        print("ℹ️ Keine neuen Leads gefunden.")

if __name__ == "__main__":
    main()
