from dataclasses import dataclass
from typing import List, Callable


from config.settings import Settings
from models.point_of_interest import PointOfInterest


@dataclass
class DummyWriter:

    # Injected dependencies
    settings: Settings
    open_file: Callable = lambda x: x
    close_file: Callable = lambda x: x

    def write(self, entries: List[PointOfInterest]) -> List[PointOfInterest]:
        for entry in entries:
            print(entry.dict())

        return entries
