from typing import Dict

import pytest

from models.point_of_interest import PointOfInterest


def test_point_of_interest_validation():
    json = {'name': 'Școala auxiliară Bulboaca', 'country': 'Moldova', 'city': 'Anenii&#39; Noi',
            'address': 'Republica Moldova, Anenii Noi, s. Bulboaca', 'categories': 'Accommodation,Medical',
            'description': 'Capacity: 38', 'organizations': 'Domomoga Moldova', 'lat': '46.884741399999996',
            'lng': '29.3123414'}
    point = PointOfInterest(**json)

    assert point.categories == ['Accommodation', 'Medical']
    assert point.organizations == ['Domomoga Moldova']
    assert point.city == "Anenii' Noi"


@pytest.fixture
def point_of_interest() -> Dict[str, str]:
    return {
        'name': 'Școala auxiliară Bulboaca',
        'country': 'Moldova',
        'city': 'Anenii&#39; Noi',
        'address': 'Republica Moldova, Anenii Noi, s. Bulboaca',
        'categories': 'Accommodation,Medical',
        'description': 'Capacity: 38',
        'organizations': 'Domomoga Moldova',
        'url': '',
        'lat': '46.884741399999996',
        'lng': '29.3123414'
    }


@pytest.mark.parametrize('origin,expected', [
    ('https://example.vegan.com', 'https://example.vegan.com'),
    ('example.vegan.com', 'https://example.vegan.com'),
    ('', ''),
    ('grabowo.pl', 'https://grabowo.pl'),
    ('http://example.vegan.com', 'http://example.vegan.com'),
    ('http://gops.mielec.pl/ ; http://www.gops.ug.mielec.pl/', 'http://gops.mielec.pl/'),
    ('[www.pcprzwolen.pl](http://www.pcprzwolen.pl/)', 'http://www.pcprzwolen.pl/'),
    ('www.klwow', 'Error: www.klwow'),
    ('mopsstalowawola@mops-stalwol.pl', 'Error: mopsstalowawola@mops-stalwol.pl'),
    ('www.pcpr-jawor.https://sac.mpips.gov.pl:8443/Pomost/CKEditorServlet?TRYB=2', 'https://sac.mpips.gov.pl:8443/Pomost/CKEditorServlet?TRYB=2')])
def test_url_validation(point_of_interest, origin, expected):
    data = dict(point_of_interest, **{'url': origin})
    point = PointOfInterest(**data)
    assert point.url == expected
