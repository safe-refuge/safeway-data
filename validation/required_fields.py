from typing import Set, Callable

from validation import Validator


class RequiredFieldsValidator(Validator):
    REQUIRED: Set[str] = {"name", "city", "country", "address", "lat", "lng", "phone"}

    def __init__(self, log: Callable = print):
        self.log = log

    def is_valid(self, point: 'models.PointOfInterest') -> bool:
        for field in self.REQUIRED:
            if not point.__getattribute__(field):
                self.log(f"Failed to validate point: field '{field}' is missing from point {point}")
                return False

        return True
