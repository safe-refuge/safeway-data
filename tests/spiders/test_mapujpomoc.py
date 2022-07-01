import pytest
from scrapy import Spider

from config import constants
from tests.utils import parse_betamax_response, get_betamax_response
from scraping.spiders.mapujpomoc import (
    MapujpomocSpider,
    CATEGORIES,
    parse_points,
    parse_details_page,
)


@pytest.mark.usefixtures('betamax_session')
def test_parse_points(betamax_session):
    spider: Spider = MapujpomocSpider()
    url = spider.start_urls[0]
    points = parse_betamax_response(betamax_session, parse_points, url)
    assert points
    for point in points:
        assert point.name
        assert point.country
        assert point.lat
        assert point.lng
        assert point.url


@pytest.mark.usefixtures('betamax_session')
def test_parse_details(betamax_session):
    spider: Spider = MapujpomocSpider()
    url = spider.start_urls[0]
    response = get_betamax_response(betamax_session, url)
    points = list(parse_points(response))

    url = points[0]['url']
    response = get_betamax_response(betamax_session, url)
    details = parse_details_page(response, {})

    assert details['country']
    assert details['city']
    assert details['address']
    assert details['email']
    assert details['phone']
    assert details['url']
    assert details['categories']
    assert details['description']


def test_categories_mapping():
    for cat in CATEGORIES.values():
        assert cat in constants.CATEGORIES
