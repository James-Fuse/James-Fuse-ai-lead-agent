import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Suchbegriffe
suchbegriffe = [
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

# Beispielergebnisse (diese sollten vom Such-Agenten ersetzt werden)
ergebnisse = "".join([f"\n🔍 {begriff}\n➡️ https://beispiel-url.de/{begriff.replace(' ', '-')}" for begriff in suchbegriffe])

# E-Mail-Konfiguration
ABSENDER = "mj.mix888@gmail.com"  # Dein Gmail-Konto
EMPFÄNGER = "info@james-fuse.de"   # Wohin die Leads sollen
BETREFF = "Neue Leads: Firmen mit Sicherungsbedarf"
PASSWORT = os.getenv("EMAIL_PASSWORD")  # App-spezifisches Passwort in GitHub Secrets speichern

# E-Mail-Nachricht erstellen
def sende_email(betreff, text):
    nachricht = MIMEMultipart()
    nachricht["From"] = ABSENDER
    nachricht["To"] = EMPFÄNGER
    nachricht["Subject"] = betreff

    body = f"""
Hallo Justin,

hier sind die neuen Suchergebnisse von {datetime.now().strftime('%d.%m.%Y %H:%M')}:
{text}

Viele Grüße,
Dein Lead-Agent
"""
    nachricht.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(ABSENDER, PASSWORT)
        server.sendmail(ABSENDER, EMPFÃNGER, nachricht.as_string())

# Hauptfunktion
def main():
    print("🔍 Suche nach Leads läuft...")
    print("📧 Sende E-Mail...")
    sende_email(BETREFF, ergebnisse)

if __name__ == "__main__":
    main()
