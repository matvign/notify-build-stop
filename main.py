import asyncio

from src.scraper import scraper, process

SCHEDULED_INTERVAL = 3600
PAGE_SIZE = 100

async def scheduled_task():
    while True:
        orders = await scraper.scrape_orders(page_size=PAGE_SIZE)

        if orders:
            result = await process.process_orders(orders)
            print(f'Inserted {len(result)} new records')

        print(f'Waiting for {SCHEDULED_INTERVAL}s...')
        await asyncio.sleep(SCHEDULED_INTERVAL)


def main():
    asyncio.run(scheduled_task())


if __name__ == "__main__":
    try:
        print('Starting monitor...')
        main()
    except KeyboardInterrupt:
        print('Stopping monitor...')
