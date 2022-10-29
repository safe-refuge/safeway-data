import pytest

from config import constants
from tests.utils import get_betamax_response
from scraping.spiders.umapa import (
    UmapaSpider,
    HEADERS,
    CATEGORIES,
    get_points_list,
    get_point_url,
    build_point,
)


@pytest.mark.usefixtures("betamax_session")
def test_get_points(betamax_session):
    url = UmapaSpider.start_urls[0]
    response = get_betamax_response(betamax_session, url, headers=HEADERS)
    points = get_points_list(response)
    assert points
    for point in points:
        assert "id" in point["properties"]


@pytest.mark.usefixtures("betamax_session")
def test_build_point(betamax_session):
    url = UmapaSpider.start_urls[0]
    response = get_betamax_response(betamax_session, url, headers=HEADERS)
    points = get_points_list(response)

    url = get_point_url(next(points))
    response = get_betamax_response(betamax_session, url, headers=HEADERS)
    details = build_point(response)

    assert details["name"]
    assert details["lat"]
    assert details["lng"]
    assert details["address"]
    assert details["email"]
    assert details["phone"]
    assert details["url"]
    assert details["categories"]


def test_categories_mapping():
    for cat in CATEGORIES.values():
        assert cat in constants.CATEGORIES
