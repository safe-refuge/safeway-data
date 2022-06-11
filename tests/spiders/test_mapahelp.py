import pytest
from scrapy import Spider

from config import constants
from tests.utils import parse_betamax_response
from scraping.spiders.mapahelp import (
    MapaHelpSpider,
    CATEGORIES,
)


@pytest.mark.usefixtures('betamax_session')
def test_parse_points(betamax_session):
    spider: Spider = MapaHelpSpider()
    url = spider.start_urls[0]
    points = parse_betamax_response(betamax_session, spider.parse, url)
    assert points
    for point in points:
        assert point.name
        assert point.country
        assert point.categories
        assert point.lat
        assert point.lng


def test_categories_mapping():
    for cat in CATEGORIES.values():
        assert cat in constants.CATEGORIES
