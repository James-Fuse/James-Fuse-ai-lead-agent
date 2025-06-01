import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

ABSENDER = "mj.mix888@gmail.com"
EMPFAENGER = "info@james-fuse.de"
PASSWORT = os.getenv("EMAIL_PASSWORD")

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

def finde_fake_leads(suchbegriff):
    print(f"🔍 Suche: {suchbegriff}")
    return [f"https://example.com/{suchbegriff.replace(' ', '_')}"]

def sende_email(betreff, inhalt_links):
    print("📧 Sende E-Mail...")

    nachricht = MIMEMultipart()
    nachricht["From"] = ABSENDER
    nachricht["To"] = EMPFAENGER
    nachricht["Subject"] = betreff

    text = "Hier sind neue potenzielle Kunden:\n\n"
    for kategorie, links in inhalt_links.items():
        text += f"🔍 {kategorie}\n"
        for link in links:
            text += f"➡️ {link}\n"
        text += "\n"

    nachricht.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(ABSENDER, PASSWORT)
        server.sendmail(ABSENDER, EMPFAENGER, nachricht.as_string())
        server.quit()
        print("✅ E-Mail erfolgreich gesendet.")

def main():
    print("🔍 Suche nach Leads läuft...")
    ergebnisse = {}
    for begriff in SUCHBEGRIFFE:
        ergebnisse[begriff] = finde_fake_leads(begriff)

    sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)

if __name__ == "__main__":
    main()
