import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from collections import namedtuple
from datetime import datetime

from src.scraper.process import process_orders, filter_companies

company_tup = namedtuple("Company", ["Id", "Name", "CreatedDate"])

orders = [
    {"company_name": "Maxim Builders Pty Ltd", "created_date": 1709294200},
    {"company_name": "Maxim Builders Pty Ltd", "created_date": 1709294400},
    {"company_name": "ABDC Holdings Pty Ltd", "created_date": 1654171200},
]


@pytest.mark.parametrize(
    "orders, company_names, output",
    [
        # filters out all of maxim builders, leaves only abdc holdings
        (
            orders,
            ["Maxim Builders Pty Ltd"],
            [{"company_name": "ABDC Holdings Pty Ltd", "created_date": 1654171200}],
        ),
        # filterse out abdc holdings, takes the first maxim builders
        (
            orders,
            ["ABDC Holdings Pty Ltd"],
            [{"company_name": "Maxim Builders Pty Ltd", "created_date": 1709294200}],
        ),
    ],
)
def test_filter_companies(orders, company_names, output):
    result = filter_companies(orders, company_names)
    assert result == output


@pytest.mark.asyncio
async def test_process_orders_empty():
    # no orders, should just return empty result
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    with (
        patch("src.db.db.engine", mock_engine),
        patch(
            "src.scraper.process.select_companies_intersect",
            return_value=[],
        ),
        patch("src.scraper.process.insert_companies", return_value=[]),
    ):
        orders = []
        result = await process_orders(orders)
        assert result == []


@pytest.mark.asyncio
async def test_process_orders():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    """
    Assume maxim builders exists already in the db
    Send company names to check if the names exist
    Filter out Maxim
    Insert ADBC Holdings
    Assert that emails were sent
    Assert that result was the filtered out values
    """
    dt = datetime(2022, 6, 2)
    mock_select = ["Maxim Builders Pty Ltd"]
    mock_insert = company_tup(2, "ABDC Holdings Pty Ltd", dt)

    with (
        patch("src.db.db.engine", mock_engine),
        patch("src.mail.mail.send_all", new_callable=AsyncMock) as mocked_send,
        patch(
            "src.scraper.process.select_companies_intersect",
            return_value=mock_select,
        ) as mocked_select,
        patch(
            "src.scraper.process.insert_companies", return_value=mock_insert
        ) as mocked_insert,
    ):
        result = await process_orders(orders)

        mocked_select.assert_called_once_with(
            ["Maxim Builders Pty Ltd", "ABDC Holdings Pty Ltd"]
        )

        mocked_insert.assert_called_once_with(
            [
                {"company_name": "ABDC Holdings Pty Ltd", "created_date": 1654171200},
            ]
        )

        mocked_send.assert_awaited_once()

        assert result == [
            {"company_name": "ABDC Holdings Pty Ltd", "created_date": 1654171200},
        ]
