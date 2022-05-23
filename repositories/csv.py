import csv
from dataclasses import dataclass
from typing import List, Callable, TextIO

from config.settings import Settings
from models.point_of_interest import PointOfInterest


def open_file(path: str) -> TextIO:
    return open(path, "w", encoding='utf-8-sig', newline='')


def open_read_only_file(path: str) -> TextIO:
    return open(path, "r", encoding='utf-8-sig')


def close_file(file: TextIO):
    file.close()


@dataclass
class CSVRepository:

    # Injected dependencies
    settings: Settings
    open_file: Callable = open_file
    open_read_only_file: Callable = open_read_only_file
    close_file: Callable = close_file

    def write(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        fieldnames = list(PointOfInterest.schema()["properties"].keys())
        file = self.open_file(self.settings.output_file)

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.dict())

        self.close_file(file)

        return entries

    def read(self, input_file: str) -> List[PointOfInterest]:
        file = self.open_read_only_file(input_file)

        reader: csv.DictReader = csv.DictReader(file)

        entries: List[PointOfInterest] = []
        reader.__next__()  # skip header
        for row in reader:
            entries.append(PointOfInterest(**row))

        self.close_file(file)

        return entries
