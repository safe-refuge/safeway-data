from implemented import ConvertSpreadsheetData
import pytest
from returns.unsafe import unsafe_perform_io

from config.settings import Settings
from services.geocoding import GeoCodingProcessor
from models.point_of_interest import PointOfInterest


@pytest.fixture
def point_of_interest():
    return PointOfInterest(
        name='The Ukrainian House',
        country='Poland',
        city='Warszawa',
        address='ul. Zamenhofa 1, 00-153',
        lat='',
        lng='',
        categories="General",
        organizations='Fundacja “Nasz Wybór”',
        description='Crisis support center'
    )


def fake_make_geocode_request(address: str, gmaps):
   return { "lat": "52.2473216", "lng": "20.9964703" }


def fake_init_google_maps():
    return {}

def test_geocoding(point_of_interest: PointOfInterest):
    geocoder: GeoCodingProcessor = ConvertSpreadsheetData(
    make_geocode_request=fake_make_geocode_request,
    init_google_maps=fake_init_google_maps).geocoder

    result = geocoder.enhance([point_of_interest])
    enhanced: PointOfInterest = unsafe_perform_io(result).unwrap()[0]
    assert enhanced.lat == 52.2473216
    assert enhanced.lng == 20.9964703
