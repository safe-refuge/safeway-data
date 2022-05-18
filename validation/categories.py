from typing import Set

from models.point_of_interest import PointOfInterest
from validation import Validator


class CategoriesValidator(Validator):
    ALLOWED_CATEGORIES: Set[str] = {
        "Clothes",
        "Accommodation",
        "Medical",
        "Border Crossing",
        "Pharmacy",
        "Finance",
        "Information",
        "Mental help",
        "Transport",
        "Food",
        "Electronics",
        "Children"
    }

    def is_valid(self, point: PointOfInterest) -> bool:
        return point.categories in self.ALLOWED_CATEGORIES
