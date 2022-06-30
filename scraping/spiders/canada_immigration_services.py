import re
import logging

import scrapy
import hjson

from config.constants import DEFAULT_CATEGORY


log = logging.getLogger(__name__)


CATEGORIES = {
    "help_gar": "Accommodation",
    "lgbtq2": "LGBTQ+",
    "youth": "Children",
    "general": "Any help",
    "other": "Any help",
    "job_lang_training": "Education",
    "job_search": "Jobs",
}

# Ref: https://ircc.canada.ca/js/tools/services/closest-services.js
SERVICES = {
    "Lang_assess": "Language assessment",
    "Lang_training": "Language training (general)",
    "Job_lang_training": "Job-specific language training",
    "General": "Help with daily life",
    "Job_search": "Help finding a job",
    "Citzenship_test_prep": "Help preparing for the citizenship test",
    "Volunteer": "Find or become a mentor to a newcomer",
    "Help_gar": "Services for refugees",
    "Franco": "Francophone service provider",
    "EngFra": "Help in English and in French",
    "Women": "Services for women",
    "Seniors": "Services for seniors",
    "Youth": "Services for youth",
    "LGBTQ2": "Services for LGBTQ2",
    "Other": "Other Services",
}


class CanadaImmigrationServicesSpider(scrapy.Spider):
    """
    Canada IRCC crawler.
    """

    name = "canada_immigration_services"
    allowed_domains = ["ircc.canada.ca"]
    start_urls = [
        "https://ircc.canada.ca/js/tools/services/services-info.js",
    ]

    def parse(self, response, **kwargs):
        points = parse_response(response)
        for point in points:
            if point.get("Services", {}).get("Help_gar") != "yes":
                log.debug("Skippint point %s", point["Type"]["en"])
                continue
            relevant_categories, other_categories = build_categories(point)
            description = build_description(point, other_categories)
            yield {
                "country": "Canada",
                "name": point["Type"]["en"],
                "city": point["City"]["en"],
                "address": f"Canada, {point['Province']['en']}, "
                           f"{point['City']['en']}, {point['Address']['en']}",
                "categories": relevant_categories,
                "description": "\n".join(description),
                "organizations": ["Canada IRCC"],
                "lat": point["Coordinates"]["Latitude"],
                "lng": point["Coordinates"]["Longitude"],
                "phone": point.get("Telephone", {}).get("en", ""),
                "email": point.get("Email", {}).get("en", ""),
            }


def parse_response(response):
    regexp = re.compile(r"\*\/\s*var ServicesData = (\[.*\]);", re.S)
    json_str, = re.search(regexp, response.text).groups()
    return hjson.loads(json_str)


def build_categories(point):
    relevant = []
    other = []
    for name, available in point["Services"].items():
        if available != "yes":
            continue
        cat = CATEGORIES.get(name)
        if cat:
            relevant.append(cat)
        else:
            other.append(SERVICES[name])
    if not relevant:
        relevant = [DEFAULT_CATEGORY]
    return relevant, other


def build_description(point, other_categories):
    description = []
    if point.get("Note", {}).get("en"):
        description.append(f"{point['Note']['en']}")
    if other_categories:
        description.append(f"Other services: " + ", ".join(other_categories))
    return description
