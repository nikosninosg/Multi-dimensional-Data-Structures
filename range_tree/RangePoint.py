from math import sqrt


class RangePoint:

    def __init__(self, x: float, y: float, data: float):
        self.x = x
        self.y = y
        self.data = data

    def euclidean_compare(self, other_point):
        return (self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2

    def euclidean_distance(self, other_point):
        return sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

    def print(self):
        print('(' + str(self.x) + ' ' + str(self.y) + ')')
