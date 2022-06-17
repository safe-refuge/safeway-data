from collections import defaultdict
from typing import List, Dict, Mapping
import requests
import scrapy
import json

from joblib import Memory

from config.constants import DEFAULT_CATEGORY
from config.settings import Settings
from services.geocoding import Point
from utils.phone_numbers import PolandPhoneNumberExtractorService



memory = Memory(location='cache/poland_rjps')
settings = Settings()
COUNTRY_NAME = 'Poland'


CATEGORY_MAPPING = {
    'Medical': ['21,22,23,24,20,19', '25,26,27,28,29,30'],
    'Children': ['16,13,17,18,14,15', '3,4,1,2,5,6'],
    'Disability support': ['7,8,9,10,11,12'],
    'Mental help': ['31,32,33,34'],
    'Social help': ['41,45,42,43,44'],
    'Finance': ['35,36,37,38,39,40']
}


class PolandRJPSSpider(scrapy.Spider):
    name = "poland_rjps"
    DETAIL_BASE_URL = 'https://rjps.mpips.gov.pl/RJPS/WJ/wyszukiwanie/pobierzDaneJednostki.do?jednostkiIds'
    coordinates: Mapping[str, Point] = {}
    descriptions: List[str] = []

    def start_requests(self):
        data = {category: self._build_urls(category_ids) for category, category_ids in CATEGORY_MAPPING.items()}
        handler = CategoryHandler(data)

        for url, _ in handler.mapping.items():
            categories = handler.get_categories_by_url(url)

            @memory.cache
            def cached_request_with_url(url: str):
                return scrapy.Request(url=url, callback=self.parse,
                                      cb_kwargs={'category': categories})

            yield cached_request_with_url(url=url)

    def _build_urls(self, category_ids: List[str]) -> List[str]:
        data = [self._fetch_point_ids_by_category(category_id_group) for category_id_group in category_ids]
        ids = [item for sublist in data for item in sublist]
        for item in ids:
            point = Point(item['y'], item['x'])
            self.coordinates.update({self._get_url_by_id(item['id']): point})
        return [self._get_url_by_id(item['id']) for item in ids]

    def _get_url_by_id(self, entity_id: str):
        return f'{self.DETAIL_BASE_URL}={entity_id}'

    def _fetch_point_ids_by_category(self, category_id_group: str):
        return fetch_point_ids_by_category(category_id_group)

    def parse(self, response, category: str):
        return {
            'name': self._get_name(response),
            'country': COUNTRY_NAME,
            'city': '',
            'address': self._get_address(response),
            'lat': self._get_lat(response),
            'lng': self._get_lng(response),
            'categories': [category or DEFAULT_CATEGORY],
            'organizations': [],
            'phone': self._get_phone(response),
            'description': self._get_description(response),
            'email': self._get_email(response),
            'url': self._get_website(response),
        }

    def _get_name(self, response):
        raw = response.css('h3.nazwa a::text').get()
        return self._clean_spaces(raw)

    def _clean_spaces(self, data):
        return data.strip()

    def _get_address(self, response):
        lines = response.css('div > div > div.flex.flex-column.justify-content-center span::text').getall()
        return ''.join(lines)

    def _get_lat(self, response):
        return self.coordinates.get(response.url).lat

    def _get_lng(self, response):
        return self.coordinates.get(response.url).lng

    def _get_description(self, response):
        self.descriptions.append(self._get_update_date(response))
        return '\n'.join(map(self._clean_spaces, self.descriptions))

    def _get_email(self, response):
        return response.css('div[title=Email] > div > div::text').get() or ''

    def _get_phone(self, response):
        raw = response.css('div[title=Telefon] > div > span.wrap-anywhere::text').get() or ''
        return self._clean_phone(raw)

    def _clean_phone(self, phone: str) -> str:
        service = PolandPhoneNumberExtractorService(phone)
        phones = service.get_phone_number_in_e164()
        if len(phones) > 1:
            self.descriptions.append(f'Other phone numbers: {", ".join(phones[1:])}')
        return phones[0]

    def _get_website(self, response):
        url = response.css('div[title="Strona www"] > div > div::text').get() or ''
        return url.strip()

    def _get_update_date(self, response):
        data = self._clean_spaces(response.css('body > div > div > div > div.data-aktualizacji::text').get()) or ''
        return data.replace('data aktualizacji', 'updated')


@memory.cache
def fetch_point_ids_by_category(category_id_group: str) -> dict:
    url = "https://rjps.mpips.gov.pl/RJPS/WJ/wyszukiwanie/zaladujDane.do"
    payload = json.dumps({
        "filtry": {
            "miejscowosc": "",
            "wojewodztwo": "",
            "powiat": "",
            "gmina": "",
            "odleglosc": 0,
            "lokalizacja": "",
            "szukanaFraza": "",
            "podkategorie": category_id_group,
            "stronaListy": 1,
            "liczbaPozycjiLista": "20",
            "wersja": "1",
            "widocznyPanel": "mapa",
            "wejscieKarta": "",
            "idJednostki": ""
        },
        "stronaListy": 1
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


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
