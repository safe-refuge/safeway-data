from typing import List

import scrapy

CATEGORY_MAPPING = {
    'Seniors': {'category': 'Medical', 'ids_file': 'seniors.json'},
    'Family': {'category': 'Children', 'ids_file': 'family.json'}
}


class QuotesSpider(scrapy.Spider):
    name = "poland_rjps"

    def start_requests(self):
        for key, value in CATEGORY_MAPPING.items():
            for url in self._build_urls(value['ids_file']):
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=value)

    def _build_urls(self, file_name: str) -> List[str]:
        raise NotImplemented

    def parse(self, response):
        raise NotImplemented
