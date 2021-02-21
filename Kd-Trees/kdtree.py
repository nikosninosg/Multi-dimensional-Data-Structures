import cProfile
import pandas as pd


# Makes the KD-Tree
def make_kd_tree(df_points, dimensions, i=0):
    """
    This method creates a KD tree from a given dataset which is represented as a dataframe. In addition the method
    allows you to choose the number of dimensions of the tree (we will be using 2 dimensions here).

    The method is using a recursive algorithm to create the tree.
    Specifically it separates the dataset in half and then calls itself in each of the 2 pairs. This way it will create
    2 trees (one from each part) and it will set as the children of the current node the roots of the 2 trees.

    In each recursive call the variable i, which shows which dimension will be used to sort the points is changing, in
    order to properly arrange the points of the KD tree.

    The recursive calls will stop when the passed dataset contains only 1 point, in which case a node will be returned
    containing this point.

    In this tree the nodes are represented as lists, instead of as individual classes and the data are stored in all the
    nodes, not only on the leaves.

    :param df_points: A dataframe containing the dataset to add in the tree.
    :param dimensions: The number of the dimensions of the points (eg 2 for 2-dimensional points).
    :param i: A number showing us which dimension should be used to sort the points in its level.
    :return: The root of the created tree.
    """
    if len(df_points) > 1:
        df_points.sort(key=lambda x: x[i])
        i = (i + 1) % dimensions
        half = len(df_points) >> 1
        return [
            make_kd_tree(df_points[: half], dimensions, i),
            make_kd_tree(df_points[half + 1:], dimensions, i),
            df_points[half]
        ]
    elif len(df_points) == 1:
        return [None, None, df_points[0]]


# k nearest neighbors
def get_knn(kd_node, point, k, dimensions, dist_func, return_distances=True, i=0, heap=None):
    """
    This is a method to calculate the k nearest neighbors of a given point.
    The algorithm "walks" down the tree comparing the point of the current node with the given point. It stores the k
    nearest neighbors at a heap at all times (meaning that if the heap already has k elements it will replace one if a
    nearest one is found).
    In order to "walk" down the whole tree and take advantage of the change in the main dimension which happens in the
    KD trees the algorithm uses recursion but it doesn't always visits both children of a node.

    :param kd_node: The root of the tree (or sub-tree) currently visited and the current node which is being processed.
    :param point: The point whose nearest neighbors we are looking for.
    :param k: The number of the neighbors we are looking for.
    :param dimensions: The number of the dimensions of the points.
    :param dist_func: The functions used to calculate the distance.
    :param return_distances: Whether or not the distance of each point to the given one should be returned.
    :param i: A number showing us which dimension should be used to sort the points in its level.
    :param heap: A heap containing the nearest neighbors.
    :return: A list containing the k nearest neighbors.
    """
    import heapq
    is_root = not heap
    if is_root:
        heap = []
    if kd_node is not None:
        dist = dist_func(point, kd_node[2])
        dx = kd_node[2][i] - point[i]
        if len(heap) < k:
            heapq.heappush(heap, (-dist, kd_node[2]))
        elif dist < -heap[0][0]:
            heapq.heappushpop(heap, (-dist, kd_node[2]))
        i = (i + 1) % dimensions
        # Goes into the left branch, and then the right branch if needed
        for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
            get_knn(kd_node[b], point, k, dimensions, dist_func, return_distances, i, heap)
    if is_root:
        neighbors = sorted((-h[0], h[1]) for h in heap)
        return neighbors if return_distances else [n[1] for n in neighbors]


"""
Testing Code
"""


def puts(ll):
    for x in ll:
        print(x)


def dist_sq(a, b, dimension):
    return sum((a[i] - b[i]) ** 2 for i in range(dimension))


def dist_sq_dim(a, b):
    return dist_sq(a, b, dim)


df = pd.read_csv("../Data/train_x_y_10K.csv")
points = df.values.tolist()

print(points[:10])

result = []

print("Type points:", type(points))
dim = 2
K = 10
# point which need to find the K nearest neighbours of this point
point_k = [5.1, 5.1]


def bench():
    kd_tree = make_kd_tree(points, dim)
    result.append(tuple(get_knn(kd_tree, point_k, K, dim, dist_sq_dim)))


cProfile.run("bench()")

puts(result[0])
