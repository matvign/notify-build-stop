import asyncio
import aiosmtplib
import os
from email.message import EmailMessage

from src.utils.utils import format_datetime

smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")


async def send_all(companies):
    try:
        tasks = [send_notification(company) for company in companies]
        await asyncio.gather(*tasks)
    except Exception:
        print("Failed to send mail")


async def send_notification(company):
    id = company.Id
    name = company.Name
    date = company.CreatedDate
    formatted_date = format_datetime(date)

    msg = EmailMessage()
    msg["Subject"] = "Company Stop Build Order Notification"
    msg["From"] = ("stop-build@example.com",)
    msg["To"] = "recipient@example.com"
    msg.set_content(
        f"Company name: {name} (no. {id}) has been added to stop work orders as of {formatted_date}"
    )

    await aiosmtplib.send(msg, hostname=smtp_host, port=smtp_port)
