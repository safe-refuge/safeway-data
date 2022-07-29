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


@pytest.mark.parametrize('phone, country, expected,', [
    ('(+48) 792 568 561', 'Poland', '+48 792 568 561'),
    ('792 568 561', 'Poland', '+48 792 568 561'),
    ('(+48) 792 568 561', None, '+48 792 568 561'),
    ('792 568 561', None, '')
])
def test_phone_validation_with_country(phone, country, expected):
    real = sanitise_phone(phone, country)
    assert real == expected


@pytest.mark.parametrize('phone, country, expected,', [
    ('(+ 48) 792 568 561, (+48) 22 621 51 65', None, '+48 792 568 561'),
    ('735174517, 735755200, 731512726', 'Poland', '+48 735174517'),
    ('0230 - 564462; 0230 – 564463; Fax: 0230 - 564464', 'Romania', '+40 230 564 462'),
    ('Tel.: +40 261 80 77 57, +40 261 80 77 77 interior 20695, 20696, 20697 ', None, '+40 261 807 757'),
    ('(+48) 727 805 764', 'Ukraine', '+48 727 805 764'),
    ('224813418', 'Czech Republic', '+43 2248 13418'),
    ('+43 05/17 76 380 (the hotline is available Monday-Friday from 9:00-16:00 and is in German or English)', 'Austria',
     '+43 517 76380'),
    ('+48 542851327', 'Poland', '+48 542851327'),
    ('+48 81 5666060', 'Poland', '+48 81 5666060'),
    ('+48 56 678 12 12', 'Poland', '+48 56 678 12 12'),
    ('+48 054-2842-252', 'Poland', '+48 054-2842-252'),
    ('+48 54 230-53-47', 'Poland', '+48 54 230-53-47'),
    ('+48 (0 44) 616 11 60', 'Poland', '+48 (0 44) 616 11 60'),
    ('+48 044 7102368', 'Poland', '+48 044 7102368'),
    ('+48 (14) 671-31-20', 'Poland', '+48 (14) 671-31-20'),
    ('+48 (0-24)', 'Poland', ''),
    ('+48 24 356 22 02  024 356 29 09', 'Poland', '+48 24 356 22 02'),
    ('+48 468302636\n468302648\n46 830', 'Poland', '+48 468302636'),
    ('+48 29 752-25-14   118', 'Poland', '+48 29 752-25-14'),
    ('+48 14 6761067       146761140', 'Poland', '+48 14 6761067'),
    ('+48 17 7445715 7445717 7445756', 'Poland', '+48 17 7445715'),
    ('+48 (15) 8643058, (15) 8665099', 'Poland', '+48 (15) 8643058'),
    ('+48 25 781 60 74, 25 787 73 50', 'Poland', '+48 25 781 60 74'),
    ('+48 22 510 98 03-19 foo', 'Poland', '+48 22 510 98 03'),
    ('foo +48 22 510 98 03-19 bar', 'Poland', '+48 22 510 98 03'),
    ('542851327', None, ''),
    ('373 786 05 080', 'Republic of Moldova' , '+373 786 05 080')
])
def test_phone_validation_with_country_edge_cases(phone, country, expected):
    real = sanitise_phone(phone, country)
    assert real == expected
