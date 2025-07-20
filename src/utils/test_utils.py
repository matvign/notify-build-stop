import pytest
from datetime import datetime

from .utils import search_company_name, to_datetime, format_datetime


@pytest.mark.parametrize(
    "input, output",
    [
        ("Stop Work Order for Some Company", "Some Company"),
        ("Stop Work Order for a", "a"),
        ("Stop Work Order for ", ""),
        ("Stop Work Order for", ""),
    ],
)
def test_search_company_name(input, output):
    assert search_company_name(input) == output


@pytest.mark.parametrize("input, output", [(1654128000, (2022, 6, 2))])
def test_to_datetime(input, output):
    result = to_datetime(input)
    year, month, day = output

    assert result.year == year
    assert result.month == month
    assert result.day == day


@pytest.mark.parametrize(
    "input, output", [((2025, 7, 21), "21/07/2025"), ((2022, 6, 2), "02/06/2022")]
)
def test_format_datetime(input, output):
    dt = datetime(*input)
    datestr = format_datetime(dt)
    assert (datestr) == output
