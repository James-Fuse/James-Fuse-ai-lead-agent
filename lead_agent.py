import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === KONFIGURATION ===
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dein_app_passwort_hier"  # App-Passwort von Gmail (z. B. dndg cizt plii mvtm)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === SUCHBEGRIFFE ===
KEYWORDS = [
    "neu gegründete GmbH Elektrotechnik site:northdata.de",
    "neueintragung Automatisierung site:handelsregister.de",
    "Gründung Schaltschrankbau site:opencorporates.com",
    "Firmengründung SPS Steuerung site:unternehmensregister.de"
]

# === FUNKTIONEN ===
def finde_neue_firmen():
    gefundene_firmen = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for begriff in KEYWORDS:
        print(f"🔍 Suche: {begriff}")
        url = f"https://www.google.com/search?q={begriff}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for result in soup.select("div.g"):
            link = result.find("a")
            titel = result.find("h3")
            if link and titel:
                gefundene_firmen.append(f"{titel.text} — {link['href']}")

    return gefundene_firmen

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

def main():
    print("🚀 Starte Suche nach Neugründungen...")
    firmen = finde_neue_firmen()
    if not firmen:
        text = "Heute wurden keine neuen relevanten Gründungen gefunden."
    else:
        text = "Neue potenzielle Firmen im Bereich Elektrotechnik/Automatisierung:\n\n"
        for eintrag in firmen:
            text += f"- {eintrag}\n"

    sende_email("Neueintragungen: Elektrotechnik & Automatisierung", text)

if __name__ == "__main__":
    main()
