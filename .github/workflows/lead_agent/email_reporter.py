# lead_agent/email_reporter.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lead_agent import config

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = config.SMTP_USERNAME
        msg['To'] = config.EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(msg)

        print("✅ E-Mail erfolgreich gesendet.")
    except Exception as e:
        print("❌ Fehler beim Senden der E-Mail:", e)
