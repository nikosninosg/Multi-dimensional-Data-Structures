from range_tree.RangeTree import *


class TwoDRangeTree:
    """
    An implementation of a 2-dimensional range tree which is using the first coordinate (x) of the contained points to
    arrange them and access them.
    All the data of the tree are stored on the leaves.
    """

    def __init__(self, df=None):
        """
        The constructor creates either an empty tree or a tree containing a set of data from dataframe.
        (The tree currently does not support rotations so it is suggested to pass the dataset in the constructor
        instead of adding each point individually on an empty tree, since this is the only way for the Range Tree to be
        balanced.)

        :param df: A dataframe containing the dataset that we want to pass inside the tree
        """
        self.root = RangeNode()
        if df is None:
            self.root.w = 5     # we choose 5 because our data's x ranges from 0 to 10
        else:
            self.root = TwoDRangeTree.create_tree(df)

    @staticmethod
    def create_tree(df) -> [RangeNode, None]:
        """
        This method is creating a list containing RangePoints generated from the dataframe passed in as an argument.
        After that it creates a tree from these points and returns its root.

        :param df: A dataframe containing the dataset to add in the tree.
        :return: The root of the created tree.
        """
        points = []
        for index, row in df.iterrows():
            points.append(RangePoint(row['x'], row['y'], data=row['row_id']))
        return TwoDRangeTree.create_tree_with_points(points)

    @staticmethod
    def create_tree_with_points(points: [RangePoint]) -> [RangeNode, None]:
        """
        This method takes a list of points as an argument and returns the root of a Range Tree containing them.
        The method uses a bottom-up algorithm to create a balanced Range Tree without needing rotations.

        The algorithm works in the same way with the 1-dimensional tree.
        The only difference is that every time a new node is created by merging 2 trees, the tree for the 2nd dimension
        on that node is also created.

        :param points: The points to be added in the tree.
        :return: The root of the newly created tree.
        """
        sorted_points = sorted(points, key=lambda p: p.x)
        if len(sorted_points) == 2:
            points = sorted_points
            node = RangeNode()
            node.w = (points[0].x + points[1].x) / 2
            if points[0].x != points[1].x:
                node.add_child(points[0], 'x')
                node.add_child(points[1], 'x')
            else:
                node.l_child = RangeLeaf(points[0])
                node.r_child = RangeLeaf(points[1])
            node.add_all_points(points)
            node.tree = RangeTree()
            node.tree.root = RangeTree.create_tree_with_points(node.get_all_points())
            return node
        elif len(sorted_points) == 1:
            point = RangePoint(sorted_points[0].x, sorted_points[0].y, sorted_points[0].data)
            leaf = RangeLeaf(point)
            leaf.add_point(point)
            return leaf
        elif len(sorted_points) == 0:
            return None
        else:
            node = RangeNode()
            df_half = int(len(sorted_points) / 2)
            node.l_child = TwoDRangeTree.create_tree_with_points(sorted_points[0:df_half])
            node.r_child = TwoDRangeTree.create_tree_with_points(sorted_points[df_half:len(sorted_points)])
            if node.l_child.is_leaf():
                lw = node.l_child.range_point.x
            else:
                lw = node.l_child.w
            if node.r_child.is_leaf():
                rw = node.r_child.range_point.x
            else:
                rw = node.r_child.w
            node.w = (lw + rw) / 2
            node.add_all_points(node.l_child.points)
            node.add_all_points(node.r_child.points)
            node.tree = RangeTree()
            node.tree.root = RangeTree.create_tree_with_points(node.get_all_points())
            return node

    def query(self, x1, x2, y1, y2):
        """
        This method queries the tree for two given ranges [x1, x2] and [y1, y2], one on each dimension.
        The algorithm works in the following way:

        First it finds the split node on the first dimension, which is the first node with a value inside the given
        range for the first dimension (this means that some of the points contained on the range will be on its left and
        some on its right).

        After that it queries the 2nd dimension tree of the split node using the range for the second dimension.

        Finally it checks the points returned from the 2nd query to see if their coordinates are inside the given ranges
        and it returns all the points for which this is true.

        :param x1: The first value of the first dimension range (inclusive).
        :param x2: The last value of the first dimension range (inclusive).
        :param y1: The first value of the second dimension range (inclusive).
        :param y2: The last value of the second dimension range (inclusive).
        :return:
        """
        split_node, visited_nodes = self.get_split_node(x1, x2)
        if split_node is None:
            return []
        if split_node.is_leaf():
            return [[split_node.range_point], visited_nodes]
        points = split_node.tree.query(y1, y2)
        return [[point for point in points if x1 <= point.x <= x2 and y1 <= point.y <= y2], visited_nodes]

    def get_split_node(self, x1, x2):
        """
        This method finds the split node for a given range. The split node is the first node with a value inside the
        given range (this means that some of the points contained on the range will be on each left and some on its
        right).

        In order to do that the method iterates "walks" down the tree going left if the current node's value is less
        than x1 and right if its great than x2. If the current node's value is between x1 and x2 then the current node
        is the split node.

        This method also returns a stack containing all the points that it visited.

        :param x1: The first value of the range (inclusive).
        :param x2: The last value of the range (inclusive).
        :return: A list containing in the 1st position the split node and in the 2nd one a stack of the points visited.
        """
        visited_nodes = deque()
        if x1 > x2:
            return [None, visited_nodes]
        current_node = self.root
        visited_nodes.append(current_node)
        while current_node is not None and not current_node.is_leaf():
            if x1 <= current_node.w <= x2:
                return [current_node, visited_nodes]
            else:
                if x1 > current_node.w:
                    current_node = current_node.r_child
                    visited_nodes.append(current_node)
                elif x2 < current_node.w:
                    current_node = current_node.l_child
                    visited_nodes.append(current_node)
        return [current_node, visited_nodes]

    def get_knn(self, point: RangePoint, k: int):
        """
        This is a method to calculate the k nearest neighbors of a given point.
        The algorithm works in the following way:

        First it queries the tree for a short range around the given point.
        As it does travels the tree to find the points it stores all of the nodes visited in a stack.

        After that it pops each node from the stack and adds its points to a list of points, until this list has k
        points or until the stack is empty.

        Using the newly created list the algorithm calculates a radius which is the distance from the given point to the
        furthest point in the list. We know now that the k nearest neighbors must be inside a circle with that radius
        and with the given point as a center (since the list contains k points).
            * if the list contains less than k points because the algorithm emptied the stack before it fills the list
            then the whole tree has less than k points

        Instead of using the circle directly, we are creating a square (2 ranges) that contains this circle in order
        to re-use the query function that we created before.

        We query the tree in order to find all the points inside the 2 given ranges.

        We sort the returned points using their distance to the given point and we return the first k points in that
        list. Those points are the k nearest neighbors.

        :param point: The point whose neighbors we are looking for.
        :param k: The number of neighbors.
        :return: A list containing the k nearest neighbors of the point.
        """
        points, visited_nodes = self.query(point.x - 0.5, point.x + 0.5, point.y - 0.5, point.y + 0.5)
        while len(visited_nodes) != 0 and len(points) < k:
            node = visited_nodes.pop()
            contained_points = node.get_all_points()
            for current_point in contained_points:
                if current_point not in points:
                    points.append(current_point)

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))
        points = points[0:k]

        radius = point.euclidean_distance(points[k - 1])
        x_range = [point.x - radius, point.x + radius]
        y_range = [point.y - radius, point.y + radius]

        points = self.query(x_range[0], x_range[1], y_range[0], y_range[1])[0]

        points.sort(key=lambda point_in_list: point.euclidean_compare(point_in_list))
        return points[0:k]
