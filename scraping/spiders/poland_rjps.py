from typing import List

import scrapy
import json

from joblib import Memory
from config.settings import Settings

memory = Memory(location='cache/poland_rjps')
settings = Settings()
DATA_PATH = f'{settings.spider_data_path}/rips/'

CATEGORY_MAPPING = {
    'Seniors': {'category': 'Medical', 'ids_file': f'{DATA_PATH}seniors.json'},
    'Family': {'category': 'Children', 'ids_file': f'{DATA_PATH}family.json'}
}

DETAIL_BASE_URL = 'https://rjps.mpips.gov.pl/RJPS/WJ/wyszukiwanie/pobierzDaneJednostki.do?jednostkiIds'


class QuotesSpider(scrapy.Spider):
    name = "poland_rjps"

    def start_requests(self):

        for key, value in CATEGORY_MAPPING.items():
            category = value['category']

            @memory.cache
            def cached_request_with_url(url: str):
                return scrapy.Request(url=url, callback=self.parse, cb_kwargs={'category': category})

            for url in self._build_urls(value['ids_file']):
                yield cached_request_with_url(url=url)

    def _build_urls(self, file_name: str) -> List[str]:
        ids = open_json_file(file_name)
        return [f'{DETAIL_BASE_URL}={value["id"]}' for value in ids]

    def parse(self, response, category: str):
        return {
            'name': self._get_name(response)
        }

    def _get_name(self, response):
        raw = response.css('h3.nazwa a::text').get()
        return self._clean_spaces(raw)

    def _clean_spaces(self, data):
        return data.strip()


def open_json_file(file_name: str) -> dict:
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data
