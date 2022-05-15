"""
Implemented use cases with dependencies injected

https://proofit404.github.io/dependencies/
"""
from dependencies import Injector

from adapters import spreadsheet_adapter
from usecases import convert_data
from services import google_sheets
from repositories import csv
from config import settings


class ConvertSpreadsheetData(Injector):
    usecase = convert_data.ConvertSpreadsheetData
    settings = settings.Settings(_env_file="config/.env.example")
    fetcher = google_sheets.GoogleSheetsService
    adapter = spreadsheet_adapter.SpreadsheetAdapter
    repository = csv.save_data_to_csv


class ConvertSpreadsheetDataLocally(ConvertSpreadsheetData):
    settings = settings.Settings(_env_file="config/.env")
