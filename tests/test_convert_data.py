from io import StringIO
from typing import List

from implemented import ConvertSpreadsheetData

HEADERS = ['Name', 'City', 'Address', 'Latitude', 'Longitude', 'Category', 'Organizations', 'Description', 'Phone',
           'Website', 'E-mail', 'Opening hours/days']
SAMPLE_ROW = ['The Ukrainian House', 'Warszawa', 'ul. Zamenhofa 1, 00-153', '52,24734033', '20,9964833',
              'Accommodation',
              'Fundacja “Nasz Wybór”', 'Crisis support center', '(+48) 727 805 764 ', 'https://ukrainskidom.pl/',
              'biuro@ukrainskidom.pl',
              'Monday:        09:00–19:00\nTuesday:       09:00–19:00\nWednesday:       09:00–19:00\nThursday:       09:00–19:00\nFriday:       09:00–19:00\nSaturday:        09:00–17:00\nSunday:       Closed\n']
SAMPLE_ROW2 = ['The Ukrainian House', 'Warszawa', 'ul. Zamenhofa 1, 00-153', '52,24734033', '20,9964833',
               'Accommodation',
               'Fundacja “Nasz Wybór”', 'Crisis support center', '(+48) 727 805 764 ', 'https://ukrainskidom.pl/',
               'biuro@ukrainskidom.pl',
               'Monday:        09:00–19:00\nTuesday:       09:00–19:00\nWednesday:       09:00–19:00\nThursday:       09:00–19:00\nFriday:       09:00–19:00\nSaturday:        09:00–17:00\nSunday:       Closed\n']
REAL_ROW = ['The Association for Legal Intervention', 'Warszawa', 'ul. Siedmiogrodzka 5/51', '',
            '', 'Attorney at law', 'Stowarzyszenie Interwencji Prawnej', 'Free legal assistance',
            '(+ 48) 792 568 561, (+48) 22 621 51 65', 'https://interwencjaprawna.pl/', 'biuro@interwencjaprawna.pl',
            'Monday:        10:00–16:00\nTuesday:        10:00–18:00 \nWednesday:      10:00–16:00\nThursday:        10:00–16:00\nFriday:      10:00–16:00\nSaturday:       Closed\nSunday:        Closed']

UA = [HEADERS, SAMPLE_ROW]
PL = [HEADERS, SAMPLE_ROW2, REAL_ROW]

FILES = {}
FILE_VALUES = []


def fake_make_request(request):
    return {
        "range": "PL!A4:L",
        "values": PL
    }


def fake_open_file(path):
    FILES[path] = StringIO()
    return FILES[path]


def fake_close_file(file):
    FILE_VALUES.append(file.getvalue())
    file.close()


def fake_make_geocode_request(*args, **kwargs):
    return [
        {
            'geometry': {
                'location': {
                    "lat": "52.23156761",
                    "lng": "20.97296521"
                }
            }
        }
    ]


def fake_init_google_maps(key):
    return {}


def stub_fetch_translated_text(settings, text: List[str]) -> List[str]:
    mapping = {
        'Warszawa': 'Warsaw',
        'Mladá Boleslav': 'Mlada Boleslav'}
    return [mapping.get(t) for t in text]


def test_spreadsheet_data_conversion():
    usecase: ConvertSpreadsheetData = ConvertSpreadsheetData(
        make_request=fake_make_request,
        make_geocode_request=fake_make_geocode_request,
        init_google_maps=fake_init_google_maps,
        fetch_translated_text=stub_fetch_translated_text,
        open_file=fake_open_file,
        close_file=fake_close_file).usecase

    result = usecase.convert_spreadsheet("some-id")
    csv = FILE_VALUES[0]
    expected_row = "The Ukrainian House,Poland,Warsaw,\"ul. Zamenhofa 1, 00-153\",52.24734033,20.9964833," \
                   "Accommodation,Fundacja “Nasz Wybór”,Crisis support center"

    # TODO: verify city translation

    assert len(result) == 1
    assert len(usecase.error_collector.invalid_points) == 1
    assert expected_row in csv
