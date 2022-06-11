import logging

import scrapy

from config.constants import DEFAULT_CATEGORY


log = logging.getLogger(__name__)


CATEGORIES = {
    "Finance": "Finance",
    "Food": "Food",
    "Health": "Medical",
    "Housing": "Accommodation",
    "Humanitarian Aid": "Food",
    "Kennels": "Pets",
    "Psychological Help": "Mental help",
    "Shelter": "Accommodation",
    "Sports": "Any help",
    "Transfer": "Transport",
    "Other Help": "Any help",
}

COUNTRIES = {
    "Австралія": "Australia",
    "Австрія": "Austria",
    "Аландські острови": "Aland Islands",
    "Англія": "UK",
    "Аргентина": "Argentina",
    "Бельгія": "Belgium",
    "Білорусь": "Belarus",
    "Болгарія": "Bulgaria",
    "Бразилія": "Brazil",
    "Великобританія": "UK",
    "Греція": "Greece",
    "Грузiя": "Georgia",
    "Данія": "Denmark",
    "Естонія": "Estonia",
    "Ізраїль": "Israel",
    "Індія": "India",
    "Ірландія": "Ireland",
    "Іспанія": "Spain",
    "Італія": "Italy",
    "Казахстан": "Kazakhstan",
    "Канада": "Canada",
    "Киргизстан": "Kyrgyzstan",
    "Кіпр": "Cyprus",
    "Косово": "Kosovo",
    "Латвія": "Latvia",
    "Литва": "Lithuania",
    "Люксембург ": "Luxembourg",
    "Мексика": "Mexico",
    "Молдова ": "Moldova",
    "Нідерланди": "Netherlands",
    "Німеччина": "Germany",
    "Норвегія": "Norway",
    "ОАЕ": "UAE",
    "Оман": "Oman",
    "Перу": "Peru",
    "Південна Корея": "Korea",
    "Північна Ірландія": "North Ireland",
    "Північна Македонія": "North Macedonia",
    "Польща": "Poland",
    "Португалія": "Portugal",
    "Росія": "Russia",
    "Румунія": "Romania",
    "Сербія": "Serbia",
    "Словаччина": "Slovakia",
    "Словенія": "Slovenia",
    "США": "USA",
    "Туреччина": "Turkey",
    "Угорщина": "Hungary",
    "Узбекистан": "Uzbekistan",
    "Україна": "Ukraine",
    "Фінляндія": "Finland",
    "Франція": "France",
    "Хорватія": "Croatia",
    "Чехія": "Czechia",
    "Чилі": "Chile",
    "Чорногорія": "Montenegro",
    "Швейцарія ": "Switzerland",
    "Швеція": "Sweden",
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
            if point["Country"] not in COUNTRIES:
                log.error("Unknown country: %s", point["Country"])

            yield {
                "country": COUNTRIES[point["Country"]],
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
