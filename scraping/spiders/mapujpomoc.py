import logging

import scrapy

from config.constants import DEFAULT_CATEGORY


CATEGORIES = {
    "food": "Food",
    "food for animals": "Food",
    "accommodation": "Accommodation",
    "assistant for people with disabilities": "Disability support",
    "clothing": "Clothes",
    "computer equipment": "Electronics",
    "disability": "Disability support",
    "doctor": "Medical",
    "education": "Education",
    "housing": "Accommodation",
    "information": "Information",
    "job search assistance": "Jobs",
    "financial support": "Finance",
    "lgbt+": "LGBTQ+",
    "logistics": "Transport",
    "medical / rehabilitation equipment": "Medical",
    "medicines, dressing materials": "Pharmacy",
    "excluded or discriminated groups": "LGBTQ+",
    "provision / sharing of rooms": "Accommodation",
    "psychological support": "Mental help",
    "psychologist": "Mental help",
    "rehabilitation and physiotherapy": "Medical",
    "sleeping bags, mats, tents": "Accommodation",
    "toys": "Children",
    "transportation": "Transport",
    "water, sanitary facilities, hygiene": "Water",
    "afterschool activities for children": "Children",
    "counteracting sexual violence and human trafficking": "Social help",
    "flashlights, batteries, chargers, power banks": "Electronics",
    "polish language classes": "Education",
    "training workshops for teachers or teaching assistants": "Education",
    "hygiene products (soap, diapers, personal hygiene)": DEFAULT_CATEGORY,
    "blankets, sheets, towels": DEFAULT_CATEGORY,
}


log = logging.getLogger(__name__)


class MapujpomocSpider(scrapy.Spider):
    """
    Mapuj Pomoc crawler.
    """

    name = "mapujpomoc"
    allowed_domains = ["mapujpomoc.pl"]
    start_urls = [
        "https://mapujpomoc.pl/en/map/",
    ]
    download_delay = 5

    def parse(self, response, **kwargs):
        for basic in parse_points(response):
            yield response.follow(
                basic["url"],
                callback=parse_details_page, cb_kwargs={
                    "basic": basic,
                })


def parse_points(response):
    blocks = response.css(".listing .item")
    for block in blocks:
        direction = block.css(".row .colitem .badge ::text").get().lower()
        if direction != "i offer help":
            logging.debug("Place does not offer help")
            continue
        yield parse_point(block)


def parse_point(block):
    phone = block.css("a[title='Numer telefonu'] ::text").get()
    email = block.css("a[title='Adres email'] ::text").get()
    basic = {
        "country": "Poland",
        "name": block.css("h4 span.pe-2 ::text").get().strip(),
        "lat": block.css("::attr(data-lat)").get(),
        "lng": block.css("::attr(data-lng)").get(),
        "phone": phone.strip() if phone else "",
        "email": email.strip() if email else "",
        "url": block.css("a.btn-more ::attr(href)").get(),
    }
    return basic


def parse_details_page(response, basic={}):
    blocks = response.css(".place-information .item")
    details = {
        "categories": [],
        "organizations": [],
        "tags": [],
    }

    headers = {
        "country": ("country", parse_text),
        "city": ("city", parse_text),
        "street name and number": ("address", parse_text),
        "email": ("email", parse_text),
        "phone number": ("phone", parse_text),
        "organisation website": ("url", parse_link),
        "fundraiser website / website detailing your activities": (
            "socialmedia", parse_link),
        "type of material or in-kind aid offered": (
            "categories", parse_categories),
        "type of services offered": (
            "categories", parse_categories),
        "your organisation’s scope of operations": (
            "categories", parse_categories),
        "description of activities": ("description", parse_text),
    }

    for block in blocks:
        header = block.css(".label ::text").get().strip().lower()
        if header not in headers:
            continue
        key, extractor = headers[header]
        value = extractor(block)
        if key in details:
            details[key] += value
        else:
            details[key] = value

    details['categories'] = list(set(details['categories']))

    return {**basic, **details}


def parse_text(element):
    return element.css("li ::text").get().strip()


def parse_link(element):
    return element.css("a ::attr('href')").get()


def parse_categories(element):
    categories = element.css("li span ::text").getall()
    return [CATEGORIES.get(c.lower(), DEFAULT_CATEGORY) for c in categories]
