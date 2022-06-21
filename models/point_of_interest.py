from typing import List, Any

from pydantic import BaseModel, validator

from validation.urls import sanitise_url
from validation.phones import sanitise_phone
from validation import sanitize_value


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
        return sanitize_value(city)

    @validator('description', pre=True)
    def sanitize_description(cls, description: str) -> str:
        return sanitize_value(description)

    @validator('categories', pre=True)
    def ensure_categories_as_list(cls, categories: Any) -> List[str]:
        return _convert_to_list(categories)

    @validator('organizations', pre=True)
    def ensure_organizations_as_list(cls, organizations: Any) -> List[str]:
        return _convert_to_list(organizations)

    @validator('url', pre=True)
    def sanitize_url(cls, url: str) -> str:
        return sanitise_url(url)

    @validator('phone', pre=True)
    def sanitize_phone(cls, phone: str) -> str:
        return sanitise_phone(phone)


def _convert_to_list(value: Any) -> List[str]:
    if isinstance(value, str):
        return value.split(',')
    return value
