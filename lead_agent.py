import os
import smtplib
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Umgebungsvariablen
ABSENDER = "mj.mix888@gmail.com"
EMPFÄNGER = "info@james-fuse.de"
PASSWORT = os.getenv("EMAIL_PASSWORD")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Suchbegriffe
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

def finde_leads(suchbegriff):
    params = {
        "engine": "google",
        "q": suchbegriff,
        "location": "Germany",
        "hl": "de",
        "gl": "de",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    firmen = []

    for ergebnis in results.get("organic_results", []):
        title = ergebnis.get("title")
        link = ergebnis.get("link")
        if title and link:
            firmen.append(f"{title} → {link}")

    return firmen

def sende_email(betreff, text):
    nachricht = MIMEMultipart()
    nachricht["From"] = ABSENDER
    nachricht["To"] = EMPFÄNGER
    nachricht["Subject"] = betreff

    body = f"""Sehr geehrte Damen und Herren,

mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann. Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten.

Unsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards. Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen. Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich.

Viele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen. Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen. Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit.

Ich würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen. Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment.

Vielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.

Mit freundlichen Grüßen

Justin James
James Fuse & Beyond GmbH
Georg-Pingler-Straße 15
61462 Königstein im Taunus
Phone: +49 6174 9699645
Email: info@james-fuse.de
Website: www.james-fuse.de

---

Neue potenzielle Leads:
{text}
"""

    nachricht.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(ABSENDER, PASSWORT)
        server.sendmail(ABSENDER, EMPFÄNGER, nachricht.as_string())

def main():
    print("🔍 Suche nach Leads läuft...")
    alle_firmen = []
    for begriff in SUCHBEGRIFFE:
        print(f"🔍 Suche: {begriff}")
        firmen = finde_leads(begriff)
        for eintrag in firmen:
            alle_firmen.append(f"Gefundene Firma bei Suche nach '{begriff}':\n{eintrag}\n")

    if alle_firmen:
        ergebnisse = "\n".join(alle_firmen)
        print("📧 Sende E-Mail...")
        sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)
    else:
        print("❗ Keine neuen Ergebnisse gefunden.")

if __name__ == "__main__":
    main()
