from PyQt6.QtCore import QLineF, QPointF
from abc import ABC, abstractmethod


class Tangent(ABC):
    def __init__(self, left_hull, right_hull):
        self.left_hull = left_hull
        self.right_hull = right_hull
        self.left_index = left_hull.get_right_most_index()
        self.right_index = right_hull.get_left_most_index()

        self.orient()

    @abstractmethod
    def cycle_left(self):
        pass

    @abstractmethod
    def cycle_right(self):
        pass

    def orient(self):
        while True:
            left_cycle_count = self.cycle_left()
            right_cycle_count = self.cycle_right()

            if left_cycle_count == 0 and right_cycle_count == 0:
                break

    def get_left_index(self):
        return self.left_index

    def get_right_index(self):
        return self.right_index

    def get_left_point(self):
        return self.left_hull.get_point_by_index(self.left_index)

    def get_right_point(self):
        return self.right_hull.get_point_by_index(self.right_index)

    def get_slope(self):
        return self.get_left_point().y() - self.get_right_point().y() /\
               self.get_left_point().x() - self.get_right_point().x()

    def to_line(self):
        return QLineF(self.get_left_point(), self.get_right_point())
