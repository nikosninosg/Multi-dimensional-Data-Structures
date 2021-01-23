import pandas as pd
from sklearn.neighbors import KDTree
import matplotlib.pyplot as plt

df = pd.read_csv("train_x_y_10K.csv")

# Num of Rows = 29.118.021 points
print("Num of Rows: ", len(df.index))

# print(df.y[0:3])

plt.scatter(df.x[0:99], df.y[0:99])
plt.show()

X = df.to_numpy()
print(X)
print(type(X))
tree = KDTree(X)
print(tree)

nearest_dist, nearest_ind = tree.query(X, k=2)  # k=2 nearest neighbors

# Each entry gives the list of distances to the neighbors of the corresponding point.
print(nearest_dist[:, 1])
# Each entry gives the list of indices of neighbors of the corresponding point.
print(nearest_ind[:, 1])  # drop id
