from dataclasses import dataclass
from typing import Callable

from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from returns.io import IOResult, impure_safe
from returns.pipeline import flow
from returns.pointfree import bind_ioresult

# If modifying these scopes, delete the file token.json.
from returns.result import safe
from returns.unsafe import unsafe_perform_io

from config.settings import Settings

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
DEFAULT_SPREADSHEET_ID = "1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0"
SAMPLE_RANGE_NAME = 'PL!A4:L'


@impure_safe
def make_request(request: HttpRequest) -> list:
    result = request.execute()
    return result['values']


@dataclass
class GoogleSheetsService:

    # Injected dependencies
    settings: Settings
    make_request: Callable = make_request

    def fetch(self) -> list:
        service = build('sheets', 'v4', developerKey="AIzaSyDGCDWPMyHsS19-cs2TZ9OkGd06fZac3Eo")
        request: HttpRequest = service.spreadsheets().values().get(
            spreadsheetId=DEFAULT_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME)

        result = flow(request, self.make_request, bind_ioresult(self.process_response))
        # result.failure()._inner_value.reason
        # TODO: implement

        perform_io = unsafe_perform_io(result)
        return []

    @safe
    def process_response(self, response: list) -> list:
        return response
