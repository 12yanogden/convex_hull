from LowerTangent import LowerTangent
from UpperTangent import UpperTangent
from which_pyqt import PYQT_VER
from Hull import Hull

if PYQT_VER == 'PYQT5':
    from PyQt6.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
def get_x_from_point(point):
    return point.x()


class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def show_tangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def erase_tangent(self, line):
        self.view.clearLines(line)

    def blink_tangent(self, line, color):
        self.show_tangent(line, color)
        self.erase_tangent(line)

    def show_hull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def erase_hull(self, polygon):
        self.view.clearLines(polygon)

    def show_text(self, text):
        self.view.displayStatusText(text)

    def calc_right_most_index(self, points):
        right_most_index = 0

        for i in range(1, len(points)):
            if points[right_most_index].x() < points[i].x():
                right_most_index = i

        return right_most_index

    def join_hulls(self, left_hull, right_hull, upper_tangent, lower_tangent):
        left_hull_current_index = left_hull.get_left_most_index() + 1
        right_hull_current_index = upper_tangent.get_right_index()
        new_hull = Hull([left_hull.get_point_by_index(left_hull_current_index)])

        # Left most to upper left
        while left_hull_current_index < upper_tangent.get_left_index():
            new_hull.add_point(left_hull.get_point_by_index(left_hull_current_index))
            left_hull_current_index = left_hull.increment_index(left_hull_current_index)

        # Add upper tangent's left point
        new_hull.add_point(upper_tangent.get_left_point())

        # Upper right to lower right
        while right_hull_current_index < lower_tangent.get_right_index():
            new_hull.add_point(right_hull.get_point_by_index(right_hull_current_index))
            right_hull_current_index = right_hull.increment_index(right_hull_current_index)

        # Add lower tangent's right point
        new_hull.add_point(lower_tangent.get_right_point())

        # Set left_hull_current_index
        left_hull_current_index = lower_tangent.get_left_index()

        # Lower left to left most
        while left_hull_current_index != left_hull.get_left_most_index():
            new_hull.add_point(left_hull.get_point_by_index(left_hull_current_index))
            left_hull_current_index = left_hull.increment_index(left_hull_current_index)

        new_hull.update_right_most_index()

        self.erase_hull(left_hull.to_lines())
        self.erase_hull(right_hull.to_lines())
        self.show_hull(new_hull.to_lines(), RED)

        return new_hull

    def compute_hull_helper(self, points):
        if len(points) == 2 or len(points) == 3:
            new_hull = Hull(points)
            new_hull.order_clock()

            self.show_hull(new_hull.to_lines(), RED)

            return new_hull

        middle_index = len(points) // 2

        left_hull = self.compute_hull_helper(points[:middle_index])
        right_hull = self.compute_hull_helper(points[middle_index:])

        upper_tangent = UpperTangent(left_hull, right_hull)
        self.show_tangent(upper_tangent.to_line(), GREEN)

        lower_tangent = LowerTangent(left_hull, right_hull)
        self.show_tangent(lower_tangent.to_line(), GREEN)

        return self.join_hulls(left_hull, right_hull, upper_tangent, lower_tangent)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()

        # Sorts the points
        points.sort(key=get_x_from_point)

        t2 = time.time()

        t3 = time.time()

        # Returns lines
        polygon = self.compute_hull_helper(points).to_lines()

        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.show_hull(polygon, RED)
        self.show_text('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
