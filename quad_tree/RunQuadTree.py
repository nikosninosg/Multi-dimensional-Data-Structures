import time
import quads
from quad_tree.LocalQuadTree import LocalQuadTree


def run(df, point: quads.Point, k: int):
    """
    This is a function that runs the knn algorithms in a Quad Tree using two implementations of the algorithm.
    The first implementation is the one developed by us and the second implementation is the one already provided by 
    the library quads.
    
    The function prints both the time needed to run the algorithm and the points returned.
    The function does not take under consideration the time needed to create the data structure.
    
    :param df: A pandas dataframe containing the points of the dataset.
    :param point: The point whose nearest neighbors we are looking for.
    :param k: The number of neighbors we want to find.
    """
    # "local" implementation
    tree = LocalQuadTree((5, 5), 10, 10)
    for index, row in df.iterrows():
        tree.insert(quads.Point(row['x'], row['y'], data=row['row_id']))
    ts = time.time()
    list1 = tree.get_knn(point, k)
    te = time.time()
    dt = te - ts
    print('Quad Algorithm')
    print(round(dt, 6))
    print(list1)
    print("_________________")

    # library
    tree = quads.QuadTree((5, 5), 10, 10)
    for index, row in df.iterrows():
        tree.insert(quads.Point(row['x'], row['y'], data=row['row_id']))
    ts = time.time()
    list2 = tree.nearest_neighbors(point, k)
    te = time.time()
    dt = te - ts
    list2.sort(key=lambda point_in_list: quads.euclidean_compare(point, point_in_list))
    print('Quad Library')
    print(round(dt, 6))
    print(list2)
    print("_________________")
