from typing import List
from pydantic import BaseModel


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
    open_hours: str = ''
    tags: List[str] = []
    icon: str = ''
    approved: bool = True
    active: bool = True
