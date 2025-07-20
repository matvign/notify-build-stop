import pytest
from datetime import datetime
from collections import namedtuple
from unittest.mock import AsyncMock, patch

from src.mail.mail import send_notification


@pytest.mark.asyncio
@patch("aiosmtplib.send", new_callable=AsyncMock)
async def test_send_notification(mock_send):
    company_tup = namedtuple("Company", ["Id", "Name", "CreatedDate"])
    dt = datetime(2025, 7, 21)

    company = company_tup(1, "Woolies", dt)

    await send_notification(company)

    mock_send.assert_awaited_once()
    email = mock_send.call_args[0][0]

    email_content = email.get_content()

    assert email["Subject"] == "Company Stop Build Order Notification"
    assert "Woolies" in email_content
    assert "21/07/2025" in email_content
    assert "(no. 1)" in email_content
