import pandas as pd
import quads

from quad_tree import RunQuadTree
from range_tree import RunRangeTree
from range_tree.RangePoint import RangePoint
from Kd_Trees.kdtree import *


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    print("Reading data...\n")
    df = read_data()
    print("Data successfully read.\n")
    print("Insert K value for the number of nearest neighbours\n")
    k = int(input())
    print("Insert D value for the number of Data you want to be included in the search\n")
    D = int(input())

    RunQuadTree.run(df[0:D], quads.Point(5.1, 5.1), k)
    RunRangeTree.run(df[0:D], RangePoint(5.1, 5.1, 0), k)
    run_kd(k, [5.1, 5.1], df[0:D], D)

