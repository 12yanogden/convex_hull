from Tangent import Tangent


# Time: O(n) Space: O(n)
class LowerTangent(Tangent):
    def cycle_left(self):
        greatest_slope = self.get_slope()
        cycle_count = 0

        self.left = self.left.get_clock()

        while self.get_slope() > greatest_slope:    # Time: O(n) Space: O(n)
            greatest_slope = self.get_slope()

            self.left = self.left.get_clock()
            cycle_count += 1

        self.left = self.left.get_counter()

        return cycle_count

    # Time: O(n) Space: O(n)
    def cycle_right(self):
        least_slope = self.get_slope()
        cycle_count = 0

        self.right = self.right.get_counter()

        while self.get_slope() < least_slope:       # Time: O(n) Space: O(n)
            least_slope = self.get_slope()

            self.right = self.right.get_counter()
            cycle_count += 1

        self.right = self.right.get_clock()

        return cycle_count

    # Time: O(1) Space: O(n)
    def stitch(self):
        self.left.set_counter(self.right)
        self.right.set_clock(self.left)

        if self.left.get_clock == self.left:
            self.left.set_clock(self.right)

        if self.right.get_counter == self.right:
            self.right.set_counter(self.left)
