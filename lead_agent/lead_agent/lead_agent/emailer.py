import os
import smtplib, ssl
from email.message import EmailMessage
from typing import List

def send_email(sender: str, password: str, recipients: List[str], subject: str,
               body: str, attachments: List[str] = None,
               smtp_host: str = "smtp.gmail.com", smtp_port: int = 587):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join([r for r in recipients if r])
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments or []:
        with open(path, "rb") as f:
            data = f.read()
        filename = os.path.basename(path)
        msg.add_attachment(data, maintype="text", subtype="csv", filename=filename)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender, password)
        server.send_message(msg)
