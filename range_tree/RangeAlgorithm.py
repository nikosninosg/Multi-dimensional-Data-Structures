import time

from range_tree.TwoDRangeTree import TwoDRangeTree
from range_tree.RangeTree import RangeTree
from math import *
from range_tree.RangePoint import RangePoint


# class Circle:
#     center: RangePoint
#     radius: float
#
#     def __init__(self, center: RangePoint, radius: float):
#         self.center = center
#         self.radius = radius
#
#
class RangeAlgorithm:
    # x1: int
    # x2: int
    # tree: TwoDRangeTree
    # c: Circle
    # node: RangeNode
    # point_list: []
    #
    # def __init__(self, tree: TwoDRangeTree, point: RangePoint):
        # self.tree = tree
        # self.c = Circle(point, sqrt(tree.width ** 2 + tree.height ** 2))
        # self.stack = []
        # self.point_list = []

    # def process(self, point: RangePoint, node: RangeNode, point_list, k):
    #     if k == 'x':
    #         while not node.isLeaf():
    #             if point.x < node.w:
    #                 point_list.append(node)
    #                 self.node = node.l_child
    #             elif point.x > node.w:
    #                 point_list.append(node)
    #                 self.node = node.r_child
    #             else:
    #                 self.process(point, node, k='y')
    #     elif k == 'y':
    #         while not node.tree.isLeaf():
    #             if point.y < node.w:
    #                 point_list.append(node)
    #                 self.node = node.l_child
    #             elif point.y > node.w:
    #                 point_list.append(node)
    #                 self.node = node.r_child
    #             else:
    #                 break

    @staticmethod
    def get_knn(tree: TwoDRangeTree, point: RangePoint, k: int):
        points, visited_nodes = tree.query(point.x, point.x, point.y, point.y)

        while len(visited_nodes) != 0 and len(points) < k:
            node = visited_nodes.pop()
            contained_points = node.get_all_points()
            for current_point in contained_points:
                if current_point not in points:
                    points.append(current_point)

        # te = time.time()
        # dt = te - ts
        # print(dt)

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))

        # te = time.time()
        # dt = te - ts
        # print(dt)

        ts = time.time()

        points = points[0:k]
        radius = point.euclidean_distance(points[k-1])
        x_range = [point.x - radius, point.x + radius]
        y_range = [point.y - radius, point.y + radius]
        points = tree.query(x_range[0], x_range[1], y_range[0], y_range[1])[0]

        te = time.time()
        dt = te - ts
        print(dt)

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))

        # te = time.time()
        # dt = te - ts
        # print(dt)

        return points[0:k]

    @staticmethod
    def run(df, x: RangePoint, k: int):
        tree = TwoDRangeTree()
        for index, row in df.iterrows():
            tree.insert(RangePoint(row['x'], row['y'], data=row['row_id']))
        points = RangeAlgorithm.get_knn(tree, x, k)
        for point in points:
            point.print()
        print("_________________")




