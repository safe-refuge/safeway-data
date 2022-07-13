from typing import Callable

from config.constants import CATEGORIES
from validation import Validator


class CategoriesValidator(Validator):

    def __init__(self, log: Callable = print):
        self.log = log

    def is_valid(self, point: 'models.PointOfInterest') -> bool:
        for cat in point.categories:
            if cat not in CATEGORIES:
                self.log(f"Failed to validate point: category '{cat}' is invalid in {point}")
                return False
        return True
