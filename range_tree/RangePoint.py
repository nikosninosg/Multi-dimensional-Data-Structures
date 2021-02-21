from math import sqrt


class RangePoint:
    """
    A class that represents a point. This class is used to represent 2-dimensional data.
    It contains the following attributes.
    - x: The x coordinate of the point (1st dimension).
    - y: The y coordinate of the point (2nd dimension).
    - data: An optional value that represents the data of this point.
    """

    def __init__(self, x: float, y: float, data: float = 0):
        """
        The constructor creates a new point with data passed as arguments.

        :param x: The x coordinate of the point (1st dimension).
        :param y: The y coordinate of the point (2nd dimension).
        :param data: An optional value that represents the data of this point. If left empty the default is 0.
        """
        self.x = x
        self.y = y
        self.data = data

    def euclidean_compare(self, other_point):
        """
        This method calculate the euclidean distance between 2 points, but without the square root. It is can be used to
        compare the distance between 2 points faster but not to calculate the actual distance.

        :param other_point: The other point to calculate the distance from.
        :return: The euclidean distance without the square root.
        """
        return (self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2

    def euclidean_distance(self, other_point):
        """
        This method calculate the euclidean distance between 2 points.

        :param other_point: The other point to calculate the euclidean distance from.
        :return: The euclidean distance.
        """
        return sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

    def print(self):
        """
        This method prints the x and y coordinates of the point.
        """
        print('(' + str(self.x) + ' ' + str(self.y) + ')')
