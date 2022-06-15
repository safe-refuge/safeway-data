from dataclasses import dataclass
from typing import List, Mapping, Set, Callable

from config.settings import Settings
from models.point_of_interest import PointOfInterest
from services.google_translate import GoogleTranslateReader


def fetch_translated_text(settings: Settings, text: List[str]):
    result = GoogleTranslateReader(settings=settings).translate(text)
    return result


@dataclass
class PointTranslator:
    # Injected dependencies
    settings: Settings
    fetch_translated_text: Callable = fetch_translated_text

    def translate(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        We need to make sure that all city names are in English
        we can do it by translating them using a translation API.
        """
        cities_translated_map = self.get_mapping({poi.city for poi in entries})
        countries_translated_map = self.get_mapping({poi.country for poi in entries})

        for entry in entries:
            original_city = entry.city
            entry.city = cities_translated_map.get(original_city, original_city)

            original_country = entry.country
            entry.country = countries_translated_map.get(original_country, original_country)
        return entries

    def get_mapping(self, data: Set[str]) -> Mapping[str, str]:
        english_embedded_data = {item for item in data if self._has_english_name(item)}
        _data = {item for item in data if not self._has_english_name(item)}
        if english_embedded_data:
            english_embedded_map = self._get_english_embedded_mapping(english_embedded_data)
            translated_map = self._get_translated_mapping(_data)
            return {**english_embedded_map, **translated_map}
        else:
            return self._get_translated_mapping(data)

    def _get_translated_mapping(self, data: Set[str]) -> Mapping[str, str]:
        translated_text = self.fetch_translated_text(self.settings, list(data))
        return dict(zip(data, translated_text))

    @staticmethod
    def _has_english_name(name: str) -> bool:
        return '/' in name

    @staticmethod
    def _get_english_embedded_mapping(names: Set[str]) -> Mapping[str, str]:
        result = {}
        for name in names:
            org, eng = name.split('/')
            result[name] = eng.strip()
        return result
