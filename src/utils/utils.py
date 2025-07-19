import asyncio
import re
from datetime import datetime, time

company_re = re.compile('Stop Work Order for (.*)', re.IGNORECASE)

async def throttled_call(sem: asyncio.Semaphore, fn, *args):
    async with sem:
        return await fn(*args)

# Elasticsearch uses ms in its filtering
def convert_datestr(datestr: str) -> int:
    date_format = '%d/%m/%Y'
    dt = datetime.strptime(datestr, date_format)
    timestamp = dt.timestamp()
    timestamp_ms = int(timestamp * 1000)

    return timestamp_ms

def eod_timestamp() -> int:
    now = datetime.now()
    dt = datetime.combine(now.date(), time(23, 59, 59))
    eod = dt.timestamp()
    eod_ms = int(eod) * 1000

    return eod_ms

def convert_timestamp() -> str:
    timestamp = 1752933599999
    dt = datetime.fromtimestamp(timestamp / 1000)
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # e.g. '2025-07-14 00:00:00'
