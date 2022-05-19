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


def test_geocoding(point_of_interest: PointOfInterest):
    subject = GeoCodingProcessor(Settings())
    result = subject.enhance([point_of_interest])
    enhanced: PointOfInterest = unsafe_perform_io(result).unwrap()[0]
    assert enhanced.lat == 52.2473216
    assert enhanced.lng == 20.9964703
