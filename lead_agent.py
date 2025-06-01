import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from datetime import datetime

ABSENDER = "mjmix888@gmail.com"
PASSWORT = "dndg cizt plii mvtm"
EMPFÄNGER = "info@james-fuse.de"

SUCHBEGRIFFE = [
    "Sicherung kaufen site:wlw.de",
    "Class CC Sicherung gesucht site:ebay.de",
    "Industriesicherung Bedarf site:kleinanzeigen.de",
    "UL Sicherung gesucht site:technikboerse.com",
    "Sicherungsbedarf site:industrystock.de",
    "Sicherung gesucht site:mikrocontroller.net",
    "Sicherung site:elektrotechnik-forum.de",
    "Sicherung site:bund.de",
    "Sicherung site:ted.europa.eu",
    "Sicherung site:northdata.de"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}


def finde_leads():
    leads = []
    for begriff in SUCHBEGRIFFE:
        try:
            response = requests.get(f"https://www.google.com/search?q={begriff}", headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")
            for g in soup.find_all('div', class_='tF2Cxc'):
                titel = g.find('h3').text if g.find('h3') else "Kein Titel"
                link = g.find('a')['href'] if g.find('a') else "Kein Link"
                beschreibung = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else "Keine Beschreibung"
                leads.append({"titel": titel, "link": link, "beschreibung": beschreibung})
        except Exception as e:
            leads.append({"titel": f"Fehler bei {begriff}", "link": "", "beschreibung": str(e)})
    return leads


def sende_email(leads):
    msg = MIMEMultipart()
    msg['From'] = ABSENDER
    msg['To'] = EMPFÄNGER
    msg['Subject'] = f"Neue Leads (Stand: {datetime.now().strftime('%d.%m.%Y %H:%M')})"

    html = "<h3>Neue potenzielle Leads:</h3><ul>"
    for eintrag in leads:
        html += f"<li><strong>{eintrag['titel']}</strong><br><a href='{eintrag['link']}'>{eintrag['link']}</a><br>{eintrag['beschreibung']}</li><br>"
    html += "</ul>"

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(ABSENDER, PASSWORT)
        server.send_message(msg)


def main():
    print("🔍 Suche nach echten Leads läuft...")
    leads = finde_leads()
    print("📧 Sende E-Mail...")
    sende_email(leads)


if __name__ == "__main__":
    main()
