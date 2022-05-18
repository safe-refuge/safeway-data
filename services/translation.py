from dataclasses import dataclass
from typing import List, Mapping, Set

from returns.io import impure_safe

from config.settings import Settings
from models.point_of_interest import PointOfInterest


@dataclass
class CityTranslator:

    # Injected dependencies
    settings: Settings

    @impure_safe
    def translate(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        We need to make sure that all city names are in English
        we can do it by translating them using a translation API.
        """
        cities_to_translate: Set[str] = {poi.city for poi in entries}

        translations: Mapping[str, str] = {}
        # TODO: use a translation API to fill the English translations for each city

        for entry in entries:
            entry.city = translations.get(entry.city, entry.city)

        return entries
