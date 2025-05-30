import os
import smtplib
from email.message import EmailMessage

# Suchbegriffe für Leads
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

# Pfad zur Datei mit bekannten Links
bekannte_links_datei = "bekannte_links.txt"
if os.path.exists(bekannte_links_datei):
    with open(bekannte_links_datei, "r") as f:
        bekannte_links = set(f.read().splitlines())
else:
    bekannte_links = set()

# Simulierte Suchfunktion (hier bitte eigene Crawling- oder API-Logik einbauen)
def suche_leads(begriffe, bekannte_links):
    neue_links = set()
    for begriff in begriffe:
        print(f"🔍 Suche: {begriff}")
        link = f"https://www.wlw.de/de/suche?q={begriff.replace(' ', '+')}"
        if link not in bekannte_links:
            neue_links.add(link)
    return list(neue_links)[:10]  # Max. 10 neue Leads

neue_links = suche_leads(suchbegriffe, bekannte_links)

# E-Mail nur senden, wenn es neue Leads gibt
if neue_links:
    absender = "info@james-fuse.de"
    empfaenger = "info@james-fuse.de"
    passwort = os.getenv("EMAIL_PASSWORD")

    # E-Mail-Inhalt
    message = EmailMessage()
    message["Subject"] = "Neue potenzielle Kunden gefunden"
    message["From"] = absender
    message["To"] = empfaenger

    inhalt = "Hier sind neue potenzielle Kunden:\n\n"
    for link in neue_links:
        inhalt += f"➡️ {link}\n"
    message.set_content(inhalt)

    # E-Mail versenden
    with smtplib.SMTP_SSL("smtp.ionos.de", 465) as server:
        server.login(absender, passwort)
        server.send_message(message)

    print("✅ E-Mail wurde erfolgreich gesendet.")

    # Neue Links merken
    bekannte_links.update(neue_links)
    with open(bekannte_links_datei, "w") as f:
        f.write("\n".join(bekannte_links))
else:
    print("ℹ️ Keine neuen Leads. Keine E-Mail gesendet.")
