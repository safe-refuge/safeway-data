from typing import List

import pytest
from scrapy import Spider

from models.point_of_interest import PointOfInterest
from scraping.spiders.moldova_dopomoga import DopomogaSpider, parse_details
from tests.utils import parse_betamax_response


TEST_DATA = [
    ('orașul Anenii Noi, str. Z.Cosmodimianscaia 5/3', 'str. Z.Cosmodimianscaia 5/3', 'str. Z.Cosmodimianscaia 5/3', 'Anenii Noi'),
    ('s. Bulboaca, Școala auxiliară Bulboaca', 'Școala auxiliară Bulboaca', 's. Bulboaca', None),
    ('Anenii Noi, Liceul Andrei Straistă', 'Liceul Andrei Straistă', 'Liceul Andrei Straistă', 'Anenii Noi'),
    ('str. Victoriei 62A Instituția Publică Școala Profesională nr. 3', 'Instituția Publică Școala Profesională nr. 3', 'str. Victoriei 62A', None),
    ('or. Briceni, str. 28 martie nr. 2 (Centrul de creație)', 'Centrul de creație', 'str. 28 martie nr. 2', 'Briceni'),
    ('mun. Cahul Școala Sportivă', 'Școala Sportivă', 'Școala Sportivă', 'Cahul'),
    ('Căminul Universității Tehnice a Moldovei str. Studenților 7/1', 'Căminul Universității Tehnice a Moldovei', 'str. Studenților 7/1', None),
    ('bd.Decebal 72/2 Centrul Sportiv de Pregătire a Loturilor Naționale a Ministerului Educației și Cercetării', 'Centrul Sportiv de Pregătire a Loturilor Naționale a Ministerului Educației și Cercetării', 'bd.Decebal 72/2', None),
    ('Bd. Mircea cel Bătrân 2, etajul 4 Asociația Obștească Pro valoare”', 'etajul 4 Asociația Obștească Pro valoare”', 'Bd. Mircea cel Bătrân 2', None),
    ('Hristo Botev nr. 2 Instituția Publică Liceul Republican cu Profil Sportiv din subordinea Ministerului Educației și Cercetării', 'Instituția Publică Liceul Republican cu Profil Sportiv din subordinea Ministerului Educației și Cercetării', 's. Hristo Botev nr. 2', None),
    ('satul Bravicea, Biserica Creștină Evanghelică Baptistă ”Emanuel”', 'Biserica Creștină Evanghelică Baptistă ”Emanuel”', 'satul Bravicea', None),
    (', 31 August, nr. 130, IP Școala Profesională din ', 'IP Școala Profesională din', '31 August, nr. 130', None),
    ('satul Ochiul Alb Centrul de zi și plasament pentru persoane în etate', 'Centrul de zi și plasament pentru persoane în etate', 'satul Ochiul Alb', None),
    ('s. Ștefănești (Căminul de elevi de pe lângă Liceul Teoretic Ștefănești)', 'Căminul de elevi de pe lângă Liceul Teoretic Ștefănești', 's. Ștefănești', None),
    ('s. Cărpineni, str. Gagarin 7', 's. Cărpineni, str. Gagarin 7', 's. Cărpineni, str. Gagarin 7', None),
    ('sat. Bozieni str. Mihai Eminescu Biserica Creștină Evanghelică Baptistă ”Noul Legământ”', 'Biserica Creștină Evanghelică Baptistă ”Noul Legământ”', 'sat. Bozieni str. Mihai Eminescu', None),
    ('sat. Costești, Clădirea fostului spital Costești', 'Clădirea fostului spital Costești', 'sat. Costești', None),
    ('satul Neculaieuca (Grădinița Neculaieuca )', 'Grădinița Neculaieuca', 'satul Neculaieuca', None),
    ('Centrul Comunitar Multifuncțional „Generația PRO” s. Peresecina', 'Centrul Comunitar Multifuncțional „Generația PRO”', 's. Peresecina', None),
    ('satul Ivancea Complexul Sportiv și de Întremare ”MAONC ACTIV”', 'Complexul Sportiv și de Întremare ”MAONC ACTIV”', 'satul Ivancea', None),
    ('s. Saharna', 's. Saharna', 's. Saharna', None),
    ('satul Egoreni (extravilan) Pensiunea Zăvoiul Nistrului', 'extravilan Pensiunea Zăvoiul Nistrului', 'satul Egoreni', None),
    ('satul Popeasca, rnul Stefan Voda', 'rnul Stefan Voda', 'satul Popeasca', None),
    ('com. Greblești r-nul  MD - 3720 (clădirea fostei grădinițe de copii)', 'clădirea fostei grădinițe de copii', 'com. Greblești r-nul  MD - 3720', None),
    ('z. Zahareuca, Pensiunea turistică ”Trei pastori”', 'Pensiunea turistică ”Trei pastori”', 'z. Zahareuca', None),
    ('com. Sculeni, Centrul de plasament pentru persoane în vârstă și adulte', 'Centrul de plasament pentru persoane în vârstă și adulte', 'com. Sculeni', None),
]


@pytest.mark.parametrize("details,expected_name,expected_address,city", TEST_DATA)
def test_parse_details(details, expected_name, expected_address, city):
    name, address = parse_details(details, city=city)
    assert name == expected_name
    assert address == expected_address


@pytest.mark.usefixtures('betamax_session')
def test_dopomoga_parse(betamax_session):
    spider: Spider = DopomogaSpider()
    url = spider.start_urls[0]
    results: List[PointOfInterest] = parse_betamax_response(betamax_session, spider.parse, url)

    assert results
    for point in results:
        assert all([
            point.name,
            point.categories,
            point.address,
            point.city,
            point.country,
            point.description
        ])
