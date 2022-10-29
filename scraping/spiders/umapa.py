import logging

import scrapy

from config.constants import DEFAULT_CATEGORY


# Ref: https://www.mapotic.com/api/v1/maps/10392/public-categories/
CATEGORIES = {
    "Education": "Education",
    "Psychological help": "Mental help",
    "Legal services": DEFAULT_CATEGORY,
    "Translators": DEFAULT_CATEGORY,
    "Integration": DEFAULT_CATEGORY,
    "Food": "Food",
    "Institutions": DEFAULT_CATEGORY,
    "Leisure activities": DEFAULT_CATEGORY,
    "Doctors": "Medical",
    "Transport": "Transport",
    "Other": DEFAULT_CATEGORY,
}

HEADERS = {
    "Accept": "application/json",
}


log = logging.getLogger(__name__)


class UmapaSpider(scrapy.Spider):
    """
    Umapa crawler.
    """

    name = "umapa"
    allowed_domains = ["umapa.eu", "www.mapotic.com"]
    start_urls = [
        "https://www.mapotic.com/api/v1/maps/10392/pois.geojson/?",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)

    def parse(self, response):
        for point in get_points_list(response):
            url = get_point_url(point)
            yield response.follow(url, callback=build_point, headers=HEADERS)


def get_points_list(response):
    for point in response.json()["features"]:
        if not point["properties"]["is_published"]:
            log.info("Point not published: %s", point["properties"]["id"])
            continue

        yield point


def get_point_url(point):
    url = "https://www.mapotic.com/api/v1/maps/10392/public-pois/{}/"
    return url.format(point["properties"]["id"])


def build_point(response):
    point = response.json()
    lat, lng = point["point"]["coordinates"]
    cat = CATEGORIES.get(point["category"]["name"]["en"], DEFAULT_CATEGORY)
    return {
        "country": "",
        "city": "",
        "name": point["name"],
        "address": get_attr(point, "Address"),
        "lat": lat,
        "lng": lng,
        "phone": get_attr(point, "Phone"),
        "email": get_attr(point, "E-mail"),
        "url": get_attr(point, "Web"),
        "open_hours": get_attr(point, "Opening hours"),
        "categories": [cat],
        "organizations": [],
        "tags": [],
        "description": get_attr(point, "Description"),
    }


def get_attr(point, name):
    for attr in point["attributes_values"]:
        if attr["attribute"]["name"]["en"] == name:
            return get_attr_value(attr)
    return ""


def get_attr_value(attr):
    if attr["attribute"]["attribute_type"] in ["multiple_select"]:
        return [
            attr["attribute"]["settings"]["choices"][v]["en"]
            for v in attr["value"]
        ]
    elif attr["attribute"]["attribute_type"] in ["select"]:
        return attr["attribute"]["settings"]["choices"][attr["value"]]["en"]
    else:
        return attr["value"].replace(" 🇺🇦", "\n").replace("🇨🇿", "")
