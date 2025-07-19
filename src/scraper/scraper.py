import asyncio
import httpx
import math

from src.utils import utils

SEMAPHORE_COUNT = 3

ENDPOINT = 'https://www.nsw.gov.au/api/v1/elasticsearch/prod_content/_search'

# Script taken from page when filtering by dates
SCRIPT = """
int l = doc[params.open].length;
boolean isValid = false;
for (int i = 0; i<l; i++) {
    JodaCompatibleZonedDateTime open = doc[params.open].get(i);
    JodaCompatibleZonedDateTime close = doc[params.close].get(i);
    long open_val = open.getMillis();
    long close_val = close.getMillis();
    if (open_val <= params.end && close_val >= params.start) {
        isValid = true;
    }    
}

return isValid;
"""

sem = asyncio.Semaphore(SEMAPHORE_COUNT)

def get_datefilter(start: int):
    if not start:
        return {}

    print(start)

    eod = utils.eod_timestamp()
    script = {
        "script": {
            "script": {
                "source": SCRIPT,
                "params": {
                    "start": start,
                    "end": eod,
                    "open": "resource_date",
                    "close": "resource_date"
                }
            }
        }
    }

    return script

def get_queryparams(page: int, page_size: int, start: int = 0):
    from_index = page * page_size

    query = {
        'query': {
            'bool': {
                'must': [],
                'filter': [
                    {'term': {'type': 'resource'}},
                    {'terms': {'agency_name': ['Building Commission NSW']}},
                    {
                        'terms': {
                            'name_category': [
                                'Building work rectification orders',
                                'Prohibition orders',
                                'Stop work orders',
                                'Rectification orders',
                            ]
                        }
                    },
                    {'terms': {'name_category': ['Stop work orders']}},
                    *([get_datefilter(start)] if start else []) 
                ],
            }
        },
        'sort': [{'_score': 'desc'}, {'resource_date': 'desc'}],
        'from': from_index,
        'size': page_size,
    }

    return query

def format(hit):
    source = hit.get('_source', None)
    if not source:
        return None

    title = next(iter(source.get('title', [])), None)
    summary = next(iter(source.get('summary', [])), None)
    createdDate = next(iter(source.get('utc_created', [])), None)

    company_name = ''
    match = utils.company_re.search(title)
    if match:
        company_name = match.group(1)

    return { 'title': title, 'summary': summary, 'createdDate': createdDate, 'companyName': company_name }

async def get_page(page: int, page_size: int):
    async with httpx.AsyncClient() as client:
        query = get_queryparams(page, page_size)

        response = await client.post(ENDPOINT, json=query)
        data = response.json()

        results = data.get('hits', {})
        page_data = results.get('hits', [])

        formatted = [format(i) for i in page_data]

        return formatted

async def scrape_orders(page_size: int):
    async with httpx.AsyncClient() as client:
        # get total pages first
        query = get_queryparams(page=0, page_size=1)

        response = await client.post(ENDPOINT, json=query)
        data = response.json()
        results = data.get('hits', {})

        # total hits and pages
        total = results.get('total', {}).get('value', 0)
        pages_total = math.ceil(total / page_size)

        # gather tasks to run
        # use semaphore to help with throttling
        tasks = [utils.throttled_call(sem, get_page, i, page_size) for i in range(0, pages_total)]
        data_pages = await asyncio.gather(*tasks)

        # flatten results into single list
        formatted = [item for page in data_pages for item in page]

        return formatted
