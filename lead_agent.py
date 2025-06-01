import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from serpapi import GoogleSearch
import time

# Konfiguration
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = "dndg cizt plii mvtm"  # App-spezifisches Passwort für Gmail

SUCHANFRAGEN = [
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

EMAIL_TEXT = '''Sehr geehrte Damen und Herren,

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
'''

def suche_nach_leads():
    leads = []
    for query in SUCHANFRAGEN:
        print(f"🔍 Suche: {query}")
        params = {
            "engine": "google",
            "q": query,
            "location": "Germany",
            "hl": "de",
            "gl": "de",
            "api_key": os.getenv("SERPAPI_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        for result in results.get("organic_results", []):
            title = result.get("title")
            link = result.get("link")
            if title and link:
                leads.append(f"{title}\n{link}")
        time.sleep(1)
    return leads

def sende_email(betreff, inhalte):
    print("📧 Sende E-Mail...")
    message = MIMEMultipart()
    message["From"] = ABSENDER
    message["To"] = EMPFÄNGER
    message["Subject"] = betreff

    body = EMAIL_TEXT + "\n\n---\nNeue potenzielle Leads:\n" + "\n\n".join(inhalte)
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.sendmail(ABSENDER, EMPFÄNGER, message.as_string())
    server.quit()

def main():
    print("\ud83d\udd0d Suche nach Leads läuft...")
    ergebnisse = suche_nach_leads()
    if ergebnisse:
        sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)
    else:
        print("Keine neuen Leads gefunden.")

if __name__ == "__main__":
    main()
