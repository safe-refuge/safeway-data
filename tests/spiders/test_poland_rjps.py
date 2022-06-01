import os

import pytest
from scrapy.http import HtmlResponse

from repositories.csv import open_read_only_file
from scraping.spiders.poland_rjps import QuotesSpider
from config.settings import Settings

settings = Settings()
DATA_PATH = f'{settings.spider_data_path}/rips'


def build_response_with_file(file_name: str) -> HtmlResponse:
    raw_text = open_read_only_file(f'{DATA_PATH}/{file_name}')
    body = '\n'.join(raw_text.readlines())
    return HtmlResponse(body=body, encoding='utf-8', url='test.com')


@pytest.fixture
def normal_place():
    return build_response_with_file('normal_page.html')


@pytest.fixture
def missing_info_place():
    return build_response_with_file('missing_info_page.html')


class TestQuotesSpider:
    def test_parse_name(self, normal_place):
        name = QuotesSpider().parse(normal_place, category='test').get('name')
        assert name == 'Miejski Ośrodek Pomocy Społecznej w Zabłudowie'

    def test_parse_address(self, normal_place):
        address = QuotesSpider().parse(normal_place, category='test').get('address')

        assert address == '16-060 Zabłudów ul. Rynek 8'

    def test_parse_email(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'biuro@mops-zabludow.pl' in description

    def test_parse_phone(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'tel. 85 7188100' in description

    def test_parse_website(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'http://bip.mops.um.zabludow.wrotapodlasia.pl' in description

    def test_parse_update_date(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'data aktualizacji: 2018-02-05' in description

    def test_parse_missing_info_page(self, missing_info_place):
        description = QuotesSpider().parse(missing_info_place, category='test').get('description')
        assert 'data aktualizacji: 2013-12-13' in description
