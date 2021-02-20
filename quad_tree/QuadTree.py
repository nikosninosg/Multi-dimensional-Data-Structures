import time
from math import sqrt
import quads
from matplotlib import pyplot as plt
from quad_tree.Circle import Circle
import quad_tree.QuadTreeStructure
from quad_tree.QuadKnnAlgorithm import QuadKnnAlgorithm
from quad_tree.LocalQuadTree import LocalQuadTree


def run(df, x: quads.Point, k: int):
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

    # second implementation
    tree = LocalQuadTree((5, 5), 10, 10)
    for index, row in df.iterrows():
        tree.insert(quads.Point(row['x'], row['y'], data=row['row_id']))
    ts = time.time()
    list3 = tree.get_nn(x, k)
    te = time.time()
    dt = te - ts
    print(dt)
    print(list3)
    print("_________________")
