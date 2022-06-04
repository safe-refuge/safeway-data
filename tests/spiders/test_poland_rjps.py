from collections import OrderedDict

import pytest
from scrapy.http import HtmlResponse

from repositories.csv import open_read_only_file
from scraping.spiders.poland_rjps import PolandRJPSSpider, CategoryHandler
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


class TestPolandRJPSSpider:
    def test_parse_name(self, normal_place):
        name = PolandRJPSSpider().parse(normal_place, category='test').get('name')
        assert name == 'Miejski Ośrodek Pomocy Społecznej w Zabłudowie'

    def test_parse_address(self, normal_place):
        address = PolandRJPSSpider().parse(normal_place, category='test').get('address')

        assert address == '16-060 Zabłudów ul. Rynek 8'

    def test_parse_email(self, normal_place):
        description = PolandRJPSSpider().parse(normal_place, category='test').get('description')
        assert 'biuro@mops-zabludow.pl' in description

    def test_parse_phone(self, normal_place):
        description = PolandRJPSSpider().parse(normal_place, category='test').get('description')
        assert 'tel. 85 7188100' in description

    def test_parse_website(self, normal_place):
        description = PolandRJPSSpider().parse(normal_place, category='test').get('description')
        assert 'http://bip.mops.um.zabludow.wrotapodlasia.pl' in description

    def test_parse_update_date(self, normal_place):
        description = PolandRJPSSpider().parse(normal_place, category='test').get('description')
        assert 'data aktualizacji: 2018-02-05' in description

    def test_parse_missing_info_page(self, missing_info_place):
        description = PolandRJPSSpider().parse(missing_info_place, category='test').get('description')
        assert 'data aktualizacji: 2013-12-13' in description

    def get_spider(self):
        class StubPolandRJPSSpider(PolandRJPSSpider):
            DETAIL_BASE_URL = 'https://test.com/?id'

            def _open_file(self, file_name):
                mapping = {
                    'foo.json': [{"id": 2321, "x": 18.59832, "y": 52.55788},
                                 {"id": 2354, "x": 18.49855, "y": 52.998119}],
                    'bar.json': [{"id": 2333, "x": 18.59832, "y": 52.55788},
                                 {"id": 2336, "x": 18.49855, "y": 52.998119}]
                }
                return mapping.get(file_name, [])

        return StubPolandRJPSSpider()

    def test_build_url_from_one_file(self):
        spider = self.get_spider()
        urls = spider._build_urls(['foo.json'])
        assert urls == ['https://test.com/?id=2321', 'https://test.com/?id=2354']

    def test_build_url_from_more_files(self):
        spider = self.get_spider()
        urls = spider._build_urls(['foo.json', 'bar.json'])
        assert urls == ['https://test.com/?id=2321', 'https://test.com/?id=2354',
                        'https://test.com/?id=2333', 'https://test.com/?id=2336']


class TestCategoryHandler:
    def get_handler(self, data):
        class StubCategoryHandler(CategoryHandler):
            GET_MAPPING_TIMES = 0

            def get_mapping(self):
                self.GET_MAPPING_TIMES += 1
                return super().get_mapping()

        return StubCategoryHandler(data)

    def test_single_category(self):
        data = {'Medical': ['https://foo.com/123', 'https://foo.com/126']}
        handler = self.get_handler(data)
        assert handler.get_mapping() == {'https://foo.com/123': {'Medical'}, 'https://foo.com/126': {'Medical'}}

    def test_two_categories(self):
        data = {
            'Medical': ['https://foo.com/123', 'https://foo.com/126'],
            'Children': ['https://foo.com/123', 'https://foo.com/129']}
        handler = self.get_handler(data)
        assert handler.get_mapping() == {'https://foo.com/123': {'Medical', 'Children'},
                                         'https://foo.com/126': {'Medical'},
                                         'https://foo.com/129': {'Children'}, }

    def test_two_categories_duplicated_urls(self):
        data = {
            'Medical': ['https://foo.com/123', 'https://foo.com/126', 'https://foo.com/126'],
            'Children': ['https://foo.com/123', 'https://foo.com/129']}
        handler = self.get_handler(data)
        assert handler.get_mapping() == {'https://foo.com/123': {'Medical', 'Children'},
                                         'https://foo.com/126': {'Medical'},
                                         'https://foo.com/129': {'Children'}, }

    def test_three_categories(self):
        data = {
            'Medical': ['https://foo.com/123', 'https://foo.com/126'],
            'Children': ['https://foo.com/123', 'https://foo.com/129'],
            'People with disabilities': ['https://foo.com/133', 'https://foo.com/129']}
        handler = self.get_handler(data)
        assert handler.get_mapping() == {'https://foo.com/123': {'Medical', 'Children'},
                                         'https://foo.com/126': {'Medical'},
                                         'https://foo.com/129': {'Children', 'People with disabilities'},
                                         'https://foo.com/133': {'People with disabilities'}}

    def test_get_category_by_url(self):
        data = {'Medical': ['https://foo.com/123', 'https://foo.com/126']}
        handler = self.get_handler(data)
        assert handler.get_categories_by_url('https://foo.com/123') == 'Medical'

    def test_get_categories_by_url(self):
        data = OrderedDict({'Medical': ['https://foo.com/123', 'https://foo.com/126'],
                            'Children': ['https://foo.com/123']})
        handler = self.get_handler(data)
        categories = handler.get_categories_by_url('https://foo.com/123')
        assert 'Children' in categories
        assert 'Medical' in categories

    def test_build_mapping_once(self):
        data = {'Medical': ['https://foo.com/123', 'https://foo.com/126']}
        handler = self.get_handler(data)
        handler.get_categories_by_url('https://foo.com/123')
        handler.get_categories_by_url('https://foo.com/123')
        assert handler.GET_MAPPING_TIMES == 1
