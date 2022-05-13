from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
DEFAULT_SPREADSHEET_ID = "1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0"
SAMPLE_RANGE_NAME = 'UA!A4:L5'

@dataclass
class GoogleSheetsService:
    def fetch(self) -> list:
        service = build('sheets', 'v4', developerKey="TBD")
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=DEFAULT_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        # TODO: implement
        return []
