"""
Implemented use cases with dependencies injected

https://proofit404.github.io/dependencies/
"""
from dependencies import Injector

from adapters import spreadsheet_adapter
from usecases import convert_data
from services import google_sheets, geocoding
from repositories import csv
from config import settings


class ConvertSpreadsheetData(Injector):
    usecase = convert_data.ConvertSpreadsheetData
    settings = settings.Settings(_env_file="config/.env.example")
    reader = google_sheets.GoogleSheetsReader
    adapter = spreadsheet_adapter.SpreadsheetAdapter
    geocoder = geocoding.GeoCodingProcessor
    writer = csv.CSVWriter


class ConvertSpreadsheetDataLocally(ConvertSpreadsheetData):
    settings = settings.Settings(_env_file="config/.env")
