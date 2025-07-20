IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BuildStopDB')
BEGIN
    CREATE DATABASE BuildStopDB;
END
GO

USE BuildStopDB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Company')
BEGIN
    CREATE TABLE Company (
        Id INT IDENTITY(1, 1) PRIMARY KEY,
        Name NVARCHAR(100) UNIQUE NOT NULL,
        CreatedDate DATETIME2 NOT NULL
    );
END
GO
