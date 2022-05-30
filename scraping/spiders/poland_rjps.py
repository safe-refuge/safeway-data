from typing import List

import scrapy
import json

DATA_PATH = 'data/spiders/rips/'
CATEGORY_MAPPING = {
    'Seniors': {'category': 'Medical', 'ids_file': f'{DATA_PATH}seniors.json'},
    'Family': {'category': 'Children', 'ids_file': f'{DATA_PATH}family.json'}
}

DETAIL_BASE_URL = 'https://rjps.mpips.gov.pl/RJPS/WJ/wyszukiwanie/pobierzDaneJednostki.do?jednostkiIds'


class QuotesSpider(scrapy.Spider):
    name = "poland_rjps"

    def start_requests(self):
        for key, value in CATEGORY_MAPPING.items():
            for url in self._build_urls(value['ids_file']):
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'category': value['category']})

    def _build_urls(self, file_name: str) -> List[str]:
        ids = open_json_file(file_name)
        return [f'{DETAIL_BASE_URL}={value["id"]}' for value in ids]

    def parse(self, response, category: str):
        import pdb;
        pdb.set_trace()
        raise NotImplemented


def open_json_file(file_name: str) -> dict:
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data
