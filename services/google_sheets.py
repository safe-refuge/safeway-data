import re

from dataclasses import dataclass
from typing import Callable, List

from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

from config.settings import Settings
from models.spreadsheet_row import SpreadsheetRow


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def make_request(request: HttpRequest) -> dict:
    result = request.execute()
    return result


@dataclass
class GoogleSheetsReader:

    # Injected dependencies
    settings: Settings
    make_request: Callable = make_request

    def fetch(self, spreadsheet_id: str) -> List[SpreadsheetRow]:
        service = build('sheets', 'v4', developerKey=self.settings.developer_key)
        sheet = self.settings.countries[0]  # TODO: loop through all countries
        request: HttpRequest = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet}!{self.settings.cells_range}")

        response = self.make_request(request)
        result = self.process_response(response)

        return result

    def process_response(self, response: dict) -> List[SpreadsheetRow]:
        country = response["range"].split("!")[0]
        rows = response["values"]
        headers: List[str] = [self.normalize_header(header) for header in rows[0]]
        rows: List[SpreadsheetRow] = [self.generate_row(values, headers, country) for values in rows[1:]]
        return rows

    def normalize_header(self, header: str) -> str:
        """
        Converts values to fields for `SpreadsheetRow`

        Examples::
            Opening hours/days -> opening_hours
            E-mail -> email
        """
        snake_case = re.sub(r"\s", "_", header.lower()).replace("-", "")
        normalized = re.split(r"\W", snake_case)[0]
        return normalized

    def generate_row(self, values: List[str], headers: List[str], country: str) -> SpreadsheetRow:
        row_data = {"country_code": country}
        for key, value in zip(headers, values):
            row_data[key] = value

        row = SpreadsheetRow(**row_data)

        return row
