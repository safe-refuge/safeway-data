import logging

from dataclasses import dataclass
from typing import Callable, Optional


logger = logging.getLogger(__name__)


@dataclass
class ConvertSpreadsheetData:
    """
    We need to:

    - load data from a source
    - convert to the desired format
    - save
    """

    # Dependencies
    fetcher: Callable
    adapter: Callable
    repository: Callable

    def convert(self, output: str):
        self.output = output
        self.fetch_source_data()
        self.transform_data()
        self.persist()
        return self.transformed_data

    def fetch_source_data(self):
        # TODO: implement
        self.source_data = self.fetcher()

    def transform_data(self):
        # TODO: implement
        self.transformed_data = self.adapter(self.source_data)

    def persist(self):
        # TODO: implement
        self.repository(self.transformed_data)
