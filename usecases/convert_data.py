import logging

from dataclasses import dataclass

from returns._internal.pipeline.flow import flow
from returns.pointfree import bind_ioresult
from returns.primitives.tracing import collect_traces
from returns.unsafe import unsafe_perform_io

from adapters.spreadsheet_adapter import SpreadsheetAdapter
from config.settings import Settings
from repositories.csv import CSVRepository
from services.geocoding import GeoCodingProcessor
from services.google_sheets import GoogleSheetsReader
from services.translation import CityTranslator
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
    geocoder: GeoCodingProcessor
    translator: CityTranslator
    error_collector: ErrorCollector
    validator: CompositeValidator
    csv_repository: CSVRepository

    def convert_spreadsheet(self, spreadsheet_id: str = None):
        self.error_collector.clear()

        result = flow(
            spreadsheet_id or self.settings.spreadsheet_id,
            self.spreadsheet_reader.fetch,
            bind_ioresult(self.adapter.transform),
            self.geocoder.enhance,
            bind_ioresult(self.translator.translate),
            bind_ioresult(self.validator.validate),
            self.csv_repository.write
        )
        # TODO: deal with failures
        # result.failure()._inner_value.reason
        # perform_io = unsafe_perform_io(result)

        invalid_points = self.error_collector.invalid_points

        saved_data = unsafe_perform_io(result).unwrap()

        return saved_data

    @collect_traces
    def convert_file(self, input_file: str = None):
        self.error_collector.clear()

        result = flow(
            input_file,
            self.csv_repository.read,
            bind_ioresult(self.geocoder.enhance),
            bind_ioresult(self.translator.translate),
            bind_ioresult(self.validator.validate),
            self.csv_repository.write
        )

        invalid_points = self.error_collector.invalid_points

        saved_data = unsafe_perform_io(result).unwrap()

        return saved_data
