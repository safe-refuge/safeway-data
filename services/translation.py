from dataclasses import dataclass
from typing import List, Mapping, Set, Callable, Dict

from returns.io import impure_safe
from returns.unsafe import unsafe_perform_io

from config.settings import Settings
from models.point_of_interest import PointOfInterest
from services.google_translate import GoogleTranslateReader


def fetch_translated_text(settings: Settings, text: List[str]):
    result = GoogleTranslateReader(settings=settings).translate(text)
    return unsafe_perform_io(result).unwrap()[0]


@dataclass
class CityTranslator:
    # Injected dependencies
    settings: Settings
    fetch_translated_text: Callable = fetch_translated_text

    @impure_safe
    def translate(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        We need to make sure that all city names are in English
        we can do it by translating them using a translation API.
        """
        cities_from_names: List[str] = [poi.city for poi in entries if self._has_english_name(poi.city)]
        cities_from_name_map: Mapping[str, str] = self._get_english_exist_mapping(cities_from_names)
        cities_to_translate: Set[str] = {poi.city for poi in entries if not self._has_english_name(poi.city)}

        translations: Mapping[str, str] = {}
        # TODO: use a translation API to fill the English translations for each city
        translated_text = self.fetch_translated_text(self.settings, list(cities_to_translate))
        translations = dict(zip(cities_to_translate, translated_text))

        for entry in entries:
            original_city = entry.city
            entry.city = translations.get(original_city, None)
            if entry.city is None:
                entry.city = cities_from_name_map.get(original_city, original_city)

        return entries

    def _has_english_name(self, name: str) -> bool:
        return '/' in name

    def _get_english_exist_mapping(self, names: List[str]) -> Mapping[str, str]:
        result = {}
        for name in names:
            org, eng = name.split('/')
            result[name] = eng.strip()
        return result
