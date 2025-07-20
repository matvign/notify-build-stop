from sqlalchemy import MetaData, Table
from src.db.db import engine

metadata = MetaData()

company_table = Table("Company", metadata, autoload_with=engine)
