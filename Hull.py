from PyQt6.QtCore import QLineF


class Hull:
    def __init__(self, left_most, right_most):
        self.left_most = left_most
        self.right_most = right_most

    def get_left_most(self):
        return self.left_most

    def get_right_most(self):
        return self.right_most

    # Time: O(n) Space: O(n)
    def to_lines(self):
        lines = []
        current_point = self.left_most.get_clock()

        # Adds first line
        lines.append(QLineF(self.left_most.to_qpointf(), current_point.to_qpointf()))

        # Adds other lines
        while current_point != self.left_most:
            lines.append(QLineF(current_point.to_qpointf(), current_point.get_clock().to_qpointf()))
            current_point = current_point.get_clock()

        return lines





