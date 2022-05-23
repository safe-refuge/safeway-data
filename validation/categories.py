from typing import Set

from config.constants import CATEGORIES
from models.point_of_interest import PointOfInterest
from validation import Validator


class CategoriesValidator(Validator):
    def is_valid(self, point: PointOfInterest) -> bool:
        return point.categories in CATEGORIES
