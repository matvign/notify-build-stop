from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime

metadata = MetaData()

company_table = Table(
    "Company",
    metadata,
    Column("Id", Integer, primary_key=True, autoincrement=True),
    Column("Name", String(100), unique=True, nullable=False),
    Column("CreatedDate", DateTime, nullable=False),
)
