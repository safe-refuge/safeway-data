from typing import List

from scrapy import Spider, Selector
from scrapy.http import Response


class DopomogaSpider(Spider):
    name = "dopomoga"
    start_urls = [
        'https://dopomoga.gov.md/akkreditovannye-centry-dlya-bezhencev/'
    ]

    def parse(self, response: Response):
        rows: List[Selector] = response.css('.ty-wysiwyg-content table tr')
        for row in rows[1:]:
            _, city, details, capacity = row.css('td::text').getall()
            name, address = details.split(',')
            yield {
                "name": self.clean(name),
                "country": "Moldova",
                "city": self.clean(city),
                "address": self.clean(address),
                "lat": "",
                "lng": "",
                "categories": "Accommodation",
                "organizations": "",
                "description": ""
            }

    def clean(self, name: str) -> str:
        return name.replace("\r\n", "").strip()
