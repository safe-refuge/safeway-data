from typing import List

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


@pytest.fixture()
def point_of_interests():
    return [PointOfInterest(city='Mladá Boleslav'), PointOfInterest(city='Warszawa')]


@pytest.fixture()
def poi_with_city_in_english():
    return PointOfInterest(
        name='Dondușeni',
        country='',
        city='satul Neculaieuca (Grădinița Neculaieuca )/ Neculaieuca Kindergarten ',
        address='or. Dondușeni, str. Ștefan cel Mare, 30 (could not locate on Google maps)',
        lat='',
        lng='',
        categories='Accredited Refugee Center ',
        organizations='',
        description='Refugee Center in a retreat center with 60 places '
    )


def stub_fetch_translated_text(text: List[str]) -> List[str]:
    mapping = {
        'Warszawa': 'Warsaw',
        'Mladá Boleslav': 'Mlada Boleslav'}
    return [mapping.get(t) for t in text]


def test_translation(point_of_interest: PointOfInterest):
    subject = CityTranslator(Settings(), stub_fetch_translated_text)
    result = subject.translate([point_of_interest])
    enhanced: PointOfInterest = unsafe_perform_io(result).unwrap()[0]
    assert enhanced.city == "Warsaw"


def test_translation_with_english(poi_with_city_in_english: PointOfInterest):
    subject = CityTranslator(Settings(), stub_fetch_translated_text)
    result = subject.translate([poi_with_city_in_english])
    enhanced: PointOfInterest = unsafe_perform_io(result).unwrap()[0]
    assert enhanced.city == 'Neculaieuca Kindergarten'


def test_translations(point_of_interests: List[PointOfInterest]):
    subject = CityTranslator(Settings(), stub_fetch_translated_text)
    result = subject.translate(point_of_interests)
    enhanced: List[PointOfInterest] = unsafe_perform_io(result).unwrap()
    assert enhanced[0].city == 'Mlada Boleslav'
    assert enhanced[1].city == 'Warsaw'
