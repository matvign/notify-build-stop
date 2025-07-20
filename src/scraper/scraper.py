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


def format(hit):
    source = hit.get("_source", None)
    if not source:
        return None

    title = next(iter(source.get("title", [])), None)
    summary = next(iter(source.get("summary", [])), None)
    created_date = next(iter(source.get("resource_date", [])), None)

    company_name = ""
    match = utils.company_re.search(title)
    if match:
        company_name = match.group(1)

    return {
        "title": title,
        "summary": summary,
        "created_date": created_date,
        "company_name": company_name,
    }


async def get_page(page: int, page_size: int):
    try:
        async with httpx.AsyncClient() as client:
            query = get_post_data(page, page_size)

            response = await client.post(ENDPOINT, json=query)
            data = response.json()

            results = data.get("hits", {})
            page_data = results.get("hits", [])

            formatted = [format(i) for i in page_data]

            return formatted
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
    # get number of pages we need to fetch
    pages_total = await get_pagination(page_size)

    if pages_total == 0:
        print(f"No pages to scrape")
        return

    async with httpx.AsyncClient() as client:
        # gather tasks to run
        # use semaphore to help with throttling
        tasks = [
            utils.throttled_call(sem, get_page, i, page_size)
            for i in range(0, pages_total)
        ]
        stop_orders = await asyncio.gather(*tasks)

        # flatten results into single list
        formatted = [item for page in stop_orders for item in page]

        return formatted
