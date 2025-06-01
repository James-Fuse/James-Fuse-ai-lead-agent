import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from serpapi import GoogleSearch

# SMTP Konfiguration
ABSENDER = "mj.mix888@gmail.com"
EMPFANGER = "info@james-fuse.de"
PASSWORT = "dndg cizt plii mvtm"  # App-spezifisches Passwort von Google

# Suchbegriffe
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

# SerpAPI Key (in Umgebungsvariable setzen oder direkt eintragen)
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or "DEIN_SERPAPI_KEY"

def suche_firmen(suchbegriff):
    print(f"🔍 Suche: {suchbegriff}")
    params = {
        "q": suchbegriff,
        "location": "Germany",
        "hl": "de",
        "gl": "de",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    firmen_urls = []
    for ergebnis in results.get("organic_results", []):
        titel = ergebnis.get("title", "")
        link = ergebnis.get("link", "")
        if link and "google.com" not in link:
            firmen_urls.append(f"{titel}\n{link}")
    return firmen_urls

def sende_email(betreff, inhalt_liste):
    print("\ud83d\udce7 Sende E-Mail...")
    body_text = "Sehr geehrte Damen und Herren,\n\n"
    body_text += "mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann. Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten.\n\n"
    body_text += "Unsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards. Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen. Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich.\n\n"
    body_text += "Viele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen. Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen. Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit.\n\n"
    body_text += "Ich würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen. Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment.\n\n"
    body_text += "Vielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.\n\nMit freundlichen Grüßen,\n\nJustin James\nManaging Director | James Fuse & Beyond GmbH\nGeorg-Pingler-Straße 15\n61462 Königstein im Taunus, Germany\nPhone: +49 6174 9699645\nEmail: info@james-fuse.de\nWebsite: www.james-fuse.de\n\n"
    body_text += "---\nNeue potenzielle Leads:\n"
    for eintrag in inhalt_liste:
        body_text += f"{eintrag}\n\n"

    nachricht = MIMEMultipart()
    nachricht["From"] = ABSENDER
    nachricht["To"] = EMPFANGER
    nachricht["Subject"] = betreff
    nachricht.attach(MIMEText(body_text, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(ABSENDER, PASSWORT)
    server.sendmail(ABSENDER, EMPFANGER, nachricht.as_string())
    server.quit()

def main():
    print("🔍 Suche nach Leads läuft...")
    ergebnisse = []
    for begriff in SUCHANFRAGEN:
        treffer = suche_firmen(begriff)
        if treffer:
            ergebnisse.extend([f"Gefundene Firma bei Suche nach '{begriff}': {t}" for t in treffer])
        time.sleep(1)  # um Rate Limits zu vermeiden

    if ergebnisse:
        sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)
    else:
        print("Keine neuen Ergebnisse gefunden.")

if __name__ == "__main__":
    main()
