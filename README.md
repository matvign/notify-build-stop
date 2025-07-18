# Notify Build Stop

## Task
Build a company Building Stop Work Orders monitor

## Objective
To evaluate the candidate's ability to build a web scraper and notification system that monitors company liquidations listed on the Register of building work orders [Link to website](www.nsw.gov.au/departments-and-agencies/building-commission/register-of-building-work-orders).

## Requirements
The web scraper should scrape data from building work orders notice board website, specifically the section that lists companies that are in the process of Stop work orders.
* The data should be stored in a SQL server database.
* The system should have a trigger mechanism that sends an email notification when a new company is added to the list of Stop work orders section in website.
* The email notification should include the company name, company number, and the date it was added to the list of companies in liquidation.

The candidate should provide clear documentation on how to run the system, including any required setup steps.

## Evaluation Criteria
The functionality of the web scraper, including the ability to scrape data from the **building work orders** notice board website and store it in the database.

The functionality of the notification system, including the ability to send an email notification when a new company is added to the Stop work orders list.

The quality of the code, including maintainability, readability, and best practices.

The ability to follow the requirements and provide clear documentation.

## Installation requirements
* Python >= 3.12
* uv (package and dependency management)
* Docker Engine

### Installation steps
1. Install Python 3.12
2. Install pipx
3. Install uv through pipx
4. Install Docker
5. Go into this repo, run `make install`
