class Point:
    def __init__(self, point):
        self.point = point

        self.clock_point = self
        self.counter_point = self

    def get_clock(self):
        return self.clock_point

    def get_counter(self):
        return self.counter_point

    def set_clock(self, clock):
        self.clock_point = clock

    def set_counter(self, counter):
        self.counter_point = counter

    def x(self):
        return self.point.x()

    def y(self):
        return self.point.y()

    def to_qpointf(self):
        return self.point
