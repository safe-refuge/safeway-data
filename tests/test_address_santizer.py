import pytest

from returns.unsafe import unsafe_perform_io
from config import settings
from services.address_sanitizer import AddressSanitizer
from models.point_of_interest import PointOfInterest
from implemented import ConvertSpreadsheetData

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


def fake_make_places_request(*args, **kwargs):
    return [
        {
            'description': 'Ludwika Zamenhofa 1, 00-153 Warsaw, Poland'
        }
    ]


def fake_init_google_maps(key):
    return {}


def test_address_sanitizer(point_of_interest: PointOfInterest):
   
    addressSanitizer: AddressSanitizer = ConvertSpreadsheetData(
        make_places_request=fake_make_places_request,
        init_google_maps=fake_init_google_maps).address_sanitizer
    addressSanitizer.settings.sanitize_address = True
    result = addressSanitizer.sanitize([point_of_interest])
    enhanced: PointOfInterest = result[0]
    assert enhanced.address == 'Ludwika Zamenhofa 1, 00-153 Warsaw, Poland'
