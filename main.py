import pandas as pd
from quad_tree import QuadTree
from range_tree.RangePoint import RangePoint
from range_tree.RangeTree import RangeTree
from range_tree.Utils import *
from range_tree.TwoDRangeTree import TwoDRangeTree


def read_data():
    ret_df = pd.read_csv("Data/train_x_y_10K.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    # df = read_data()
    # print(df[0:3])
    # QuadTree.run(df[0:100000])  # it runs well with 10^5 items and it runs ok with 10^6 items
    points = [
        RangePoint(5, 9, 0),
        RangePoint(7, 3, 0),
        RangePoint(3, 8, 0),
        RangePoint(6, 7, 0),
        RangePoint(4, 2, 0),
        RangePoint(8, 1, 0),
        RangePoint(1, 5, 0),
        RangePoint(9, 4, 0)
    ]
    tree = TwoDRangeTree()
    for point in points:
        tree.insert(point)
    tree.root.printNode()
    print("_________________")
    tree.root.tree.root.printNode()
