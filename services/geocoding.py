from dataclasses import dataclass
from typing import Callable, List, Mapping, Set

import googlemaps

from config.settings import Settings
from models.point_of_interest import PointOfInterest


@dataclass
class Point:
    lat: str
    lng: str


def make_geocode_request(address: str, gmaps):
    return gmaps.geocode(address)


def init_google_maps(key):
    return googlemaps.Client(key=key)


@dataclass
class GeoCodingProcessor:

    # Injected dependencies
    settings: Settings
    log: Callable
    make_geocode_request: Callable = make_geocode_request
    init_google_maps: Callable = init_google_maps

    def enhance(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        For entries with missing lat/lng but present address
        we can find lat/lng using a geocoding API.
        """

        # Create client instance of gmaps
        gmaps = self.init_google_maps(self.settings.developer_key)

        addresses_to_geocode: Set[str] = {
            poi.address
            for poi in entries
            if (not poi.lat or not poi.lng)
            and poi.address
        }

        coordinates: Mapping[str, Point] = {}

        for address in addresses_to_geocode:
            reason = ""
            response = None
            try:
                response = self.make_geocode_request(address, gmaps)
            except Exception as e:
                reason = str(e)

            geoData = response[0]["geometry"]["location"] if response else None
            if geoData:
                point = Point(geoData["lat"], geoData["lng"])
                coordinates.update({address: point})
                self.log(f"Found coordinates for {address}: {point}")
            else:
                self.log(f"Failed to geocode address: {address}. {reason}")

        for entry in entries:
            point = coordinates.get(entry.address)
            if point:
                entry.lat = point.lat
                entry.lng = point.lng

        return entries
