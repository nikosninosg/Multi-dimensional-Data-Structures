from collections import deque

import quads


class LocalQuadTree(quads.QuadTree):
    """
    This is a local implementation of a Quad Tree.
    It extends the QuadTree class provided by the quads method and implements a "local" algorithm to find the k nearest
    neighbors.
    """

    def query(self, point: quads.Point):
        """
        This is a method to query the Quad Tree for a specific given point and return back all the points contained in
        the square (node) of the tree that would contain it and a stack containing all the points visited.
        (The point passed as an argument might be or might not be a point of the tree.)

        In order to do that the algorithm starts from the root of the tree, sets it as the current node and then
        chooses one of its 4 children as the next current node, based on which one will lead us to the given point.
        It continues like that until it reaches the given point and every time that the current_node is update it adds
        it to the stack of the visited nodes.

        :param point: The point we are looking for
        :return: A list containing in the 1st position the points in the node that can contain the selected point and
        in the 2nd position a stack of the nodes visited while traveling towards the given point.
        """
        nodes_visited = deque()
        current_node = self._root
        nodes_visited.append(current_node)
        while current_node is not None and not LocalQuadTree.nodeIsLeaf(current_node):
            if current_node.ll.contains_point(point):
                current_node = current_node.ll
                nodes_visited.append(current_node)
            elif current_node.lr.contains_point(point):
                current_node = current_node.lr
                nodes_visited.append(current_node)
            elif current_node.ul.contains_point(point):
                current_node = current_node.ul
                nodes_visited.append(current_node)
            elif current_node.ur.contains_point(point):
                current_node = current_node.ur
                nodes_visited.append(current_node)
            else:
                current_node = None
        if LocalQuadTree.nodeIsLeaf(current_node):
            points = current_node.all_points()
        else:
            points = []
        return points, nodes_visited

    def get_knn(self, point: quads.Point, k: int):
        """
        This is a method to calculate the k nearest neighbors of a given point.
        The algorithm works in the following way:

        First it queries the tree for the given point. As it does travels the tree to find the points it stores all of
        the nodes visited in a stack.

        After that it pops each node from the stack and adds its points to a list of points, until this list has k
        points or until the stack is empty.

        Using the newly created list the algorithm calculates a radius which is the distance from the given point to the
        furthest point in the list. We know now that the k nearest neighbors must be inside a circle with that radius
        and with the given point as a center (since the list contains k points)
            * if the list contains less than k points because the algorithm emptied the stack before it fills the list
            then the whole tree has less than k points

        Instead of using the circle directly, we are creating a square (bounding box) that contains this circle in order
        to take advantage of the library's functions for bounding boxes.

        We query the tree in order to find all the points inside the bounding box.

        We sort the returned points using their distance to the given point and we return the first k points in that
        list. Those points are the k nearest neighbors.

        :param point: The point whose neighbors we are looking for.
        :param k: The number of neighbors.
        :return: A list containing the k nearest neighbors of the point.
        """
        points, nodes_visited = self.query(point)
        while len(nodes_visited) != 0 and len(points) < k:
            node = nodes_visited.pop()
            contained_points = node.all_points()
            for current_point in contained_points:
                if current_point not in points:
                    points.append(current_point)

        points.sort(key=lambda point_in_list: quads.euclidean_compare(point, point_in_list))
        points = points[0:k]

        radius = quads.euclidean_distance(point, points[k - 1])
        bb = quads.BoundingBox(point.x - radius, point.y - radius, point.x + radius, point.y + radius)

        points = self._root.within_bb(bb)
        points.sort(key=lambda point_in_list: quads.euclidean_compare(point, point_in_list))
        return points[0:k]

    @staticmethod
    def nodeIsLeaf(node: quads.QuadNode):
        """
        This method returns if a given node is a leaf or not.

        :param node: The node to check.
        :return: True if it is a leaf, false otherwise.
        """
        return node.ll is None and node.ul is None and node.lr is None and node.ur is None
