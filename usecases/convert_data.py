import logging

from dataclasses import dataclass

from returns._internal.pipeline.flow import flow
from returns.pointfree import bind_ioresult
from returns.unsafe import unsafe_perform_io

from adapters.spreadsheet_adapter import SpreadsheetAdapter
from config.settings import Settings
from repositories.csv import CSVWriter
from services.geocoding import GeoCodingProcessor
from services.google_sheets import GoogleSheetsReader

logger = logging.getLogger(__name__)


@dataclass
class ConvertSpreadsheetData:
    """
    We need to:

    - load data from a source
    - convert to the desired format
    - save
    """

    # Injected dependencies
    settings: Settings
    reader: GoogleSheetsReader
    adapter: SpreadsheetAdapter
    geocoder: GeoCodingProcessor
    writer: CSVWriter

    def convert(self):
        result = flow(
            self.settings.spreadsheet_id,
            self.reader.fetch,
            bind_ioresult(self.adapter.transform),
            self.geocoder.enhance,
            bind_ioresult(self.writer.write)
        )
        # TODO: deal with failures
        # result.failure()._inner_value.reason
        # perform_io = unsafe_perform_io(result)

        saved_data = unsafe_perform_io(result).unwrap()

        return saved_data
