import html
import re
from typing import List, Any
from pydantic import BaseModel, validator

from models.constants import DEFAULT_URL_PROTOCOLS, DEFAULT_URL_SCHEMES, ERROR_PREFIX


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
            return ERROR_PREFIX + org_url

        markdown_url = re.search('\[.*\]\((.*)\)', url)
        if markdown_url:
            url = markdown_url.groups()[0]

        regex_url = re.compile(
            r'([(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))',
            re.IGNORECASE)
        valid_url = regex_url.search(url)
        if valid_url:
            _url = valid_url.groups()[0]
            if all([scheme not in _url for scheme in DEFAULT_URL_SCHEMES]) and not url.startswith(ERROR_PREFIX):
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
