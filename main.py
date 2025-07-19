import asyncio
from scraper.scraper import scrape_orders
# from queries.orders import process_companies

def main():
    result = asyncio.run(scrape_orders(page_size=100))
    print(result)


if __name__ == "__main__":
    main()
