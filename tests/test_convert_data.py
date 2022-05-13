from implemented import ConvertSpreadsheetData


def test_spreadsheet_data_conversion():
    usecase = ConvertSpreadsheetData.usecase
    result: list = usecase.convert(output="result.csv")
    assert not result
