from typing import List

import pycountry

from models.point_of_interest import PointOfInterest
from models.spreadsheet_row import SpreadsheetRow


class SpreadsheetAdapter:
    ALIASES = {
        # Same: name, city, address, organizations, descriptions
        "latitude": "lat",
        "longitude": "lng",
        "category": "categories",
        "country_code": "country"
    }

    def transform(self, source: List[SpreadsheetRow]) -> List[PointOfInterest]:
        return [self.transform_row(row) for row in source]

    def transform_row(self, row: SpreadsheetRow) -> PointOfInterest:
        fields = {}

        for name, value in row.dict().items():
            field = self.ALIASES.get(name, name)
            converter = getattr(self, f"convert_{field}", self.convert_noop)
            fields[field] = converter(value)

        return PointOfInterest(**fields)

    def convert_noop(self, value: str) -> str:
        return value

    def convert_country(self, country_code: str) -> str:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else ""

    def convert_lat(self, latitude: str) -> str:
        return self._convert_number(latitude)

    def convert_lng(self, longitude: str) -> str:
        return self._convert_number(longitude)

    @staticmethod
    def _convert_number(number: str) -> str:
        return number.replace(",", ".")
