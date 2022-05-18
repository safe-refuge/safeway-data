from dataclasses import dataclass
from typing import List

from models.point_of_interest import PointOfInterest
from validation import Validator
from validation.error_collector import ErrorCollector


@dataclass
class CompositeValidator:

    # Injected dependencies
    error_collector: ErrorCollector
    validators: List[Validator]

    def validate(self, source: List[PointOfInterest]) -> List[PointOfInterest]:
        valid_points = []
        for point in source:
            if all([validator.is_valid(point) for validator in self.validators]):
                valid_points.append(point)
            else:
                self.error_collector.add(point)

        return valid_points

