import pandas as pd
import quads

from quad_tree import RunQuadTree
from range_tree import RunRangeTree
from range_tree.RangePoint import RangePoint


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    df = read_data()

    N = 10_000
    k = 5
    x = 5.1
    y = 5.1

    print('Quad Tree')
    RunQuadTree.run(df[0:N], point=quads.Point(x, y), k=k)

    print('2D Range Tree')
    RunRangeTree.run(df[0:N], point=RangePoint(x, y), k=k)


