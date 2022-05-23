from dataclasses import dataclass
from typing import List, Mapping, Set, Callable

from config.settings import Settings
from models.point_of_interest import PointOfInterest
from services.google_translate import GoogleTranslateReader


def fetch_translated_text(settings: Settings, text: List[str]):
    result = GoogleTranslateReader(settings=settings).translate(text)
    return result


@dataclass
class CityTranslator:

    # Injected dependencies
    settings: Settings
    fetch_translated_text: Callable = fetch_translated_text

    def translate(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        We need to make sure that all city names are in English
        we can do it by translating them using a translation API.
        """
        cities_from_names: List[str] = [poi.city for poi in entries if self._has_english_name(poi.city)]
        cities_from_name_map: Mapping[str, str] = self._get_english_exist_mapping(cities_from_names)
        cities_to_translate: Set[str] = {poi.city for poi in entries if not self._has_english_name(poi.city)}

        translated_text = self.fetch_translated_text(self.settings, list(cities_to_translate))
        translations: Mapping[str, str] = dict(zip(cities_to_translate, translated_text))

        for entry in entries:
            original_city = entry.city
            entry.city = translations.get(original_city, None)
            if entry.city is None:
                entry.city = cities_from_name_map.get(original_city, original_city)

        return entries

    @staticmethod
    def _has_english_name(name: str) -> bool:
        return '/' in name

    @staticmethod
    def _get_english_exist_mapping(names: List[str]) -> Mapping[str, str]:
        result = {}
        for name in names:
            org, eng = name.split('/')
            result[name] = eng.strip()
        return result
