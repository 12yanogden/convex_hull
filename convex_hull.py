from LowerTangent import LowerTangent
from Point import Point
from UpperTangent import UpperTangent
from which_pyqt import PYQT_VER
from Hull import Hull

if PYQT_VER == 'PYQT5':
    from PyQt6.QtCore import QPointF, QObject
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


class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.view = None
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

    # Time: O(1) Space: O(n)
    def join_hulls(self, left_hull, right_hull, upper_tangent, lower_tangent):
        new_hull = Hull(left_hull.get_left_most(), right_hull.get_right_most())

        upper_tangent.stitch()
        lower_tangent.stitch()

        return new_hull

    # Time: O(nlogn) Space: O(n)
    def compute_hull_helper(self, points):
        if len(points) == 1:
            single_point = Point(points[0])
            new_hull = Hull(single_point, single_point)

            return new_hull

        middle_index = len(points) // 2

        left_hull = self.compute_hull_helper(points[:middle_index])                             # Time: O(nlogn) Space: O(n)
        right_hull = self.compute_hull_helper(points[middle_index:])                            # Time: O(nlogn) Space: O(n)

        upper_tangent = UpperTangent(left_hull.get_right_most(), right_hull.get_left_most())    # Time: O(n) Space: O(n)
        lower_tangent = LowerTangent(left_hull.get_right_most(), right_hull.get_left_most())    # Time: O(n) Space: O(n)

        return self.join_hulls(left_hull, right_hull, upper_tangent, lower_tangent)             # Time: O(1) Space: O(n)

    # Time: O(nlogn) Space: O(n)
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()

        # Sorts the points
        points.sort(key=lambda point: point.x())                # Time: O(nlogn) Space: O(n)

        t2 = time.time()

        t3 = time.time()

        # Returns lines
        polygon = self.compute_hull_helper(points).to_lines()   # Time: O(nlogn) Space: O(n)

        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.show_hull(polygon, RED)
        self.show_text('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
