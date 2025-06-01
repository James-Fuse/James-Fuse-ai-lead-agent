import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from serpapi import GoogleSearch

# Konfiguration
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dndg cizt plii mvtm"  # App-spezifisches Passwort von Google

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

EMAIL_TEXT = """
Sehr geehrte Damen und Herren,

mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann. Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten.

Unsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards. Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen. Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich.

Viele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen. Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen. Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit.

Ich würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen. Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment.

Vielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.

Mit freundlichen Grüßen,

Justin James
Managing Director | James Fuse & Beyond GmbH
Georg-Pingler-Straße 15
61462 Königstein im Taunus, Germany
Phone: +49 6174 9699645
Email: info@james-fuse.de
Website: www.james-fuse.de
"""

def suche_leads():
    print("\U0001F50D Suche nach Leads läuft...")
    ergebnisse = []
    for begriff in SUCHBEGRIFFE:
        print(f"🔍 Suche: {begriff}")
        params = {
            "engine": "google",
            "q": begriff,
            "location": "Germany",
            "hl": "de",
            "gl": "de",
            "api_key": os.getenv("SERPAPI_API_KEY")
        }
        suche = GoogleSearch(params)
        result = suche.get_dict()
        if "organic_results" in result:
            for eintrag in result["organic_results"][:3]:
                ergebnisse.append(f"Gefundene Firma bei Suche nach '{begriff}': {eintrag.get('title')} - {eintrag.get('link')}")
    return ergebnisse

def sende_email(betreff, inhalt_zeilen):
    print("\U0001F4E7 Sende E-Mail...")
    nachricht = MIMEMultipart()
    nachricht["From"] = ABSENDER
    nachricht["To"] = EMPFÄNGER
    nachricht["Subject"] = betreff

    text = EMAIL_TEXT + "\n---\nNeue potenzielle Leads:\n" + "\n".join(inhalt_zeilen)
    nachricht.attach(MIMEText(text, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.sendmail(ABSENDER, EMPFÄNGER, nachricht.as_string())
    server.quit()

def main():
    ergebnisse = suche_leads()
    sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)

if __name__ == "__main__":
    main()
