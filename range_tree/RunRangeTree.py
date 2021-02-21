import time

from range_tree.TwoDRangeTree import TwoDRangeTree
from range_tree.RangePoint import RangePoint


def run(df, point: RangePoint, k: int):
    """
    This is a function that runs the knn algorithms in a Range Tree using the implementation of the algorithm we
    developed for the data structure we created.

    The function prints both the time needed to run the algorithm and the points returned.
    The function does not take under consideration the time needed to create the data structure.

    :param df: A pandas dataframe containing the points of the dataset.
    :param point: The point whose nearest neighbors we are looking for.
    :param k: The number of neighbors we want to find.
    """
    tree = TwoDRangeTree(df)

    ts = time.time()
    points = tree.get_knn(point, k)
    te = time.time()
    dt = te - ts
    print(round(dt, 6))

    for point in points:
        point.print()
    print("_________________")
