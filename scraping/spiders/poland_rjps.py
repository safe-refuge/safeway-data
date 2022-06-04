from collections import defaultdict
from typing import List, Dict

import scrapy
import json

from joblib import Memory
from config.settings import Settings

memory = Memory(location='cache/poland_rjps')
settings = Settings()
DATA_PATH = f'{settings.spider_data_path}/rips'
COUNTRY_NAME = 'Poland'
DEFAULT_CATEGORY = "Any Help"

CATEGORY_MAPPING = {
    'Medical': [f'{DATA_PATH}/seniors.json'],
    'Children': [f'{DATA_PATH}/family.json', f'{DATA_PATH}/children_and_youth.json'],
    'Disability support': [f'{DATA_PATH}/people_with_disabilities.json'],
}


class PolandRJPSSpider(scrapy.Spider):
    name = "poland_rjps"
    DETAIL_BASE_URL = 'https://rjps.mpips.gov.pl/RJPS/WJ/wyszukiwanie/pobierzDaneJednostki.do?jednostkiIds'

    def start_requests(self):
        data = {category: self._build_urls(file_name) for category, file_name in CATEGORY_MAPPING.items()}
        handler = CategoryHandler(data)

        for _, file_name in CATEGORY_MAPPING.items():

            @memory.cache
            def cached_request_with_url(url: str):
                return scrapy.Request(url=url, callback=self.parse,
                                      cb_kwargs={'category': handler.get_categories_by_url(url)})

            for url in self._build_urls(file_name):
                yield cached_request_with_url(url=url)

    def _build_urls(self, file_names: List[str]) -> List[str]:
        data = [self._open_file(file_name) for file_name in file_names]
        ids = [item for sublist in data for item in sublist]
        return [f'{self.DETAIL_BASE_URL}={value["id"]}' for value in ids]

    def _open_file(self, file_name):
        return open_json_file(file_name)

    def parse(self, response, category: str):
        return {
            'name': self._get_name(response),
            'country': COUNTRY_NAME,
            'city': '',
            'address': self._get_address(response),
            'lat': '',
            'lng': '',
            'category': category or DEFAULT_CATEGORY,
            'organizations': '',
            'description': self._get_description(response)
        }

    def _get_name(self, response):
        raw = response.css('h3.nazwa a::text').get()
        return self._clean_spaces(raw)

    def _clean_spaces(self, data):
        return data.strip()

    def _get_address(self, response):
        lines = response.css('div > div > div.flex.flex-column.justify-content-center span::text').getall()
        return ''.join(lines)

    def _get_description(self, response):
        rows = [self._get_email(response),
                self._get_phone(response),
                self._get_website(response),
                self._get_update_date(response)]

        return '\n'.join(map(self._clean_spaces, rows))

    def _get_email(self, response):
        return response.css('div[title=Email] > div > div::text').get() or ''

    def _get_phone(self, response):
        return response.css('div[title=Telefon] > div > span.wrap-anywhere::text').get() or ''

    def _get_website(self, response):
        return response.css('div[title="Strona www"] > div > div::text').get() or ''

    def _get_update_date(self, response):
        return self._clean_spaces(response.css('body > div > div > div > div.data-aktualizacji::text').get()) or ''


def open_json_file(file_name: str) -> dict:
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


class CategoryHandler:
    def __init__(self, data: Dict[str, List[str]]):
        self.data = data
        self.mapping = self.get_mapping()

    def get_mapping(self):
        mapping = defaultdict(set)
        for category, urls in self.data.items():
            for url in urls:
                mapping[url].add(category)
        return mapping

    def get_categories_by_url(self, url: str) -> str:
        return ','.join(list(self.mapping[url]))
