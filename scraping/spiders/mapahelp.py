import logging

import scrapy

from config.constants import DEFAULT_CATEGORY


log = logging.getLogger(__name__)


CATEGORIES = {
    "Finance": "Finance",
    "Food": "Food",
    "Health": "Medical",
    "Housing": "Accommodation",
    "Humanitarian Aid": "Any help",
    "Kennels": "Pets",
    "Psychological Help": "Mental help",
    "Shelter": "Accommodation",
    "Sports": "Any help",
    "Transfer": "Transport",
    "Other Help": "Any help",
}


class MapaHelpSpider(scrapy.Spider):
    """
    MapaHelp crawler.
    """

    name = "mapahelp"
    allowed_domains = ["cloudfront.net"]
    start_urls = [
        "https://d2916ie68qiajx.cloudfront.net/mapka/organizations",
    ]

    def parse(self, response):
        for point in response.json()["result"]:
            if not point["Published"]:
                log.info("Point not published: %s", point["Name"])
                continue

            description = build_description(point)
            yield {
                "country": point["Country"],
                "name": point["Name"],
                "city": "",
                "address": point.get("Address", ""),
                "lat": point["Lat"],
                "lng": point["Lng"],
                "phone": point.get("Phone", ""),
                "email": point.get("Email", ""),
                "url": point.get("Website", ""),
                "open_hours": point.get("WorkTime", ""),
                "categories": [CATEGORIES.get(point["CategoryEn"],
                                              DEFAULT_CATEGORY)],
                "organizations": [],
                "description": "\n".join(description),
            }


def build_description(point):
    description = []
    if point.get("Services"):
        description.append(point["Services"])
    if point.get("SocialNetworks"):
        description.append(f"Social networks: {point['SocialNetworks']}")
    return description
