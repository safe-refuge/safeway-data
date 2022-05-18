from typing import Set

from models.point_of_interest import PointOfInterest
from validation import Validator


class RequiredFieldsValidator(Validator):
    # TODO: Validate "country"
    REQUIRED: Set[str] = {"name", "city", "address", "lat", "lng"}

    def is_valid(self, point: PointOfInterest) -> bool:
        for field in self.REQUIRED:
            if not point.__getattribute__(field):
                return False

        return True
