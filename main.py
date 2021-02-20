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
    print('Quad Tree')
    QuadTree.run(df[0:100000], x=quads.Point(5.1, 5.1), k=10)

    print('2D Range Tree')
    RangeAlgorithm.run(df[0:100000], x=RangePoint(5.1, 5.1), k=4)

    # tree = RangeTree()
    # tree.root = tree.create_tree(df)
    # for point in tree.root.l_child.r_child.points:
    #     point.print()

    # tree = TwoDRangeTree()
    # tree.root = TwoDRangeTree.create_tree(df)
    #
    # for point in tree.root.tree.root.points:
    #     point.print()


