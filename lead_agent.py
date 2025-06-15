import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === KONFIGURATION ===
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dndg cizt plii mvtm"  # App-Passwort von Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === FUNKTIONEN ===
def finde_neugruendungen():
    suchbegriffe = [
        "neu gegründete GmbH Elektrotechnik site:northdata.de",
        "neueintragung Automatisierung site:handelsregister.de",
        "Gründung Schaltschrankbau site:opencorporates.com",
        "Firmengründung SPS Steuerung site:unternehmensregister.de"
    ]
    gefundene = []

    for begriff in suchbegriffe:
        print("🔍 Suche:", begriff)
        try:
            response = requests.get(f"https://www.google.com/search?q={begriff}", headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            treffer = soup.select("div.g h3")
            for t in treffer:
                titel = t.get_text()
                if titel not in gefundene:
                    gefundene.append(titel)
        except Exception as e:
            gefundene.append(f"Fehler bei Suche nach '{begriff}': {e}")
    return gefundene

def sende_email(betreff, inhalt):
    print("📧 Sende E-Mail...")
    msg = MIMEMultipart()
    msg["From"] = ABSENDER
    msg["To"] = EMPFÄNGER
    msg["Subject"] = betreff

    msg.attach(MIMEText(inhalt, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.send_message(msg)
    server.quit()

# === HAUPTFUNKTION ===
def main():
    print("🚀 Starte Suche nach Neugründungen...")
    daten = finde_neugruendungen()

    if not daten:
        text = "Leider wurden heute keine neuen Einträge gefunden."
    else:
        text = "Hier sind die gefundenen Neugründungen im Bereich Elektrotechnik und Automatisierung:\n\n"
        for eintrag in daten:
            text += f"– {eintrag}\n"

    sende_email("Neueintragungen: Elektrotechnik & Automatisierung", text)

# === AUSFÜHRUNG ===
if __name__ == "__main__":
    main()
