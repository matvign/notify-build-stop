from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from src.db import engine, company_table
from src.mail import mail
from src.utils import utils


def filter_companies(orders, company_names: list[str]):
    intersect = set(company_names)
    seen_companies = set()
    filtered_companies = []

    for company in orders:
        company_name = company.get("company_name")
        if company_name not in seen_companies and company_name not in intersect:
            filtered_companies.append(company)
            seen_companies.add(company_name)

    return filtered_companies


async def process_orders(orders):
    """
    From the scraped orders, filter out companies that already exist in the db.
    If there are multiple companies in orders, use the first instance found.

    From the filtered out companies, insert them and send email notifications for each
    """
    if not len(orders):
        return []

    company_names = [order.get("company_name") for order in orders]
    uniq_names = list(dict.fromkeys(company_names))

    try:
        company_intersect = select_companies_intersect(uniq_names)
    except SQLAlchemyError:
        print("Couldn't get overlapping companies")
        return []

    filtered_companies = filter_companies(orders, company_intersect)

    if len(filtered_companies):
        try:
            results = insert_companies(filtered_companies)
            await mail.send_all(results)
        except SQLAlchemyError:
            print("Failed to insert new companies")
            return []

    return filtered_companies


def select_companies_intersect(companies: list[str]) -> list[str]:
    query = select(company_table.c.Name).where(company_table.c.Name.in_(companies))

    with engine.connect() as conn:
        result = conn.execute(query)
        return [row.Name for row in result]


def insert_companies(companies):
    results = []

    with engine.begin() as conn:
        for company in companies:
            company_name = company.get("company_name")
            company_date = company.get("created_date")
            formatted_date = utils.to_datetime(company_date)

            query = (
                insert(company_table)
                .values(Name=company_name, CreatedDate=formatted_date)
                .returning(
                    company_table.c.Id,
                    company_table.c.Name,
                    company_table.c.CreatedDate,
                )
            )
            result = conn.execute(query)

            row = result.fetchone()
            results.append(row)

    return results
