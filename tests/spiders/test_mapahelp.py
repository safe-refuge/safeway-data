import pytest
from scrapy import Spider

from config import constants
from tests.utils import parse_betamax_response
from scraping.spiders.mapahelp import (
    MapaHelpSpider,
    CATEGORIES,
    extract_social,
)


SOCIAL_KNOWN = [
    ("https://www.facebook.com/handler", {"messenger": "https://www.facebook.com/handler"}, []),
    ("> https://t.me/handler", {"telegram": "https://t.me/handler"}, []),
    ("Telegram: @handler", {"telegram": "handler"}, []),
    ("handler (телеграм)", {"telegram": "handler"}, []),
    ("вацап - +123456", {"whatsapp": "+123456"}, []),
]

SOCIAL_UNKNOWN = [
    ("handler (all whatsapp, tg, fb)", {}, ["handler (all whatsapp, tg, fb)"]),
    ("Телеграм-канал: @handler", {}, ["Телеграм-канал: @handler"]),
]


@pytest.mark.parametrize("txt,known,unknown", SOCIAL_KNOWN + SOCIAL_UNKNOWN)
def test_extract_social(txt, known, unknown):
    known_social, unknown_social = extract_social(txt)
    assert known_social == known
    assert unknown_social == unknown


@pytest.mark.usefixtures("betamax_session")
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
