import pandas as pd
import quads

from quad_tree import QuadTree
from range_tree.RangeAlgorithm import RangeAlgorithm
from range_tree.RangePoint import RangePoint
from range_tree.RangeTree import RangeTree
from range_tree.Utils import *
from range_tree.TwoDRangeTree import TwoDRangeTree


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    df = read_data()

    # it runs well with 10^5 items and it runs ok with 10^6 items
    # print('Quad Tree')
    # QuadTree.run(df[0:100000], x=quads.Point(7.31, 2.8), k=4)

    print('2D Range Tree')
    RangeAlgorithm.run(df[0:100000], x=RangePoint(7.31, 2.8, 0), k=4)

    # points = [
    #     RangePoint(5, 9, 0),
    #     RangePoint(7, 3, 0),
    #     RangePoint(3, 8, 0),
    #     RangePoint(8, 7, 0),
    #     RangePoint(8, 2, 0),
    #     RangePoint(8, 1, 0),
    #     RangePoint(1, 5, 0),
    #     RangePoint(9, 4, 0)
    # ]
    # tree = TwoDRangeTree()
    # for point in points:
    #     tree.insert(point)
    # tree.root.printNode()
    # print("_________________")
    # tree.root.tree.root.printNode()

    # df = read_data()
    # QuadTree.run(df[0:1000000])

    # tree = TwoDRangeTree()
    # for point in points:
    #     tree.insert(point)
    # queryPoints, visitedNodes = tree.query(8, 8, 1, 1)
    # print('___________________________')
    # for point in queryPoints:
    #     print('x')
    #     print(point.x)
    #     print('y')
    #     print(point.y)
    #     print('___________________________')

    # new_points = RangeAlgorithm.get_knn(tree, RangePoint(8, 1, 0), 4)
    # for point in new_points:
    #     point.print()
    #     print('___________________________')
    #
    # print('CHANGE')
    #
    # for point in points:
    #     point.print()
    #     print(point.euclidean_compare(RangePoint(8, 1, 0)))
    #
    # points2 = [
    #     RangePoint(8, 7, 0),
    #     RangePoint(8, 2, 0),
    #     RangePoint(8, 1, 0),
    #     RangePoint(9, 4, 0)
    # ]

    # tree2 = RangeTree()
    # for point in points2:
    #     tree2.insert(point)
    # queryPoints2 = tree2.query(1, 1)
    # print('___________________________')
    # for point in queryPoints2:
    #     print('x')
    #     print(point.x)
    #     print('y')
    #     print(point.y)
