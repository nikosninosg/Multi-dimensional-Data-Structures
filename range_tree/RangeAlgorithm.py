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
    @staticmethod
    def get_knn(tree: TwoDRangeTree, point: RangePoint, k: int):
        points, visited_nodes = tree.query(point.x-0.5, point.x+0.5, point.y-0.5, point.y+0.5)
        while len(visited_nodes) != 0 and len(points) < k:
            node = visited_nodes.pop()
            contained_points = node.get_all_points()
            for current_point in contained_points:
                if current_point not in points:
                    points.append(current_point)

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))
        points = points[0:k]

        radius = point.euclidean_distance(points[k-1])
        x_range = [point.x - radius, point.x + radius]
        y_range = [point.y - radius, point.y + radius]

        points = tree.query(x_range[0], x_range[1], y_range[0], y_range[1])[0]

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))
        return points[0:k]

    @staticmethod
    def run(df, x: RangePoint, k: int):
        # ts = time.time()
        tree = TwoDRangeTree()
        # for index, row in df.iterrows():
        #     tree.insert(RangePoint(row['x'], row['y'], data=row['row_id']))
        tree.root = TwoDRangeTree.create_tree(df)
        # te = time.time()
        # dt = te - ts
        # print('Build')
        # print(dt)

        ts = time.time()
        points = RangeAlgorithm.get_knn(tree, x, k)
        te = time.time()
        dt = te - ts
        print('Algorithm')
        print(dt)

        for point in points:
            point.print()
        print("_________________")




