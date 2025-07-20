import asyncio
import httpx
import math

from src.utils import utils

ENDPOINT = "https://www.nsw.gov.au/api/v1/elasticsearch/prod_content/_search"
SEMAPHORE_COUNT = 3

sem = asyncio.Semaphore(SEMAPHORE_COUNT)


def get_post_data(page: int, page_size: int):
    from_index = page * page_size

    return {
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {"term": {"type": "resource"}},
                    {"terms": {"agency_name": ["Building Commission NSW"]}},
                    {
                        "terms": {
                            "name_category": [
                                "Building work rectification orders",
                                "Prohibition orders",
                                "Stop work orders",
                                "Rectification orders",
                            ]
                        }
                    },
                    {"terms": {"name_category": ["Stop work orders"]}},
                ],
            }
        },
        "sort": [{"_score": "desc"}, {"resource_date": "asc"}],
        "from": from_index,
        "size": page_size,
    }


def format_record(record):
    source = record.get("_source", None)
    if not source:
        return None

    title = next(iter(source.get("title", [])), "")
    created_date = next(iter(source.get("resource_date", [])), None)

    company_name = ""
    match = utils.company_re.search(title)
    if match:
        company_name = match.group(1)

    if not company_name or not created_date:
        return None

    return {
        "company_name": company_name,
        "created_date": created_date,
    }


async def get_page(page: int, page_size: int):
    try:
        async with httpx.AsyncClient() as client:
            query = get_post_data(page, page_size)

            response = await client.post(ENDPOINT, json=query)
            data = response.json()

            results = data.get("hits", {})
            page_data = results.get("hits", [])

            formatted = [format_record(record) for record in page_data]

            # filter out any invalid records that don't have a proper company name
            filtered = [record for record in formatted if record is not None]

            return filtered
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return []


async def get_pagination(page_size: int):
    try:
        async with httpx.AsyncClient() as client:
            query = get_post_data(page=0, page_size=1)

            response = await client.post(ENDPOINT, json=query)
            data = response.json()
            results = data.get("hits", {})

            # total hits and pages
            total = results.get("total", {}).get("value", 0)
            pages_total = math.ceil(total / page_size)

            return pages_total
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return 0


async def scrape_orders(page_size: int):
    if page_size <= 0:
        print("Page size should be at least 1")
        return []

    # get number of pages we need to fetch
    pages_total = await get_pagination(page_size)

    if pages_total == 0:
        print("No pages to scrape")
        return []

    # gather tasks to run
    # use semaphore to help with throttling
    tasks = [
        utils.throttled_call(sem, get_page, i, page_size) for i in range(0, pages_total)
    ]
    stop_orders = await asyncio.gather(*tasks)

    # flatten results into single list
    formatted = [item for page in stop_orders for item in page]

    print(f"Found {len(formatted)} stop work orders")

    return formatted
