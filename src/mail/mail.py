import os
import smtplib
from email.message import EmailMessage

smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")


def send_notification(company_name: str, company_number: str, datestr: str):
    msg = EmailMessage()
    msg["Subject"] = "Company Stop Build Order Notification"
    msg["From"] = ("stop-build@example.com",)
    msg["To"] = "recipient@example.com"
    msg.set_content(
        f"Company name: {company_name} (no. {company_number}) has been added as of {datestr}"
    )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        print(f'Sending message for {company_name} (no. {company_number})...')
        server.send_message(msg)
