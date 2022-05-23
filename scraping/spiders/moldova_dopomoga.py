import re

from typing import List, Tuple, Union

from scrapy import Spider, Selector
from scrapy.http import Response


BASE_ADDRESS_PATTERN = r"(s.\s|str.\s|bd.\s?|sat.\s|satul\s|com.\s|z.\s)(\d{0,10})(\D+)"
ADDRESS_CHECK_PATTERN = rf"{BASE_ADDRESS_PATTERN}(,|\d|\(|$)"
ADDRESS_PATTERN1 = r"(s.\s)(.+)(,\sstr.\s)(\D+)([\d\w/]+)"
ADDRESS_PATTERN2 = rf"{BASE_ADDRESS_PATTERN}(,|\()"
ADDRESS_PATTERN3 = rf"{BASE_ADDRESS_PATTERN}(,|[\d\w/]+|\()"
KNOWN_STREETS = {'Hristo Botev'}
VENUE_PREFIXES = {'IP', 'Centrul', 'Complexul', 'Biserica'}


def clean(value: str) -> str:
    value = re.sub(r"\s{2,10}", " ", value)
    return value.replace("\r\n", "").strip()


def clean_punctuation(value: str) -> str:
    return value.strip().replace(",", "").replace("(", "").replace(")", "").strip()


def strip_punctuation(value: str) -> str:
    value = value.strip()

    for punctuation in [",", "(", ")"]:
        if value.startswith(punctuation):
            value = value[1:]

        if value.endswith(punctuation):
            value = value[:-1]

    return value.strip()


def parse_details(details: str, city: str = None) -> Tuple[str, str]:
    # clear the city name from details
    if city:
        details = re.sub(rf"(mun|or|orașul)(.)(\s?)({city})", "", details).replace(city, "")

    # add prefixes to known streets
    for street in KNOWN_STREETS:
        if street in details:
            details = details.replace(street, f"s. {street}")

    # try to find address
    address = find_address(details)
    if address:
        parts = sorted(details.split(address), key=lambda x: -len(x))
        name = clean_punctuation(parts[0])
        address = strip_punctuation(address)
        return name or address, address

    # try to find venue
    venue = find_venue(details)
    if venue:
        parts = sorted(details.split(venue), key=lambda x: -len(x))
        name = clean_punctuation(venue)
        address = strip_punctuation(parts[0])
        return name, address or name


    parts = details.split(',', 1)
    if len(parts) == 1:
        value = clean(parts[0])
        return value, value

    name, address = [clean_punctuation(part) for part in parts]

    return name or address, address or name


def find_address(details: str) -> Union[str, None]:
    match = re.search(ADDRESS_CHECK_PATTERN, details, re.I)
    if not match:
        return

    address = match.group()
    if address.endswith(","):
        return address

    for pattern in [ADDRESS_PATTERN1, ADDRESS_PATTERN2, ADDRESS_PATTERN3]:
        match = re.search(pattern, details, re.I)
        if match:
            address = match.group()
            venue_prefix = find_venue_prefix(address)
            if venue_prefix:
                address = address.split(venue_prefix)[0]
            return address


def find_venue_prefix(details: str) -> Union[str, None]:
    for prefix in VENUE_PREFIXES:
        if prefix in details:
            return prefix


def find_venue(details: str) -> Union[str, None]:
    venue_prefix = find_venue_prefix(details)
    if venue_prefix:
        name = sorted(details.split(venue_prefix), key=lambda x: -len(x))[0]
        return f"{venue_prefix}{name}"


class DopomogaSpider(Spider):
    name = "dopomoga"
    start_urls = [
        'https://dopomoga.gov.md/akkreditovannye-centry-dlya-bezhencev/'
    ]

    def parse(self, response: Response):
        rows: List[Selector] = response.css('.ty-wysiwyg-content table tr')
        for row in rows[1:]:
            _, city, details, capacity = [clean(cell) for cell in row.css('td::text').getall()]

            name, address = parse_details(details, city=city)

            point = {
                "name": name,
                "country": "Moldova",
                "city": city,
                "address": f"Republica Moldova, {city}, {address}",
                "categories": "Accommodation",
                "description": f"Capacity: {capacity}",
                "organizations": "",
                "lat": "",
                "lng": "",
            }

            yield point
