import pytest
from scrapy import Spider

from scraping.tests.utils import get_betamax_response
from scraping.spiders.france_red_cross import (
    FranceRedCrossSpider,
    parse_points,
)


@pytest.mark.usefixtures('betamax_session')
def test_parse_points(betamax_session):
    spider: Spider = FranceRedCrossSpider()
    url = spider.start_urls[0]
    response = get_betamax_response(betamax_session, url)

    points = parse_points(response)
    assert points

    for point in points:
        assert point.get('name')
        assert point.get('country')
        assert point.get('city')
        assert point.get('address')
        assert point.get('description')
        assert len(point.get('categories')) > 0
