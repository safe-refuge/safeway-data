import pytest
from scrapy import Spider

from config import constants
from tests.utils import parse_betamax_response, get_betamax_response
from scraping.spiders.canada_immigration_services import (
    CanadaImmigrationServicesSpider,
    CATEGORIES,
    SERVICES,
    parse_response,
    build_categories,
)


@pytest.mark.usefixtures("betamax_session")
def test_parse_points(betamax_session):
    spider: Spider = CanadaImmigrationServicesSpider()
    url = spider.start_urls[0]
    points = parse_betamax_response(betamax_session, spider.parse, url)
    assert points
    for point in points:
        assert point.name
        assert point.country
        assert point.city
        assert point.address
        assert point.categories
        assert point.organizations


def test_categories_mapping():
    for cat in CATEGORIES.values():
        assert cat in constants.CATEGORIES


@pytest.mark.usefixtures("betamax_session")
def test_build_categories(betamax_session):
    spider: Spider = CanadaImmigrationServicesSpider()
    url = spider.start_urls[0]
    response = get_betamax_response(betamax_session, url)
    for point in parse_response(response):
        relevant_categories, other_categories = build_categories(point)
        for cat in relevant_categories:
            assert cat in list(CATEGORIES.values())
        for cat in other_categories:
            assert cat in list(SERVICES.values())
