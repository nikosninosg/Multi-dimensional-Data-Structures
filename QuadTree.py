import time
from math import sqrt
import quads
from Circle import Circle
from matplotlib import pyplot as plt
import QuadTreeStructure
from QuadKnnAlgorithm import QuadKnnAlgorithm
from LocalQuadTree import LocalQuadTree

def run(df):
    x = quads.Point(5, 5)
    k = 4

    tree = LocalQuadTree((5, 5), 10, 10)
    for index, row in df.iterrows():
        tree.insert(quads.Point(row['x'], row['y'], data=row['row_id']))
    ts = time.time()
    alg = QuadKnnAlgorithm(tree, x, k)
    list1 = alg.nn_query()
    te = time.time()
    dt = te - ts
    print(dt)
    print(list1)
    print("_________________")

    # library
    tree = quads.QuadTree((5, 5), 10, 10)
    for index, row in df.iterrows():
        tree.insert(quads.Point(row['x'], row['y'], data=row['row_id']))
    ts = time.time()
    list2 = tree.nearest_neighbors(x, k)
    te = time.time()
    dt = te - ts
    print(dt)
    print(list2)
    print("_________________")


