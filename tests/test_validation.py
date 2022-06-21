import pytest

from models.point_of_interest import PointOfInterest
from validation import RequiredFieldsValidator
from validation.categories import CategoriesValidator
from validation.phones import sanitise_phone
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


@pytest.mark.parametrize('origin,expected', [
    ('+48 542851327', '+48 54 285 13 27'),
    ('+48 81 5666060', '+48 81 566 60 60'),
    ('+48 56 678 12 12', '+48 56 678 12 12'),
    ('+48 054-2842-252', '+48 0542842252'),
    ('+48 54 230-53-47', '+48 54 230 53 47'),
    ('+48 24 356 22 02  024 356 29 09', 'Error: +48 24 356 22 02  024 356 29 09'),
    ('+48 (0-24)', 'Error: +48 (0-24)'),
    ('+48 468302636\n468302648\n46 830', 'Error: +48 468302636\n468302648\n46 830'),
    ('+48 (0 44) 616 11 60', '+48 0446161160'),
    ('+48 044 7102368', '+48 0447102368'),
    ('+48 (14) 671-31-20', '+48 14 671 31 20'),
    ('+48 14 6761067       146761140', 'Error: +48 14 6761067       146761140'),
    ('+48 17 7445715 7445717 7445756', 'Error: +48 17 7445715 7445717 7445756'),
    ('+48 29 752-25-14   118', 'Error: +48 29 752-25-14   118'),
    ('+48 (15) 8643058, (15) 8665099', 'Error: +48 (15) 8643058, (15) 8665099'),
    ('+48 25 781 60 74, 25 787 73 50', 'Error: +48 25 781 60 74, 25 787 73 50'),
    ('+48 22 510 98 03-19 foo', 'Error: +48 22 510 98 03-19 foo'),
    ('foo +48 22 510 98 03-19 bar', 'Error: foo +48 22 510 98 03-19 bar'),
    ('542851327', 'Error: 542851327')])
def test_phone_validation(origin, expected):
    real = sanitise_phone(origin)
    assert real == expected
