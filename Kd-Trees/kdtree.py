import cProfile
import random
import pandas as pd


# Makes the KD-Tree
def make_kd_tree(df_points, dimensions, i=0):
    if len(df_points) > 1:
        points.sort(key=lambda x: x[i])
        sorted(df_points, key=lambda x: x[i])
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


# For the closest neighbor
def get_nearest(kd_node, point, dimensions, dist_func, return_distances=True, i=0, best=None):
    if kd_node is not None:
        dist = dist_func(point, kd_node[2])
        dx = kd_node[2][i] - point[i]
        if not best:
            best = [dist, kd_node[2]]
        elif dist < best[0]:
            best[0], best[1] = dist, kd_node[2]
        i = (i + 1) % dimensions
        # Goes into the left branch, and then the right branch if needed
        for b in [dx < 0] + [dx >= 0] * (dx * dx < best[0]):
            get_nearest(kd_node[b], point, dimensions, dist_func, return_distances, i, best)
    return best if return_distances else best[1]


"""
Testing Code
"""


def puts(ll):
    for x in ll:
        print(x)


def rand_point(dimension):
    return [random.uniform(-1, 1) for y in range(dimension)]


def dist_sq(a, b, dimension):
    return sum((a[i] - b[i]) ** 2 for i in range(dimension))


def dist_sq_dim(a, b):
    return dist_sq(a, b, dim)


dim = 2

df = pd.read_csv("../Data/train_x_y_10K.csv")
points = df.values.tolist()

print(points[:10])

test = [rand_point(dim) for x in range(len(df))]
result = []

print("Type points:", type(points))


def bench():
    KdTree = make_kd_tree(points, dim)
    result.append(tuple(get_knn(KdTree, [0] * dim, 8, dim, dist_sq_dim)))
    for t in test:
        result.append(tuple(get_knn(KdTree, t, 8, dim, dist_sq_dim)))


cProfile.run("bench()")

puts(result[0])
print("")

print("")
kd_tree = make_kd_tree(points, dim)

print(get_nearest(kd_tree, [0] * dim, dim, dist_sq_dim))

# Define the distance function inline, like:
print(get_nearest(kd_tree, [0] * dim, dim, lambda a, b: dist_sq(a, b, dim)))
# print(get_nearest(kd_tree, [0] * dim, dim, lambda a, b: sum((a[i] - b[i]) ** 2 for i in range(dim))))
