import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random

# E-Mail Konfiguration
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dndgciztpliimvtm"  # App-spezifisches Passwort von Google
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Lead-Suchbegriffe
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

def suche_nach_leads():
    print("\U0001F50D Suche nach Leads läuft...")
    ergebnisse = []
    for begriff in suchbegriffe:
        print(f"🔍 Suche: {begriff}")
        # Simuliertes Ergebnis
        ergebnisse.append(f"Gefundene Firma bei Suche nach '{begriff}'")
        time.sleep(random.uniform(0.5, 1.2))
    return ergebnisse

def sende_email(betreff, ergebnisse):
    print("\U0001F4E7 Sende E-Mail...")
    nachricht = MIMEMultipart()
    nachricht['From'] = ABSENDER
    nachricht['To'] = EMPFÄNGER
    nachricht['Subject'] = betreff

    text = "Sehr geehrte Damen und Herren,\n"
    text += "\nmein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus."
    text += " Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann."
    text += " Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten."
    text += "\n\nUnsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards."
    text += " Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen."
    text += " Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich."
    text += "\n\nViele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen."
    text += " Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen."
    text += " Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit."
    text += "\n\nIch würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen."
    text += " Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment."
    text += "\n\nVielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.\n\nMit freundlichen Grüßen,\n\n"
    text += "Justin James\nManaging Director | James Fuse & Beyond GmbH\nGeorg-Pingler-Straße 15\n61462 Königstein im Taunus, Germany\nPhone: +49 6174 9699645\nEmail: info@james-fuse.de\nWebsite: www.james-fuse.de"
    text += "\n\n---\nNeue potenzielle Leads:\n" + "\n".join(ergebnisse)

    nachricht.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.sendmail(ABSENDER, EMPFÄNGER, nachricht.as_string())
    server.quit()

def main():
    ergebnisse = suche_nach_leads()
    sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)

if __name__ == "__main__":
    main()
