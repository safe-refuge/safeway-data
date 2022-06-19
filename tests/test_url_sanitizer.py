import pytest

from utils.urls import sanitise_url


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
