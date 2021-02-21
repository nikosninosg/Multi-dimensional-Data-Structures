from collections import deque

from range_tree.RangePoint import RangePoint


class RangeNode:
    """
    A class that represents a node of the range tree. This class is used both for the 1D and the 2D Range Tree.
    It contains the following attributes.
    - l_child: The left child of the node.
    - r_child: The right child of the node.
    - tree: The tree of the node containing the points arranged using the secondary dimension (only used in the nodes
    of the TwoDRangeTree).
    - w: A value that shows us if we should go left or right when we are "walking" down the tree.
    - points: A list of points containing all the points below this node.
    """

    def __init__(self):
        """
        The constructor initializes an empty node.
        """
        self.l_child: [RangeNode, None] = None
        self.r_child: [RangeNode, None] = None
        self.tree: [RangeTree, None] = None
        self.w: [float, None] = None
        self.points = []

    def is_leaf(self):
        """
        This method returns if this node is a leaf. This method always returns false and it is overwritten by the leaf
        nodes.

        :return: False.
        """
        return False

    def child_is_leaf_or_none(self, child: str):
        """
        This method returns if the left child of the node is leaf or None (which means that it is not a non-leaf node).
        The method takes a parameter to determine whether it should check the left or the right child.

        :param child: 'left' to check the left child and 'right' to check the right one.
        :return: True if the selected child is leaf or None, false otherwise.
        """
        if child == 'left':
            return self.l_child is None or self.l_child.is_leaf()
        elif child == 'right':
            return self.r_child is None or self.r_child.is_leaf()
        return False

    def add_child(self, point: RangePoint, axis: str):
        """
        This method adds a point as a child to this node. The method will assume that the child of the node in which the
        point should be added (left or right) is None and it will override it with a new leaf.
        The method can work both for trees that use the x-dimension to arrange their nodes and for trees that use the
        y-dimension.

        :param point: The point to add as a child of this node.
        :param axis: 'x' or 'y' depending on which dimension is used to arrange the nodes of the tree.
        :return: -
        """
        if axis == 'y':
            if point.y <= self.w:
                self.l_child = RangeLeaf(point)
            else:
                self.r_child = RangeLeaf(point)
        elif axis == 'x':
            if point.x <= self.w:
                self.l_child = RangeLeaf(point)
            else:
                self.r_child = RangeLeaf(point)

    def get_all_points(self):
        """
        This method returns the points below this node. The points are already stored in a list so this method simply
        returns this list.

        :return: A list containing the points below this node.
        """
        return self.points

    def print_node(self):
        """
        This method prints all the nodes of the tree.
        """
        for child in [self.l_child, self.r_child]:
            if child is not None and child.is_leaf():
                print("(" + str(child.range_point.x)
                      + ", " + str(child.range_point.y)
                      + ") data: " + str(child.range_point.data))
            elif child is not None and not child.is_leaf():
                child.print_node()

    def add_point(self, point: RangePoint):
        """
        This method adds a point to the list of points of the this node.

        :param point: The point to add to the list of points.
        """
        self.points.append(point)

    def add_all_points(self, points: [RangePoint]):
        """
        This method adds a list of points to the current list of points of this node.
        The method adds each point to the list individually.

        :param points: The list of points to add.
        """
        for point in points:
            self.points.append(point)


class RangeLeaf(RangeNode):
    """
    A class that represents a leaf of the range tree. This class extends the RangeNode class since Leaves are a specific
    type of nodes.
    It has all the attributes of the RangeNode class and it adds to them the following.
    - point: A point that is stored to the tree.
    """

    def __init__(self, range_point: RangePoint):
        """
        The constructor creates a new leaf containing a given point.

        :param range_point: The point to be contained in the leaf.
        """
        super(RangeLeaf, self).__init__()
        self.range_point: RangePoint = range_point

    def is_leaf(self):
        """
        This method returns if this node is a leaf. Naturally this method always returns True and it can be used to
        distinguish between a RangeNode and a RangeLeaf.
        This method overrides RangeNode's isLeaf method.

        :return: True.
        """
        return True

    def get_all_points(self):
        """
        This method returns the points below this node. Since this node is a leaf, it only returns the point of this
        leaf inside a list.
        This method overrides RangeNode's get_all_points method.

        :return: A list containing the point of this leaf.
        """
        return [self.range_point]


