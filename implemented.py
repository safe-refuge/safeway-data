"""
Implemented use cases with dependencies injected

https://proofit404.github.io/dependencies/
"""
from dependencies import Injector

from adapters import spreadsheet
from usecases import convert_data
from services import google_sheets
from repositories import csv


class ConvertSpreadsheetData(Injector):
    usecase = convert_data.ConvertSpreadsheetData
    fetcher = google_sheets.GoogleSheetsService
    adapter =  spreadsheet.transform
    repository = csv.save_data_to_csv
