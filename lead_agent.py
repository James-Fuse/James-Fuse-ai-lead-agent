import os
import smtplib
from email.mime.text import MIMEText

# Stichworte definieren
stichwoerter = [
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

# Dummy-Suche – simuliert echte Treffer
def suche_leads(keyword):
    # Hier kannst du deine eigene Suchlogik einfügen (z. B. Webscraping, API etc.)
    if keyword in ["Sicherung kaufen", "Class CC Sicherung gesucht"]:
        return [f"{keyword}:\n➡️ https://www.example.com/{keyword.replace(' ', '-')}/"]
    return []

# Hauptlogik
leads = []
for wort in stichwoerter:
    print(f"🔍 Suche: {wort}")
    resultate = suche_leads(wort)
    leads.extend(resultate)

# Immer E-Mail senden, auch wenn keine Leads
if leads:
    body = "Hier sind deine neuen Leads:\n\n" + "\n\n".join(leads)
else:
    body = "Diesmal wurden leider keine neuen Leads gefunden."

msg = MIMEText(body)
msg["Subject"] = "Lead-Agent – neue Ergebnisse"
msg["From"] = "lead-agent@james-fuse.de"
msg["To"] = "info@james-fuse.de"

# SMTP-Versand
server = smtplib.SMTP("smtp.ionos.de", 587)
server.starttls()
server.login("lead-agent@james-fuse.de", os.getenv("EMAIL_PASSWORD"))
server.sendmail(msg["From"], msg["To"], msg.as_string())
server.quit()
