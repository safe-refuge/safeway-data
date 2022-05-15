from returns.io import impure_safe

from implemented import ConvertSpreadsheetData


HEADERS = ['Name', 'City', 'Address', 'Latitude', 'Longitude', 'Category', 'Organizations', 'Description', 'Phone',
         'Website', 'E-mail', 'Opening hours/days']
SAMPLE_ROW = ['The Ukrainian House', 'Warszawa', 'ul. Zamenhofa 1, 00-153', '52,24734033', '20,9964833', 'General',
      'Fundacja “Nasz Wybór”', 'Crisis support center', '(+48) 727 805 764 ', 'https://ukrainskidom.pl/',
      'biuro@ukrainskidom.pl',
      'Monday:        09:00–19:00\nTuesday:       09:00–19:00\nWednesday:       09:00–19:00\nThursday:       09:00–19:00\nFriday:       09:00–19:00\nSaturday:        09:00–17:00\nSunday:       Closed\n']
SAMPLE_ROW2 = ['The Ukrainian House', 'Warszawa', 'ul. Zamenhofa 1, 00-153', '52,24734033', '20,9964833', 'General',
      'Fundacja “Nasz Wybór”', 'Crisis support center', '(+48) 727 805 764 ', 'https://ukrainskidom.pl/',
      'biuro@ukrainskidom.pl',
      'Monday:        09:00–19:00\nTuesday:       09:00–19:00\nWednesday:       09:00–19:00\nThursday:       09:00–19:00\nFriday:       09:00–19:00\nSaturday:        09:00–17:00\nSunday:       Closed\n']
REAL_ROW = ['The Association for Legal Intervention', 'Warszawa', 'ul. Siedmiogrodzka 5/51', '52,23156761',
           '20,97296521', 'Attorney at law', 'Stowarzyszenie Interwencji Prawnej', 'Free legal assistance',
           '(+ 48) 792 568 561, (+48) 22 621 51 65', 'https://interwencjaprawna.pl/', 'biuro@interwencjaprawna.pl',
           'Monday:        10:00–16:00\nTuesday:        10:00–18:00 \nWednesday:      10:00–16:00\nThursday:        10:00–16:00\nFriday:      10:00–16:00\nSaturday:       Closed\nSunday:        Closed']

UA = [HEADERS, SAMPLE_ROW]
PL = [HEADERS, SAMPLE_ROW2, REAL_ROW]


def fake_make_request(request):
    return {
        "range": "PL!A4:L",
        "values": PL
    }


def test_spreadsheet_data_conversion():
    usecase = ConvertSpreadsheetData(make_request=fake_make_request).usecase
    result = usecase.convert(output="result.csv")
    assert len(result) == 2
