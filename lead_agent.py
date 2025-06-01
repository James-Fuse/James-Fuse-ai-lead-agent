# lead_agent.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dndg cizt plii mvtm"  # App-spezifisches Passwort von Gmail

# Placeholder-Scraper (Dummy-Ergebnisse, du kannst später echte Scraper einbauen)
def finde_leads_wlw():
    return ["Firma A bei wlw.de", "Firma B bei wlw.de"]

def finde_leads_ebay():
    return ["Inserat: Sicherung gesucht auf ebay"]

def finde_leads_kleinanzeigen():
    return ["Gesuch: UL Sicherung auf Kleinanzeigen"]

def finde_leads_industrystock():
    return ["Firma C bei industrystock"]

def finde_leads_technikboerse():
    return ["Anfrage auf technikboerse"]

def finde_leads_mikrocontroller():
    return ["Post: Suche Sicherung auf mikrocontroller.net"]

def finde_leads_elektronik_forum():
    return ["Beitrag auf elektrotechnik-forum.de"]

def finde_leads_opencorporates():
    return ["Neue Firma: Elektro XY GmbH"]

def finde_leads_northdata():
    return ["Neueintragung: Automatisierung ABC"]

def finde_leads_bund():
    return ["Ausschreibung Sicherungen auf bund.de"]

def finde_leads_ted():
    return ["EU-Tender: Sicherungen"]

def sende_email(betreff, text):
    nachricht = MIMEMultipart()
    nachricht['From'] = ABSENDER
    nachricht['To'] = EMPFÄNGER
    nachricht['Subject'] = betreff
    nachricht.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.sendmail(ABSENDER, EMPFÄNGER, nachricht.as_string())
    server.quit()

def main():
    print("🔍 Suche nach Leads läuft...")
    leads = []
    leads += finde_leads_wlw()
    leads += finde_leads_ebay()
    leads += finde_leads_kleinanzeigen()
    leads += finde_leads_industrystock()
    leads += finde_leads_technikboerse()
    leads += finde_leads_mikrocontroller()
    leads += finde_leads_elektronik_forum()
    leads += finde_leads_opencorporates()
    leads += finde_leads_northdata()
    leads += finde_leads_bund()
    leads += finde_leads_ted()

    text = "Sehr geehrte Damen und Herren,\n\n" + \
           "mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. " \
           "Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann..." \
           "\n\n---\n\nNeue potenzielle Leads:\n" + "\n".join(leads)

    print("📧 Sende E-Mail...")
    sende_email("Neue Leads: Firmen mit Sicherungsbedarf", text)

if __name__ == "__main__":
    main()
