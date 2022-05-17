from pydantic import BaseModel


class PointOfInterest(BaseModel):
    name: str = ""
    country: str = ""
    city: str = ""
    address: str = ""
    lat: str = ""
    lng: str = ""
    categories: str = ""
    organizations: str = ""
    description: str = ""
