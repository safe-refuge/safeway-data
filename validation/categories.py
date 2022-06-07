from config.constants import CATEGORIES
from models.point_of_interest import PointOfInterest
from validation import Validator


class CategoriesValidator(Validator):
    def is_valid(self, point: PointOfInterest) -> bool:
        for cat in point.categories:
            if cat not in CATEGORIES:
                return False
        return True
