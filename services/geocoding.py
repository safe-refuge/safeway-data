import re
import googlemaps

from dataclasses import dataclass
from typing import List, Mapping
from returns.io import impure_safe
from config.settings import Settings
from models.point_of_interest import PointOfInterest
@dataclass
class Point:
    lat: str
    lng: str


@dataclass
class GeoCodingProcessor:

    # Injected dependencies
    settings: Settings

    @impure_safe
    def enhance(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        For entries with missing lat/lng but present address
        we can find lat/lng using a geocoding API.
        """
        #Create client instance of gmaps
        gmaps = googlemaps.Client(key=self.settings.developer_key)

        addresses_to_geocode: List[str] = [
            poi.address
            for poi in entries
            if not poi.lat or not poi.lng
        ]

        coordinates: Mapping[str, Point] = {}

        for address in addresses_to_geocode:
            latLng = gmaps.geocode(address)
            coordinates.update(address, latLng)
 
        for entry in entries:
            point = coordinates.get(entry.address)
            if point:
                entry.lat = point.lat
                entry.lng = point.lng

        return entries
