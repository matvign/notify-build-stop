# Notify Build Stop

# Task
Build a company Building Stop Work Orders monitor

# Objective
To evaluate the candidate's ability to build a web scraper and notification system that monitors company liquidations listed on the Register of building work orders. [Link to website](www.nsw.gov.au/departments-and-agencies/building-commission/register-of-building-work-orders).

# Requirements
The web scraper should scrape data from building work orders notice board website, specifically the section that lists companies that are in the process of Stop work orders.
* The data should be stored in a SQL server database.
* The system should have a trigger mechanism that sends an email notification when a new company is added to the list of Stop work orders section in website.
* The email notification should include the company name, company number, and the date it was added to the list of companies in liquidation.

The candidate should provide clear documentation on how to run the system, including any required setup steps.

# Evaluation Criteria
The functionality of the web scraper, including the ability to scrape data from the **building work orders** notice board website and store it in the database.

The functionality of the notification system, including the ability to send an email notification when a new company is added to the Stop work orders list.

The quality of the code, including maintainability, readability, and best practices.

The ability to follow the requirements and provide clear documentation.

# Prerequisites
* Ubuntu 24.04
* Docker (for SQL Server 2022)
* ODBC Driver 18 for Ubuntu 22.04
* Python >= 3.12
* pipx (install CLI tools)
* uv (package and dependency management)
* make (script management)
* dotenvx (environment variable management)

## Installation steps
1. [Install Docker Engine](https://docs.docker.com/engine/install/)
2. [Install ODBC Driver 18](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver17&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline)
3. [Install Python 3.12](https://www.python.org/downloads/)
4. [Install pipx](https://github.com/pypa/pipx)
5. [Install uv](https://github.com/astral-sh/uv)
6. [Install dotenvx](https://dotenvx.com/docs/install)
7. Install `make` using `sudo apt install build-essential`
8. Copy and paste contents of `env_sample` and `env_sample_docker` into `.env` and `.env.docker`
9. Install dependencies with `make install`
10. Setup Docker containers with `make docker`
11. Start local mail server with `make smtpd`
12. Open another terminal and run `make main` to start monitoring script

Note: For ODBC Driver, replace `/ubuntu/$(grep version ...)/` with `/ubuntu/22.04`.

## Formatting and Linting
This repo uses `ruff` for formatting and linting.
* Lint: `make lint`
* Format: `make format`

## Tests
This repo uses pytest for unit tests. Run `make test` for unit tests.

# Solution Notes
## Scraping
The page populates stop work orders through Javascript, so simple HTML parsing wouldn't be enough. You would need to scrape through it using an automated browser tool like Playwright.

A much better alternative is obtaining the data directly from the Elasticsearch endpoint that the frontend uses. This is faster as you won't need to spin up a browser environment, and would be less prone to breaking if the page layout changes.

This solution focuses on using the Elasticsearch endpoint. (Hopefully using the API is not completely misinterpreting the requirements)

This solution calls the API with a page size of 100, and sorts the results by ascending order (default is descending). 
This means that we can get the earliest stop work orders when there are companies that have multiple work orders.

We can also make an initial call to figure out how many pages we need to fetch. As there are possible API throttling concerns,
we use semaphores to limit the number of concurrent requests at once.

The scraper takes the company name from the title and uses the resource date of the result as the date that the stop work order was created. This is because the resource date also happens to be the criteria used for sorting dates for the orders.


Playwright isn't used here, but a possible solution would be:
* Visit the page (using query parameters prefilled for stop build orders)
* Wait for the results to populate
* Crawl and store the results
* Check for the next page button and click it
* Continue until next page button no longer in the document
* Reverse the results to get results ordered from earliest to most recent

## Database
This solution creates a SQL Server development database using Docker. After calling docker compose, SQL Server will initialise a database and a table to store `Company` information.

The table includes:
* Autoincrementing Id
* Name (unique constraint)
* CreatedDate

There doesn't appear to be any unique identifier for companies in the scraped data. In place of this, an autoincrementing id is used.

SQLAlchemy Core is used for database queries. Queries for inserting a company also return the record, which is later used for sending email notifications.

## Mail Server
This solution uses a local mail server to send and receive mails. This helps avoid sending real email messages, and is useful for testing in development.

The messages are sent from "stop-build@example.com" to "recipient@example.com", which are placeholders for real emails. 

## Monitoring
This solution runs the scraper on a loop. Any new companies found are inserted into the database before waiting an hour to be invoked again.

# Considerations
The scraping solution gets all records from the API. This could become heavier over time. A more efficient solution would be to store the last access time (in the database or a file) and use that to filter new work orders.  
We could replicate the exact way that the frontend does this, using Elasticsearch scripting to filter out dates.

The current solution initializes tables through Docker. If additional database table changes are required, a database migration tool such as Alembic could be used.

The database queries use SQLAlchemy Core for simplicity. If the data model or logic becomes more complex, adopting SQLAlchemy’s ORM can improve maintainability and readability.

This solution is designed to run locally. For hosting, running this on an AWS Lambda or Azure Function and set on a timer would be ideal. As we need ODBC driver support, we could create Docker images with the driver support installed. Both AWS Lambda and Azure Function support containers.

Email sender and recipient are hardcoded at the moment. An environment variable would be ideal for configuring emails.

The email notification sends a plain text response. A better message format and possibly HTML email would be appreciated for consumers.

Full test coverage was omitted to this task due to limited time. For production code, tests should aim for higher coverage rate to ensure correctness and quality.

Type hints for complex objects and docstrings were omitted for time, but are very useful for readability and maintanence.

Formatting and linting is implemented through ruff, but there are currently no git hooks to enforce quality.

Conventional commits help with managing releases, but wasn't deemed necessary here. In a larger team setting, conventional commits should be used to help with automated changelog and versioning.
