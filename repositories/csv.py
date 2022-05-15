import csv
from dataclasses import dataclass
from typing import List, Callable, TextIO

from returns.io import impure_safe

from config.settings import Settings
from models.point_of_interest import PointOfInterest


def open_file(path: str) -> TextIO:
    return open(path, "w")


def close_file(file: TextIO):
    file.close()


@dataclass
class CSVWriter:

    # Injected dependencies
    settings: Settings
    open_file: Callable = open_file
    close_file: Callable = close_file

    @impure_safe
    def write(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        fieldnames = list(PointOfInterest.schema()["properties"].keys())
        file = self.open_file(self.settings.output_file)

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.dict())

        self.close_file(file)

        return entries
