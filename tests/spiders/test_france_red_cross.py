import pytest
from scrapy import Spider

from config import constants
from tests.utils import parse_betamax_response
from scraping.spiders.france_red_cross import (
    FranceRedCrossSpider,
    parse_points,
    CATEGORIES,
    SERVICES_TO_CATEGORIES,
)


@pytest.mark.usefixtures('betamax_session')
def test_parse_points(betamax_session):
    spider: Spider = FranceRedCrossSpider()
    url = spider.start_urls[0]
    points = parse_betamax_response(betamax_session, parse_points, url)
    assert points
    for point in points:
        assert point.name
        assert point.country
        assert point.city
        assert point.address
        assert point.description
        assert point.categories


def test_categories_mapping():
    cats = list(CATEGORIES.values()) + list(SERVICES_TO_CATEGORIES.values())
    for cat in cats:
        assert cat in constants.CATEGORIES
