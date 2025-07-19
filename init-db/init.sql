CREATE DATABASE BuildStopDB;
GO
USE BuildStopDB;

CREATE TABLE Company (
    Id INT PRIMARY KEY,
    Name NVARCHAR(100),
    CreatedDate DATE,
);
GO
