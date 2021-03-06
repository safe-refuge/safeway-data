import pytest

from services.geocoding import GeoCodingProcessor
from models.point_of_interest import PointOfInterest
from implemented import ConvertSpreadsheetData


@pytest.fixture
def point_of_interest():
    return PointOfInterest(
        name="The Ukrainian House",
        country="Poland",
        city="Warszawa",
        address="ul. Zamenhofa 1, 00-153",
        lat="",
        lng="",
        categories=["General"],
        organizations=["Fundacja “Nasz Wybór”"],
        description="Crisis support center",
    )


@pytest.fixture
def addressless_point_of_interest():
    return PointOfInterest(
        name="The Ukrainian House",
        country="",
        city="",
        address="",
        lat="52.2473216",
        lng="20.9964703",
    )


def fake_make_geocode_request(*args, **kwargs):
    return [{
        "geometry": {
            "location": {
                "lat": "52.2473216",
                "lng": "20.9964703",
            },
        },
    }]


def fake_make_reverse_geocode_request(*args, **kwargs):
    return [{
        "address_components": [{
            "long_name": "Warsaw",
            "short_name": "Warsaw",
            "types": ["administrative_area_level_1", "political"],
        }, {
            "long_name": "Poland",
            "short_name": "Poland",
            "types": ["country", "political"],
        }],
        "formatted_address": "ul. Zamenhofa 1, 00-153",
    }]


def fake_init_google_maps(key):
    return {}


def test_geocoding(point_of_interest: PointOfInterest):
    geocoder: GeoCodingProcessor = ConvertSpreadsheetData(
        make_geocode_request=fake_make_geocode_request,
        init_google_maps=fake_init_google_maps).geocoder

    result = geocoder.enhance([point_of_interest])
    enhanced: PointOfInterest = result[0]
    assert enhanced.lat == "52.2473216"
    assert enhanced.lng == "20.9964703"


def test_reverse_geocoding(addressless_point_of_interest: PointOfInterest):
    geocoder: GeoCodingProcessor = ConvertSpreadsheetData(
        make_reverse_geocode_request=fake_make_reverse_geocode_request,
        init_google_maps=fake_init_google_maps).geocoder

    point = geocoder.enhance_by_reverse_lookup(addressless_point_of_interest)
    assert point.country == "Poland"
    assert point.city == "Warsaw"
    assert point.address == "ul. Zamenhofa 1, 00-153"
