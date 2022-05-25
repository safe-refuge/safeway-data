import re
import logging

import scrapy


log = logging.getLogger(__name__)


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
        blocks = response.css('article.item')
        for block in blocks:
            yield parse_point(block)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


def parse_point(block):
    name = block.css('h2 a span::text').get().strip().title()

    point = {
        'name': name,
        'country': 'France',
        # XXX: oversimplified, need to understand if actions can be used here
        'categories': 'Medical',
    }

    # XXX: all info here is in French, might need to either make it explicit
    # (e.g. mark fields with .fr suffix) or use a translation service
    paragraphs = block.css('p.row')
    for paragraph in paragraphs:
        point.update(**parse_point_keys(paragraph))

    return point


def parse_point_keys(paragraph):
    titles = {
        'adresse': (None, parse_address),
        'actions': (None, parse_actions),

        # XXX: these return some extra keys, perhaps useless, or even breaking
        'site web': ('website', parse_website),
        'téléphone': ('phone', parse_default_key),
        'fax': ('fax', parse_default_key),
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


# TODO: use actions to categorize points
def parse_actions(paragraph, _):
    actions = paragraph.css('span.value *::text').getall()
    services = despacify('; '.join(actions))
    return {
        'description': f'Available aid: {services}'
    }


def parse_website(paragraph, key):
    value = paragraph.css('span.value *::text').get().strip()
    return {key: value.lower()}


def despacify(txt):
    """
    Normalize spacing.

    Squeeze multiple spacial symbols into a single " ".
    """
    return re.sub(r'[\s]+', ' ', txt, flags=re.M).strip()
