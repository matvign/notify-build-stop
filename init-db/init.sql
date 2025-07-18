CREATE DATABASE BuildStopDB;
GO
USE BuildStopDB;

CREATE TABLE Company (
    Id INT PRIMARY KEY,
    Name NVARCHAR(100)
);
GO

CREATE TABLE StopOrder (
    Id INT PRIMARY KEY,
    CompanyId INT,
    CreatedDate DATE,
    CONSTRAINT FK_Company FOREIGN KEY (CompanyId) REFERENCES Company(id)
);
GO
