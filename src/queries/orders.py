from src.db import get_cursor

def process_companies(companies):
    # there may be multiple stop work orders for the same company
    # get only the first one that you come across
    seen_companies = {}
    filtered_companies = []

    for company in companies:
        company_name = company.get('companyName')
        if company_name not in seen_companies:
            filtered_companies.append(company)


def get_companies():
    with get_cursor() as cursor:
        sql = """
        SELECT Company.Name from Company
        """

        rows = cursor.execute(sql)
        return rows

