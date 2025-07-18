import os
import smtplib
from email.message import EmailMessage

smtp_host = os.getenv('SMTP_HOST')
smtp_port = os.getenv('SMTP_PORT')

def send_notification(company_name: str, company_number: str, date: str):
    msg = EmailMessage()
    msg["Subject"] = "Stop Build Order Notification"
    msg["From"] = "stop-build@example.com",
    msg["To"] = "recipient@example.com"
    msg.set_content(f'{company_name} {company_number} {date}')

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.send_message(msg)
