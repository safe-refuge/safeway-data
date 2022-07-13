import pytest

from adapters.spreadsheet_adapter import SpreadsheetAdapter
from models.point_of_interest import PointOfInterest
from models.spreadsheet_row import SpreadsheetRow


@pytest.fixture
def spreadsheet_row():
    return SpreadsheetRow(
        country='Poland',
        name='The Ukrainian House',
        city='Warszawa',
        address='ul. Zamenhofa 1, 00-153',
        latitude='52,24734033',
        longitude='20,9964833',
        category='General',
        organizations='Fundacja “Nasz Wybór”',
        description='Crisis support center',
        phone='(+48) 727 805 764 ',
        website='https://ukrainskidom.pl/',
        email='biuro@ukrainskidom.pl',
        opening_hours='Monday:        09:00–19:00\nTuesday:       09:00–19:00',
    )


@pytest.fixture
def point_of_interest():
    return PointOfInterest(
        name='The Ukrainian House',
        country='Poland',
        city='Warszawa',
        address='ul. Zamenhofa 1, 00-153',
        lat='52.24734033',
        lng='20.9964833',
        categories=["General"],
        organizations=['Fundacja “Nasz Wybór”'],
        description='Crisis support center',
        phone='(+48) 727 805 764 ',
        website='https://ukrainskidom.pl/',
        email='biuro@ukrainskidom.pl',
        open_hours='Monday:        09:00–19:00\nTuesday:       09:00–19:00',
    )


def test_transform_row(spreadsheet_row, point_of_interest):
    subject = SpreadsheetAdapter()
    assert subject.transform_row(spreadsheet_row) == point_of_interest
