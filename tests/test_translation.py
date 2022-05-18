import pytest
from returns.unsafe import unsafe_perform_io

from config.settings import Settings
from services.translation import CityTranslator
from models.point_of_interest import PointOfInterest



@pytest.fixture
def point_of_interest():
    return PointOfInterest(
        name='The Ukrainian House',
        country='Poland',
        city='Warszawa',
        address='ul. Zamenhofa 1, 00-153',
        lat='50.847608',
        lng='16.473205',
        categories="General",
        organizations='Fundacja “Nasz Wybór”',
        description='Crisis support center'
    )


def test_translation(point_of_interest: PointOfInterest):
    # TODO: Make this test pass by implementing CityTranslator
    subject = CityTranslator(Settings())
    result = subject.translate([point_of_interest])
    enhanced: PointOfInterest = unsafe_perform_io(result).unwrap()[0]
    assert enhanced.city == "Warsaw"
