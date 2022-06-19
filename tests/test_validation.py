import pytest

from models.point_of_interest import PointOfInterest
from validation import RequiredFieldsValidator
from validation.categories import CategoriesValidator
from validation.urls import sanitise_url


@pytest.fixture
def complete_point_of_interest():
    return PointOfInterest(
        name='The Ukrainian House',
        country='Poland',
        city='Warszawa',
        address='ul. Zamenhofa 1, 00-153',
        lat='52.24734033',
        lng='20.9964833',
        categories=['Pharmacy'],
        organizations=['Fundacja “Nasz Wybór”'],
        description='Crisis support center'
    )


def test_required_fields_missing():
    incomplete_point = PointOfInterest(name='Incomplete')
    assert not RequiredFieldsValidator().is_valid(incomplete_point)


def test_required_fields_in_place(complete_point_of_interest: PointOfInterest):
    assert RequiredFieldsValidator().is_valid(complete_point_of_interest)


def test_allowed_category(complete_point_of_interest):
    assert CategoriesValidator().is_valid(complete_point_of_interest)


def test_invalid_category(complete_point_of_interest):
    invalid_point = complete_point_of_interest.copy(update={'categories': 'General'})
    assert not CategoriesValidator().is_valid(invalid_point)


@pytest.mark.parametrize('origin,expected', [
    ('https://example.vegan.com', 'https://example.vegan.com'),
    ('example.vegan.com', 'https://example.vegan.com'),
    ('', ''),
    ('grabowo.pl', 'https://grabowo.pl'),
    ('http://example.vegan.com', 'http://example.vegan.com'),
    ('http://gops.mielec.pl/ ; http://www.gops.ug.mielec.pl/', 'http://gops.mielec.pl/'),
    ('[www.pcprzwolen.pl](http://www.pcprzwolen.pl/)', 'http://www.pcprzwolen.pl/'),
    ('www.klwow', ''),
    ('mopsstalowawola@mops-stalwol.pl', ''),
    ('www.pcpr-jawor.https://sac.mpips.gov.pl:8443/Pomost/CKEditorServlet?TRYB=2',
     'https://sac.mpips.gov.pl:8443/Pomost/CKEditorServlet?TRYB=2')])
def test_url_validation(origin, expected):
    real = sanitise_url(origin)
    assert real == expected
