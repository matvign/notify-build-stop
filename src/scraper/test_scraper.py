import pytest
import json
import httpx
from httpx import Response, Request, MockTransport

from src.scraper.scraper import get_post_data, format_record, get_page, get_pagination


@pytest.mark.parametrize(
    "page, page_size, expected_index", [(0, 100, 0), (1, 100, 100)]
)
def test_get_post_data(page, page_size, expected_index):
    data = get_post_data(page, page_size)
    assert data["from"] == expected_index
    assert data["size"] == page_size


def test_format_record():
    with open("./src/mocks/record.json") as f:
        data = json.load(f)

        formatted = format_record(data)
        assert formatted["company_name"] == "Maxim Builders Pty Ltd"
        assert formatted["created_date"] == 1709294400


def test_format_record_source():
    record = {"no_source": True}
    formatted = format_record(record)

    assert formatted is None


def test_format_record_nameless():
    with open("./src/mocks/record.json") as f:
        data = json.load(f)
        data["_source"]["title"] = []

        formatted = format_record(data)
        assert formatted is None


def test_format_record_dateless():
    with open("./src/mocks/record.json") as f:
        data = json.load(f)
        data["_source"]["resource_date"] = []

        formatted = format_record(data)
        assert formatted is None


@pytest.mark.asyncio
async def test_get_page(monkeypatch):
    with open("./src/mocks/search.json") as f:
        data = json.load(f)

    async def mock_handler(request: Request) -> Response:
        return Response(200, json=data)

    transport = MockTransport(mock_handler)
    original_client = httpx.AsyncClient

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: original_client(transport=transport),
    )

    results = await get_page(page=1, page_size=10)
    assert len(results) == 3
    assert results == [
        {"company_name": "Maxim Builders Pty Ltd", "created_date": 1709294400},
        {"company_name": "Maxim Builders Pty Ltd", "created_date": 1709294400},
        {"company_name": "ABDC Holdings Pty Ltd", "created_date": 1654171200},
    ]


@pytest.mark.asyncio
async def test_get_pagination(monkeypatch):
    with open("./src/mocks/search.json") as f:
        data = json.load(f)

    async def mock_handler(request: Request) -> Response:
        return Response(200, json=data)

    transport = MockTransport(mock_handler)
    original_client = httpx.AsyncClient

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: original_client(transport=transport),
    )

    result = await get_pagination(page_size=10)
    assert result == 2
