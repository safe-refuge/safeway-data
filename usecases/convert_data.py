import logging

from dataclasses import dataclass
from typing import Callable

from returns._internal.pipeline.flow import flow
from returns.pointfree import bind_ioresult, bind, map_
from returns.unsafe import unsafe_perform_io

from adapters.spreadsheet_adapter import SpreadsheetAdapter
from config.settings import Settings

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
    fetcher: Callable
    adapter: SpreadsheetAdapter
    repository: Callable

    def convert(self, output: str):
        result = flow(
            self.settings.spreadsheet_id,
            self.fetcher.fetch,
            bind_ioresult(self.adapter.transform),
            self.repository
        )
        # TODO: deal with failures
        # result.failure()._inner_value.reason
        # perform_io = unsafe_perform_io(result)
        # saved_data = unsafe_perform_io(result)

        return result
