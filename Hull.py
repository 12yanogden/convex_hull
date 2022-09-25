from PyQt6.QtCore import QLineF


class Hull:
    def __init__(self, points):
        self.points = points
        self.right_most_index = 0

        self.update_right_most_index()

    def add_point(self, point):
        self.points.append(point)

    def get_point_by_index(self, i):
        return self.points[i]

    def get_left_most(self):
        return self.points[self.get_left_most_index()]

    def get_right_most(self):
        return self.points[self.get_right_most_index()]

    def get_left_most_index(self):
        return 0

    def get_right_most_index(self):
        return self.right_most_index

    def slope_by_indexes(self, left, right):
        return self.points[left].y() - self.points[right].y() /\
               self.points[left].x() - self.points[right].x()

    def switch_points(self, index1, index2):
        tmp = self.points[index1]
        self.points[index1] = self.points[index2]
        self.points[index2] = tmp

    def order_clock(self):
        if len(self.points) == 3 and self.slope_by_indexes(0, 1) < self.slope_by_indexes(0, 2):
            self.switch_points(1, 2)

    def to_lines(self):
        lines = []

        for i in range(len(self.points)):
            if i == (len(self.points) - 1):
                lines.append(QLineF(self.points[i], self.points[0]))
            else:
                lines.append(QLineF(self.points[i], self.points[i + 1]))

        return lines

    def increment_index(self, i):
        incremented_index = i + 1

        if i == (len(self.points) - 1):
            incremented_index = 0

        return incremented_index

    def decrement_index(self, i):
        decremented_index = i - 1

        if i == 0:
            decremented_index = len(self.points) - 1

        return decremented_index

    def cycle_right_most_index_clock(self, right_most_index):
        while self.points[right_most_index].x() < self.points[self.increment_index(right_most_index)].x():
            right_most_index = self.increment_index(right_most_index)

        return right_most_index

    def cycle_right_most_index_counter(self, right_most_index):
        while self.points[right_most_index].x() < self.points[self.decrement_index(right_most_index)].x():
            right_most_index = self.decrement_index(right_most_index)

        return right_most_index

    def update_right_most_index(self):
        right_most_index = len(self.points) // 2
        right_most_index = self.cycle_right_most_index_clock(right_most_index)
        right_most_index = self.cycle_right_most_index_counter(right_most_index)

        self.right_most_index = right_most_index





