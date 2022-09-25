from Tangent import Tangent


class UpperTangent(Tangent):
    def cycle_left(self):
        least_slope = self.get_slope()
        cycle_count = 0

        self.left_index = self.left_hull.decrement_index(self.left_index)

        while self.get_slope() < least_slope:
            self.left_index = self.left_hull.decrement_index(self.left_index)
            cycle_count = cycle_count + 1

        self.left_index = self.left_hull.increment_index(self.left_index)

        return cycle_count

    def cycle_right(self):
        greatest_slope = self.get_slope()
        cycle_count = 0

        self.right_index = self.right_hull.increment_index(self.right_index)

        while self.get_slope() > greatest_slope:
            self.right_index = self.right_hull.increment_index(self.right_index)
            cycle_count = cycle_count + 1

        self.right_index = self.right_hull.decrement_index(self.right_index)

        return cycle_count
