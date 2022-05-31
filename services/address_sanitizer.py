from dataclasses import dataclass
from multiprocessing.connection import Client
from typing import Callable, List, Mapping, Set

import googlemaps

import googlemaps.places

from config.settings import Settings
from models.point_of_interest import PointOfInterest


def make_places_request(address: str, gmaps: googlemaps.places):
    return gmaps.places_autocomplete(address)

# is there somewhere I can put this method to reuse it throughout the app?
def init_google_maps(key):
    return googlemaps.Client(key=key)


@dataclass
class AddressSanitizer:

    # Injected dependencies
    settings: Settings
    log: Callable
    make_places_request: Callable = make_places_request
    init_google_maps: Callable = init_google_maps

    def sanitize(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        """
        Sanitize address to conform to a standard format.
        We can find a standard format using the google places API.
        """
        if not self.settings.sanitize_address:
            return entries
        # Create client instance of gmaps
        gmaps: googlemaps.Client = self.init_google_maps(
            self.settings.developer_key)

        for entry in entries:
            reason = ""
            response = None
            try:
                response = self.make_places_request(entry.address, gmaps)
            except Exception as e:
                reason = str(e)

            santizedAddress = response[0]['description'] if response else None
            
            if santizedAddress:
                if santizedAddress != entry.address:
                    self.log(
                        f"{entry.address} has been converted to {santizedAddress}")
                    entry.address = santizedAddress
            else:
                self.log(
                    f"Failed to sanitize address: {entry.address}. {reason}")

        return entries
