from pydantic import BaseModel


class SpreadsheetRow(BaseModel):
    country_code: str = ""
    name: str = ""
    city: str = ""
    address: str = ""
    latitude: str = ""
    longitude: str = ""
    category: str = ""
    organizations: str = ""
    description: str = ""
    phone: str = ""
    website: str = ""
    email: str = ""
    opening_hours: str = ""
