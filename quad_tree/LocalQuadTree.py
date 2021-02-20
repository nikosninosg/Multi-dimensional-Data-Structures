from collections import deque

import quads


class LocalQuadTree(quads.QuadTree):
    def get_root(self):
        return self._root

    def get_nn(self, point: quads.Point, k: int):
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

    def query(self, point: quads.Point):
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

    @staticmethod
    def nodeIsLeaf(node: quads.QuadNode):
        return node.ll is None and node.ul is None and node.lr is None and node.ur is None
