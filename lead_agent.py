import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === KONFIGURATION ===
ABSENDER = "mj.mix888@gmail.com"
PASSWORT = "dein_app_passwort"  # z. B. dndg cizt plii mvtm
EMPFÄNGER = "info@james-fuse.de"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SUCHBEGRIFFE = [
    "Bussmann Sicherung", "Schmelzsicherung", "FNQ-R", "LP-CC", "KTK-R", "FNM-15", "Industriesicherung"
]

# === FUNKTION: TED.europa.eu ===
def scrape_ted():
    text = "📄 Ergebnisse von TED.europa.eu:\n"
    for begriff in SUCHBEGRIFFE:
        url = f"https://ted.europa.eu/TED/search/searchResult.xhtml?searchScope=NOTICES&locale=de&QueryText={begriff}"
        text += f"- {begriff}: {url}\n"
    return text

# === FUNKTION: bund.de ===
def scrape_bund():
    text = "\n📄 Ergebnisse von bund.de:\n"
    for begriff in SUCHBEGRIFFE:
        url = f"https://www.bund.de/DE/Suche/Ausschreibungen/ausschreibungen_node.html?nn=4641482&q={begriff}"
        text += f"- {begriff}: {url}\n"
    return text

# === FUNKTION: eBay Kleinanzeigen Suche ===
def scrape_ebay():
    text = "\n📄 Ergebnisse von eBay Kleinanzeigen:\n"
    for begriff in SUCHBEGRIFFE:
        url = f"https://www.kleinanzeigen.de/s-anzeige/{begriff.replace(' ', '-')}/k0"
        text += f"- {begriff}: {url}\n"
    return text

# === FUNKTION: E-Mail senden ===
def sende_email(betreff, inhalt):
    msg = MIMEMultipart()
    msg['From'] = ABSENDER
    msg['To'] = EMPFÄNGER
    msg['Subject'] = betreff
    msg.attach(MIMEText(inhalt, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.send_message(msg)
    server.quit()

# === MAIN ===
def main():
    print("🚀 Starte kombinierte Lead-Suche...")

    ted_text = scrape_ted()
    bund_text = scrape_bund()
    ebay_text = scrape_ebay()

    full_report = ted_text + bund_text + ebay_text

    print("📧 Sende E-Mail...")
    sende_email("Täglicher Lead-Report: Sicherungen", full_report)
    print("✅ Fertig!")

if __name__ == "__main__":
    main()
