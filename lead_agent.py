import smtplib
import os
import time
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

BEKANNTE_DATEI = "bekannte_links.json"
EMAIL_EMPFÄNGER = "info@james-fuse.de"
ABSENDER = "info@james-fuse.de"
PASSWORT = os.getenv("EMAIL_PASSWORD")

def lade_bekannte_links():
    if os.path.exists(BEKANNTE_DATEI):
        with open(BEKANNTE_DATEI, "r") as f:
            return set(json.load(f))
    return set()

def speichere_bekannte_links(links):
    with open(BEKANNTE_DATEI, "w") as f:
        json.dump(list(links), f)

def dummy_google_suche(begriff):
    # Dies ist ein Platzhalter. Hier soll in Zukunft echte Websuche implementiert werden.
    dummy_links = [
        f"https://www.wlw.de/suche?q={begriff.replace(' ', '+')}&firma=beispiel{n}"
        for n in range(1, 6)
    ]
    return dummy_links

def finde_neue_leads():
    bekannte_links = lade_bekannte_links()
    neue_links = set()
    ausgabe = ""

    for suchbegriff in SUCHBEGRIFFE:
        ausgabe += f"\n🔍 Suche: {suchbegriff}\n"
        ergebnisse = dummy_google_suche(suchbegriff)
        neue = [link for link in ergebnisse if link not in bekannte_links]

        for link in neue[:3]:  # Pro Suchbegriff max. 3 neue
            ausgabe += f"➡️ {link}\n"
            neue_links.add(link)

    bekannte_links.update(neue_links)
    speichere_bekannte_links(bekannte_links)
    return ausgabe.strip()

def sende_email(betreff, inhalt):
    msg = MIMEMultipart()
    msg["From"] = ABSENDER
    msg["To"] = EMAIL_EMPFÄNGER
    msg["Subject"] = betreff

    text = f"""
Sehr geehrte Damen und Herren,
mein Name ist Justin James, Geschäftsführer der James Fuse & Beyond GmbH mit Sitz in Königstein im Taunus. Wir sind spezialisiert auf die Lieferung von Industriesicherungen der Marke Eaton Bussmann. Durch die direkte Zusammenarbeit mit dem Hersteller können wir zertifizierte Qualität, schnelle Reaktionszeiten und sehr attraktive Konditionen bieten.
Unsere Produkte sind UL, CSA und CE zertifiziert und erfüllen höchste Qualitäts- und Sicherheitsstandards. Besonders möchten wir betonen, dass wir sowohl kleine als auch große Bestellungen flexibel und zuverlässig bedienen. Bei Mehrbestellungen und für Stammkunden sind selbstverständlich auch Rabatte möglich.
Viele unserer Hauptprodukte sind direkt ab Lager verfügbar, mit einer typischen Lieferzeit von 2 bis 3 Werktagen. Sollte ein Artikel nicht lagernd sein, liegt die Lieferzeit je nach Produkt bei maximal 2 bis 4 Wochen. Gerne informiere ich Sie auf Anfrage sofort über die konkrete Verfügbarkeit.
Ich würde mich freuen, mich als potenzieller Lieferant bei Ihnen vorstellen zu dürfen. Falls jetzt oder in Zukunft Bedarf besteht, sende ich Ihnen gerne ein individuelles Angebot oder weitere Informationen zu unserem Sortiment.

Vielen Dank für Ihre Zeit und freundliche Grüße an Ihr Team.

Hier sind neue potenzielle Kunden aus dem Internet:
{inhalt}

Mit freundlichen Grüßen,

Justin James  
Managing Director | James Fuse & Beyond GmbH  
Georg-Pingler-Straße 15  
61462 Königstein im Taunus, Germany  
Phone: +49 6174 9699645  
Email: info@james-fuse.de  
Website: www.james-fuse.de
"""
    msg.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.ionos.de", 587) as server:
        server.starttls()
        server.login(ABSENDER, PASSWORT)
        server.send_message(msg)

if __name__ == "__main__":
    ergebnisse = finde_neue_leads()
    if ergebnisse:
        sende_email("Neue Leads: Firmen mit Sicherungsbedarf", ergebnisse)
    else:
        sende_email("Keine neuen Leads gefunden", "Diesmal wurden keine neuen Ergebnisse gefunden.")
