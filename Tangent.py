from PyQt6.QtCore import QLineF
from abc import ABC, abstractmethod


class Tangent(ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right

        self.orient()

    @abstractmethod
    def cycle_left(self):
        pass

    @abstractmethod
    def cycle_right(self):
        pass

    # Time: O(n) Space: O(n)
    def orient(self):
        while True:
            left_cycle_count = self.cycle_left()                    # Time: O(n) Space: O(n)
            right_cycle_count = self.cycle_right()                  # Time: O(n) Space: O(n)

            if left_cycle_count == 0 and right_cycle_count == 0:
                break

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    @abstractmethod
    def stitch(self):
        pass

    def get_slope(self):
        return (self.left.y() - self.right.y()) / \
               (self.left.x() - self.right.x())

    def to_line(self):
        return QLineF(self.left.to_qpointf(), self.right.to_qpointf())
