import smtplib
import ssl
from email.message import EmailMessage
import os
from datetime import datetime
import random

# Einstellungen
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = os.getenv("EMAIL_PASSWORD")  # App-Passwort hier hinterlegen als GitHub Secret
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Simulierte Suchbegriffe und Ergebnisse
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

BEISPIEL_LEADS = [
    "https://www.wlw.de/de/firma/formeotec-gmbh-co-kg-1858600",
    "https://www.wlw.de/de/firma/fronius-schweiz-ag-100136",
    "https://www.wlw.de/de/firma/dosen-zentrale-zuechner-gmbh-395576",
    "https://www.wlw.de/de/firma/wurster-druck-verpackung-gmbh-1152358",
    "https://www.wlw.de/de/firma/keller-elektrotechnik-gmbh-1234567",
    "https://www.wlw.de/de/firma/beispiel-firma-gmbh-9999999",
    "https://www.wlw.de/de/firma/stark-elektroanlagen-gmbh-1112223",
    "https://www.wlw.de/de/firma/auto-sicherung-gmbh-4455667",
    "https://www.wlw.de/de/firma/industrie-schutz-gmbh-3338881",
    "https://www.wlw.de/de/firma/fusetec-automation-gmbh-7779990"
]

def generiere_leads(max_anzahl=10):
    zufaellige_leads = random.sample(BEISPIEL_LEADS, k=max_anzahl)
    ergebnisse = []
    for begriff in SUCHBEGRIFFE:
        linkgruppe = random.sample(zufaellige_leads, k=min(3, len(zufaellige_leads)))
        ergebnisse.append(f"\U0001F50D Suche: {begriff}")
        for link in linkgruppe:
            ergebnisse.append(f"➔ {link}")
        ergebnisse.append("")
    return "\n".join(ergebnisse)

def sende_email(betreff, inhalt):
    msg = EmailMessage()
    msg.set_content(inhalt)
    msg["Subject"] = betreff
    msg["From"] = ABSENDER
    msg["To"] = EMPFÄNGER

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(ABSENDER, PASSWORT)
        server.send_message(msg)

def main():
    print("🔍 Suche nach Leads läuft...")
    ergebnisse = generiere_leads()
    print("📧 Sende E-Mail...")
    sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)

if __name__ == "__main__":
    main()
