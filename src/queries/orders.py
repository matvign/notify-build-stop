import pyodbc

def query():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=localhost,1433;'
        'DATABASE=BuildStopDB;'
        'UID=sa;'
        'PWD=YourStrong!Passw0rd;'
        'TrustServerCertificate=yes;'
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM INFORMATION_SCHEMA.TABLES;
    """)
    for row in cursor.fetchall():
        print(row.TABLE_SCHEMA, row.TABLE_NAME)

    cursor.close()
    conn.close()