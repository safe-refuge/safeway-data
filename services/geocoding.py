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


def make_reverse_geocode_request(lat: str, lng: str, gmaps):
    return gmaps.reverse_geocode(f"{lat},{lng}")


def init_google_maps(key):
    return googlemaps.Client(key=key)


@dataclass
class GeoCodingProcessor:

    # Injected dependencies
    settings: Settings
    log: Callable
    gmaps: googlemaps.Client = None
    make_geocode_request: Callable = make_geocode_request
    make_reverse_geocode_request: Callable = make_reverse_geocode_request
    init_google_maps: Callable = init_google_maps

    def enhance(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        For entries with missing lat/lng but present address
        we can find lat/lng using a geocoding API.
        """

        # Create client instance of gmaps
        self.gmaps = self.init_google_maps(self.settings.developer_key)

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
                response = self.make_geocode_request(address, self.gmaps)
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

            if not entry.lat or not entry.lng:
                continue
            if entry.country and entry.city and entry.address:
                continue
            self.enhance_by_reverse_lookup(entry)

        return entries

    def enhance_by_reverse_lookup(self, entry: PointOfInterest):
        try:
            response = self.make_reverse_geocode_request(
                entry.lat, entry.lng, self.gmaps)
        except (googlemaps.exceptions.ApiError, googlemaps.exceptions.Timeout,
                googlemaps.exceptions.TransportError) as e:
            self.log(f"Reverse geocode: failed {entry.lat},{entry.lng}: {e}")

        if not response:
            self.log(f"Reverse geocode: got 0 results {entry.lat},{entry.lng}")
        geodata = response[0]["address_components"]

        if not entry.country:
            entry.country = next(
                r["long_name"] for r in geodata
                if "country" in r["types"])

        if not entry.city:
            city_levels = {
                "locality",
                "administrative_area_level_1",
                "administrative_area_level_2",
            }
            entry.city = next(
                r["long_name"] for r in geodata
                if city_levels & set(r["types"]))

        if not entry.address:
            entry.address = response[0]["formatted_address"]

        return entry
