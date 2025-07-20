import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


DRIVER = "ODBC Driver 18 for SQL Server"

is_dev = os.getenv("ENVIRONMENT", "development") == "development"

query_params = {"driver": DRIVER}

if is_dev:
    query_params["TrustServerCertificate"] = "Yes"

connection_url = URL.create(
    "mssql+pyodbc",
    username=os.getenv("DB_UID"),
    password=os.getenv("DB_PWD"),
    host=os.getenv("DB_SERVER"),
    database=os.getenv("DB_NAME"),
    query=query_params,
)

engine = create_engine(connection_url)
