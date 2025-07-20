import pyodbc
import os
from contextlib import contextmanager


@contextmanager
def get_cursor():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_UID')};"
        f"PWD={os.getenv('DB_PWD')};"
        "TrustServerCertificate=yes;"
    )

    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    finally:
        conn.close
