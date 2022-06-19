import html
import re
from typing import List, Any
from pydantic import BaseModel, validator

from models.constants import DEFAULT_URL_PROTOCOLS, DEFAULT_URL_SCHEMES, URL_REGEX, MARKDOWN_URL_REGEX


class PointOfInterest(BaseModel):
    name: str = ''
    country: str = ''
    city: str = ''
    address: str = ''
    categories: List[str] = []
    organizations: List[str] = []
    description: str = ''
    lat: str = ''
    lng: str = ''
    phone: str = ''
    email: str = ''
    url: str = ''
    socialmedia: str = ''
    messenger: str = ''
    telegram: str = ''
    whatsapp: str = ''
    open_hours: str = ''
    tags: List[str] = []
    icon: str = ''
    approved: bool = False
    active: bool = None

    @validator('city', pre=True)
    def sanitize_city(cls, city: str) -> str:
        return _sanitize(city)

    @validator('categories', pre=True)
    def ensure_categories_as_list(cls, categories: Any) -> List[str]:
        return _convert_to_list(categories)

    @validator('organizations', pre=True)
    def ensure_organizations_as_list(cls, organizations: Any) -> List[str]:
        return _convert_to_list(organizations)

    @validator('url', pre=True)
    def sanitize_url(cls, url: str) -> str:
        org_url = url
        if len(url.split('.')) < 3 and url.startswith('www') or '@' in url:
            return ''

        markdown_url = re.compile(MARKDOWN_URL_REGEX).search(url)
        if markdown_url:
            url = markdown_url.groups()[0]

        valid_url = re.compile(URL_REGEX, re.IGNORECASE).search(url)
        if valid_url:
            _url = valid_url.groups()[0]
            if all([scheme not in _url for scheme in DEFAULT_URL_SCHEMES]):
                url = DEFAULT_URL_PROTOCOLS + url

            not_start_with_http = re.search('(http.*)$', _url)
            if not_start_with_http:
                url = not_start_with_http.groups()[0]

        return url


def _convert_to_list(value: Any) -> List[str]:
    if isinstance(value, str):
        return value.split(',')
    return value


def _sanitize(value: str) -> str:
    return html.unescape(value)
