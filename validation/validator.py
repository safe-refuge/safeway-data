class Validator:
    """
    Base class for all validators
    """
    def is_valid(self, point: 'models.PointOfInterest') -> bool:
        raise NotImplemented()
