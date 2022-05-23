from typing import List

import pytest

from config.settings import Settings
from services.google_translate import BatchRequestsBuilder, GoogleTranslateReader
from services.translation import CityTranslator
from models.point_of_interest import PointOfInterest
from googleapiclient.http import HttpRequest


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


def stub_fetch_translated_text(settings, text: List[str]) -> List[str]:
    mapping = {
        'Warszawa': 'Warsaw',
        'Mladá Boleslav': 'Mlada Boleslav'}
    return [mapping.get(t) for t in text]


class TestCityTranslator:
    def test_translation(self, point_of_interest: PointOfInterest):
        subject = CityTranslator(Settings(), stub_fetch_translated_text)
        result = subject.translate([point_of_interest])
        enhanced: PointOfInterest = result[0]
        assert enhanced.city == "Warsaw"

    def test_translation_with_english(self, poi_with_city_in_english: PointOfInterest):
        subject = CityTranslator(Settings(), stub_fetch_translated_text)
        result = subject.translate([poi_with_city_in_english])
        enhanced: PointOfInterest = result[0]
        assert enhanced.city == 'Neculaieuca Kindergarten'

    def test_translations(self, point_of_interests: List[PointOfInterest]):
        subject = CityTranslator(Settings(), stub_fetch_translated_text)
        result = subject.translate(point_of_interests)
        enhanced: List[PointOfInterest] = result
        assert enhanced[0].city == 'Mlada Boleslav'
        assert enhanced[1].city == 'Warsaw'


def stub_build_request(service, multiple_texts: List[str]) -> HttpRequest:
    return HttpRequest(None, None, None, body=multiple_texts)


class TestBatchRequestBuilder:

    def test_run_one_batch(self):
        data = ['foo', 'bar']
        requests = BatchRequestsBuilder(data, None, batch_size=4, build_request=stub_build_request)
        result = [request.body for request in requests]
        expect = [request.body for request in [stub_build_request(None, ['foo', 'bar'])]]
        assert result == expect

    def test_run_more_batch(self):
        data = ['foo', 'bar', 'fizz', 'buzz']
        requests = BatchRequestsBuilder(data, None, batch_size=2, build_request=stub_build_request)
        result = [request.body for request in requests]
        expect = [request.body for request in [stub_build_request(None, ['foo', 'bar'])]] + \
                 [request.body for request in [stub_build_request(None, ['fizz', 'buzz'])]]
        assert result == expect


class TestGoogleTranslateReader:
    def test_process_response(self):
        data = [{'translations': [{'translatedText': 'foo'}, {'translatedText': 'bar'}]}]
        result = GoogleTranslateReader.process_response(data)
        assert result == ['foo', 'bar']

    def test_process_responses(self):
        data = [{'translations': [{'translatedText': 'foo'}, {'translatedText': 'bar'}]},
                {'translations': [{'translatedText': 'fizz'}, {'translatedText': 'buzz'}]}]
        result = GoogleTranslateReader.process_response(data)
        assert result == ['foo', 'bar', 'fizz', 'buzz']
