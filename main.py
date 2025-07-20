import asyncio
from src.scraper.scraper import scrape_orders
from src.queries.orders import process_orders

def main():
    orders = asyncio.run(scrape_orders(page_size=100))
    result = process_orders(orders)

    print(result)


if __name__ == "__main__":
    main()
