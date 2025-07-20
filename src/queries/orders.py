from datetime import datetime

from src.db import get_cursor
from src.mail import mail
from src.utils import utils


def process_orders(orders):
    # get set of existing company names from db
    company_names = get_company_names()
    existing_companies = set(company_names)

    seen_companies = set()
    filtered_companies = []

    # filter companies that already exist in db
    # there may be multiple stop work orders for the same company
    # use only the first company date found
    for company in orders:
        company_name = company.get("company_name")
        if (
            company_name not in seen_companies
            and company_name not in existing_companies
        ):
            filtered_companies.append(company)
            seen_companies.add(company_name)

    results = insert_companies(filtered_companies)

    # send email notifications for new companies that were inserted
    for new_company in results:
        id = new_company.Id
        name = new_company.Name
        date = new_company.CreatedDate

        formatted_date = utils.format_datetime(date)
        print(formatted_date)

        mail.send_notification(new_company.Name, new_company.Id, formatted_date)

    return


def get_company_names() -> list[str]:
    with get_cursor() as cursor:
        sql = """
        SELECT Name from Company;
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        return [row.Name for row in rows]


def insert_companies(companies):
    with get_cursor() as cursor:
        sql = """
        INSERT INTO Company (Name, CreatedDate)
        OUTPUT Inserted.Id, Inserted.Name, Inserted.CreatedDate
        VALUES (?, ?)
        """

        results = []

        for company in companies:
            company_name = company.get("company_name")
            company_date = company.get("created_date")
            formatted_date = utils.to_datetime(company_date)

            cursor.execute(sql, (company_name, formatted_date))
            row = cursor.fetchone()

            results.append(row)

        return results
