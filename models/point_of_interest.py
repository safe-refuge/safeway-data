from typing import List, Any
from pydantic import BaseModel, validator


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
    approved: bool = True
    active: bool = True

    @validator('categories', pre=True)
    def ensure_categories_as_list(cls, categories: Any) -> List[str]:
        return _convert_to_list(categories)

    @validator('organizations', pre=True)
    def ensure_organizations_as_list(cls, organizations: Any) -> List[str]:
        return _convert_to_list(organizations)


def _convert_to_list(value: Any) -> List[str]:
    if isinstance(value, str):
        return value.split(',')
    return value