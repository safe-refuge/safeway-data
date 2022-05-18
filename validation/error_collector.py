from typing import List

from models.point_of_interest import PointOfInterest


class ErrorCollector:
    def __init__(self):
        self._invalid_points: List[PointOfInterest] = []

    def clear(self):
        self._invalid_points = []

    def add(self, point: PointOfInterest):
        self._invalid_points.append(point)

    @property
    def invalid_points(self):
        return self._invalid_points
