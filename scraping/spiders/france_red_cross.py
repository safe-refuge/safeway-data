import re
import logging

import scrapy


log = logging.getLogger(__name__)


CATEGORIES = {
    'domicile': 'Accommodation',
    'enfants & familles': 'Children',
    'personnes handicapees': 'Disability support',
    "lutte contre l'exclusion": 'Social help',
    'sanitaire': 'Medical',
}

SERVICES_TO_CATEGORIES = {
    'aide alimentaire': 'Food',
    'aides financières': 'Finance',
    'textile & bric-à-brac': 'Clothes',
    'accès aux soins et bien être': 'Medical',
    'accueil et orientation': 'Accommodation',
    'accueil famille-enfant': 'Children',
    'espace bébé parents': 'Children',
    'dynamique jeunesse': 'Children',
    'point hygiène': 'Medical',
    'postes de secours': 'Any help',

}

DEFAULT_CATEGORY = 'Any Help'


class FranceRedCrossSpider(scrapy.Spider):
    """
    Red Cross France crawler.

    .. note::
        Website seems to block access to some of its pages
        from certain locations.
        A way to tunnel the traffic through other locations
        (Europe, U.S. seem to work well) may be needed.
    """

    name = 'france_red_cross'
    allowed_domains = ['croix-rouge.fr']
    start_urls = [
        'https://www.croix-rouge.fr/Annuaire?structure_type%5B%5D=1'
        '&structure_type%5B%5D=2&structure_type%5B%5D=3&structure_type%5B%5D=4'
        '&field=-1&sector=-1&department=-1&address=&searchBtn=Rechercher',
    ]

    # There's 165 pages in this directory as of 2022-05-22.
    # This here is to avoid potentially upsetting the sysops.
    download_delay = 5

    def parse(self, response, **kwargs):
        yield from parse_points(response)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


def parse_points(response):
    blocks = response.css('article.item')
    for block in blocks:
        yield parse_point(block)


def parse_point(block):
    name = block.css('h2 a span::text').get().strip().title()

    point = {
        'name': name,
        'country': 'France',
    }

    # XXX: all info here is in French, might need to either make it explicit
    # (e.g. mark fields with .fr suffix) or use a translation service
    paragraphs = block.css('p.row')
    for paragraph in paragraphs:
        point.update(**parse_point_keys(paragraph))

    normalize_point_data(point)

    return point


def normalize_point_data(point):
    point.update(**{
        'categories': [],
        'description': '',
    })

    if point.get('_category'):
        point['categories'] += [point['_category']]

    if point.get('_relevant_services'):
        point['categories'] += point['_relevant_services']
        services = ', '.join(point['_relevant_services'])
        point['description'] = f'Services available: {services}'

    if not point['categories']:
        point['categories'] = [DEFAULT_CATEGORY]

    point['categories'] = ','.join(point['categories'])

    if point.get('_other_services'):
        services = ', '.join(point['_other_services'])
        point['description'] += f'\nOther services: {services}'

    if point.get('_website'):
        point['description'] += f'\nWebsite: {point["_website"]}'

    if point.get('_phone'):
        point['description'] += f'\nContact information: {point["_phone"]}'
        if point.get('_fax'):
            point['description'] += f', fax {point["_phone"]}'

    if point.get('_working_hours'):
        point['description'] += f'\nWorking hours: {point["_working_hours"]}'

    point['description'] = point['description'].strip()

    # all keys starting with _ are for processing purposes only
    for key in list(point.keys()):
        if key.startswith('_'):
            del(point[key])


def parse_point_keys(paragraph):
    titles = {
        'adresse': (None, parse_address),
        'actions': (None, parse_actions),
        'filière ': (None, parse_categories),
        'site web': ('_website', parse_website),
        'téléphone': ('_phone', parse_default_key),
        'fax': ('_fax', parse_default_key),
        "heures d'ouverture": ('_working_hours', parse_default_key),
    }

    title = paragraph.css('strong::text').get().lower()
    keys = [v for k, v in titles.items() if title.startswith(k)]
    if not keys:
        log.warning('Unknown title: %s', title)
        return {}
    key, func = keys.pop()
    return func(paragraph, key)


def parse_default_key(paragraph, key):
    value = paragraph.css('span.value *::text').get().strip()
    return {key: value.title()}


def parse_address(paragraph, _):
    values = paragraph.css('span.value::text').getall()
    return {
        'city': despacify(values[-1].split('\n')[-1]).title(),
        'address': despacify(' '.join(values[:-1])).title(),
    }


def parse_actions(paragraph, _):
    actions = paragraph.css('span.value *::text').getall()
    relevant_services = []
    other_services = []
    for action in actions:
        action = action.strip()
        if action.lower() in SERVICES_TO_CATEGORIES:
            relevant_services.append(SERVICES_TO_CATEGORIES[action.lower()])
        else:
            other_services.append(action)
    return {
        '_relevant_services': relevant_services,
        '_other_services': other_services,
    }


def parse_categories(paragraph, _):
    category = paragraph.css('span.value *::text').get()
    if not category:
        return {}
    return {
        '_category': CATEGORIES[category.lower()]
    } if category.lower() in CATEGORIES else {}


def parse_website(paragraph, key):
    value = paragraph.css('span.value a::attr(href)').get().strip()
    return {key: value.lower()}


def despacify(txt):
    """
    Normalize spacing.

    Squeeze multiple spacial symbols into a single " ".
    """
    return re.sub(r'[\s]+', ' ', txt, flags=re.M).strip()
