import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Konfiguration
SMTP_SERVER = 'smtp.ionos.de'
SMTP_PORT = 587
EMAIL_SENDER = 'lead-agent@james-fuse.de'
EMAIL_RECEIVER = 'info@james-fuse.de'
EMAIL_SUBJECT = 'Neue potenzielle Leads (James Fuse Lead Agent)'

# Dummy-Links als Beispiel (normalerweise durch die Suche generiert)
neue_leads = [
    'https://www.wlw.de/de/firma/fronius-schweiz-ag-100136',
    'https://www.wlw.de/de/firma/dosen-zentrale-zuechner-gmbh-395576',
    'https://www.wlw.de/de/firma/wurster-druck-verpackung-gmbh-1152358'
]

# Email-Inhalt erstellen
body = '🔍 Neue potenzielle Leads gefunden (Stand: {})\n\n'.format(datetime.now().strftime('%d.%m.%Y %H:%M'))
for link in neue_leads:
    body += f'➡️ {link}\n'

msg = MIMEMultipart()
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_RECEIVER
msg['Subject'] = EMAIL_SUBJECT
msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, os.getenv("EMAIL_PASSWORD"))
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ E-Mail erfolgreich gesendet.")
except Exception as e:
    print("❌ Fehler beim Senden der E-Mail:", e)
