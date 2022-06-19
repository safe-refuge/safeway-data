from config.constants import CATEGORIES
from validation import Validator


class CategoriesValidator(Validator):
    def is_valid(self, point: 'models.PointOfInterest') -> bool:
        for cat in point.categories:
            if cat not in CATEGORIES:
                return False
        return True
