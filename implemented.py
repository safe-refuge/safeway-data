"""
Implemented use cases with dependencies injected

https://proofit404.github.io/dependencies/
"""
from dependencies import Injector
from dependencies import Package

adapters = Package("adapters")
usecases = Package("usecases")
services = Package("services")
repositories = Package("repositories")


class ConvertSpreadsheetData(Injector):
    usecase = usecases.convert_data.ConvertSpreadsheetData
    fetcher = services.google_sheets.fetch_spreadsheet_data
    adapter =  adapters.spreadsheet.transform
    repository = repositories.csv.save_data_to_csv
