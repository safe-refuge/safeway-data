from models.point_of_interest import PointOfInterest


class Validator:
    """
    Base class for all validators
    """
    def is_valid(self, point: PointOfInterest) -> bool:
        raise NotImplemented()
