import asyncio
import re
from datetime import datetime, time

company_re = re.compile("Stop Work Order for (.*)", re.IGNORECASE)


async def throttled_call(sem: asyncio.Semaphore, fn, *args):
    async with sem:
        return await fn(*args)


def format_datetime(date: datetime) -> str:
    return date.strftime("%d/%m/%Y")


def to_datetime(timestamp: int) -> datetime:
    # convert timestamp into a datetime object
    # used for inserting into datetime2 fields in sqlserver
    return datetime.fromtimestamp(timestamp)