class RangeTree:
    """
    An implementation of a 1-dimensional range tree which is using the second coordinate (y) of the contained points to
    arrange them and access them.
    All the data of the tree are stored on the leaves.
    """

    def __init__(self, df=None):
        """
        The constructor creates either an empty tree or a tree containing a set of data from dataframe.
        (The tree currently does not support rotations so it is suggested to pass the dataset in the constructor
        instead of adding each point individually, since this is the only way for the Range Tree to be balanced.)

        :param df: A dataframe containing the dataset that we want to pass inside the tree
        """
        self.root = RangeNode()
        if df is None:
            self.root.w = 5     # we choose 5 cause our data's y ranges from 0 to 10
        else:
            self.root = RangeTree.create_tree(df)

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
        return RangeTree.create_tree_with_points(points)

    @staticmethod
    def create_tree_with_points(points: [RangePoint]) -> [RangeNode, None]:
        """
        This method takes a list of points as an argument and returns the root of a Range Tree containing them.
        The method uses a bottom-up algorithm to create a balanced Range Tree without needing rotations.
        The algorithm works in the following way:

        First it sorts all the points of the list using their y value.

        Then it splits the points in 2 and recursively calls itself in each of the 2 parts. This way it will create 2
        trees (one from each part) and it will set as the children of the current node the roots of the 2 trees.

        The recursion will end when:
        - there are only 2 points left, in which case the method returns a node which has these 2 as children.
        - there is only 1 point left, in which case the method returns a leaf that contains these points.

        Once all the recursions end the node returned will be the root of a tree containing all the points.

        In addition the algorithm does one more job.
        Since each node of the tree contain a list with all the points that are below it, the algorithm will create
        these lists by merging the lists of the two children which are returned from the previous recursive call.

        :param points: The points to be added in the tree.
        :return: The root of the newly created tree.
        """
        sorted_points = sorted(points, key=lambda p: p.y)
        if len(sorted_points) == 2:
            points = sorted_points
            node = RangeNode()
            node.w = (points[0].x + points[1].x) / 2
            if points[0].x != points[1].x:
                node.add_child(points[0], 'y')
                node.add_child(points[1], 'y')
            else:
                node.l_child = RangeLeaf(points[0])
                node.r_child = RangeLeaf(points[1])
            node.add_all_points(points)
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
            node.l_child = RangeTree.create_tree_with_points(sorted_points[0:df_half])
            node.r_child = RangeTree.create_tree_with_points(sorted_points[df_half:len(sorted_points)])
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
            return node

    def query(self, y1, y2):
        """
        This method queries the tree for a given range [y1, y2].
        The algorithm works in the following way:

        First it finds the split node, which is the first node with a value inside the given range (this means that
        some of the points contained on the range will be on its left and some on its right).

        After that it gets all the points of the given node.

        Finally from these points it returns only those, whose y value is in the given range.

        :param y1: The first value of the range (inclusive).
        :param y2: The last value of the range (inclusive).
        :return: The points in the given range.
        """
        split_node, visited_nodes = self.get_split_node(y1, y2)
        if split_node is None:
            return []
        points = split_node.get_all_points()
        return [point for point in points if y1 <= point.y <= y2]

    def get_split_node(self, y1, y2):
        """
        This method finds the split node for a given range. The split node is the first node with a value inside the
        given range (this means that some of the points contained on the range will be on each left and some on its
        right).

        In order to do that the method iterates "walks" down the tree going left if the current node's value is less
        than y1 and right if its great than y2. If the current node's value is between y1 and y2 then the current node
        is the split node.

        This method also returns a stack containing all the points that it visited.

        :param y1: The first value of the range (inclusive).
        :param y2: The last value of the range (inclusive).
        :return: A list containing in the 1st position the split node and in the 2nd one a stack of the points visited.
        """
        visited_nodes = deque()
        if y1 > y2:
            return [None, visited_nodes]
        current_node = self.root
        visited_nodes.append(current_node)
        while current_node is not None and not current_node.is_leaf():
            if y1 <= current_node.w <= y2:
                return [current_node, visited_nodes]
            else:
                if y1 > current_node.w:
                    current_node = current_node.r_child
                    visited_nodes.append(current_node)
                elif y2 < current_node.w:
                    current_node = current_node.l_child
                    visited_nodes.append(current_node)
        return [current_node, visited_nodes]
