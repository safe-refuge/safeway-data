import re
import logging

import scrapy

from config.constants import DEFAULT_CATEGORY


log = logging.getLogger(__name__)


SOCIAL_PATTERNS = [
    ("messenger", re.compile(r"(https://www\.facebook\.com/[^,;\s]+)")),
    ("telegram", re.compile(r"(https://t\.me/[^,;\s]+)")),
    ("telegram", re.compile(
        r"(?:telegram|телеграм)[-:\s]*@?([_+a-z0-9]+)", flags=re.I)),
    ("telegram", re.compile(
        r"@?([_+a-z0-9]+)[-\s]*(?:\(telegram|телеграм\))", flags=re.I)),
    ("whatsapp", re.compile(
        r"(?:whatsapp|вотсап|ватсап|вацап)[-:\s]*@?([-_+a-z0-9]+)",
        flags=re.I)),
    ("whatsapp", re.compile(
        r"@?([-_+a-z0-9]+)[-\s]*(?:\(whatsapp|вотсап|ватсап|вацап\))",
        flags=re.I)),
]


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


def extract_social(txt):
    known = {}
    unknown = []
    for line in txt.splitlines():
        found = None
        for medium, pattern in SOCIAL_PATTERNS:
            found = re.search(pattern, line)
            if found:
                value, = found.groups()
                known[medium] = value
        if not found:
            if line.strip():
                unknown.append(line.strip())

    return known, unknown


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

            known_social, unknown_social = extract_social(
                point.get("SocialNetworks", ""))

            poi = {
                "country": point["Country"],
                "name": point["Name"],
                "city": "",
                "address": point.get("Address", ""),
                "lat": point["Lat"],
                "lng": point["Lng"],
                "phone": point.get("Phone", ""),
                "email": point.get("Email", ""),
                "url": point.get("Website", ""),
                "socialmedia": "\n".join(unknown_social),
                "open_hours": point.get("WorkTime", ""),
                "categories": [CATEGORIES.get(point["CategoryEn"],
                                              DEFAULT_CATEGORY)],
                "organizations": [],
                "description": point.get("Services", ""),
            }

            for medium, value in known_social.items():
                point[medium] = value

            yield poi
