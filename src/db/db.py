import pyodbc
from contextlib import contextmanager

@contextmanager
def get_cursor():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=BuildStopDB;"
        "UID=sa;"
        "PWD=YourStrong!Passw0rd;"
        "TrustServerCertificate=yes;"
    )

    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    finally:
        conn.close
