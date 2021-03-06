import logging

from dataclasses import dataclass

from returns._internal.pipeline.flow import flow
from returns.pointfree import bind_ioresult
from returns.primitives.tracing import collect_traces
from returns.unsafe import unsafe_perform_io

from adapters.spreadsheet_adapter import SpreadsheetAdapter
from config.settings import Settings
from repositories.csv import CSVRepository
from services.address_sanitizer import AddressSanitizer
from services.geocoding import GeoCodingProcessor
from services.google_sheets import GoogleSheetsReader
from services.translation import PointTranslator
from validation.composite_validator import CompositeValidator
from validation.error_collector import ErrorCollector

logger = logging.getLogger(__name__)


@dataclass
class ConvertSpreadsheetData:
    """
    We need to:

    - load data from a source
    - convert to the desired format
    - validate and enhance if necessary
    - save
    """

    # Injected dependencies
    settings: Settings
    spreadsheet_reader: GoogleSheetsReader
    adapter: SpreadsheetAdapter
    address_sanitizer: AddressSanitizer    
    geocoder: GeoCodingProcessor
    translator: PointTranslator
    error_collector: ErrorCollector
    validator: CompositeValidator
    csv_repository: CSVRepository

    def convert_spreadsheet(self, spreadsheet_id: str = None):
        self.error_collector.clear()

        result = flow(
            spreadsheet_id or self.settings.spreadsheet_id,

            # Fetch list of spreadsheet rows from a Google Sheet
            self.spreadsheet_reader.fetch,

            # Transform list of spreadsheet rows to list of Points of Interest
            self.adapter.transform,

            # Optionally, sanitize addresses
            self.address_sanitizer.sanitize,

            # Find missing coordinates by geocoding addresses
            self.geocoder.enhance,

            # Translate city names to English
            self.translator.translate,

            # Validate the final list of points
            self.validator.validate,

            # Save points to a CSV file
            self.csv_repository.write
        )

        # TODO: deal with failures and invalid points
        invalid_points = self.error_collector.invalid_points

        return result

    def convert_file(self, input_file: str = None):
        self.error_collector.clear()

        result = flow(
            input_file,

            # Fetch list of points of interest from the input CSV file
            self.csv_repository.read,

            # Optionally, sanitize addresses
            self.address_sanitizer.sanitize,

            # Find missing coordinates by geocoding addresses
            self.geocoder.enhance,

            # Translate city names to English
            self.translator.translate,

            # Validate the final list of points
            self.validator.validate,

            # Save points to a CSV file
            self.csv_repository.write
        )

        # TODO: deal with failures and invalid points
        invalid_points = self.error_collector.invalid_points

        return result
