from collections import deque

from range_tree.RangeTree import *


class TwoDRangeTree:

    def __init__(self):
        self.root = RangeNode()
        # we choose 5 because our data's x ranges from 0 to 10
        self.root.w = 5

    @staticmethod
    def create_tree(df) -> [RangeNode, None]:
        points = []
        for index, row in df.iterrows():
            points.append(RangePoint(row['x'], row['y'], data=row['row_id']))
        return TwoDRangeTree.create_tree_with_points(points)

    @staticmethod
    def create_tree_with_points(points: [RangePoint]) -> [RangeNode, None]:
        sorted_points = sorted(points, key=lambda p: p.x)
        if len(sorted_points) == 2:
            points = sorted_points
            node = RangeNode()
            node.w = (points[0].x + points[1].x) / 2
            if points[0].x != points[1].x:
                node.addChild(points[0], 'x')
                node.addChild(points[1], 'x')
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
            if node.l_child.isLeaf():
                lw = node.l_child.range_point.x
            else:
                lw = node.l_child.w
            if node.r_child.isLeaf():
                rw = node.r_child.range_point.x
            else:
                rw = node.r_child.w
            node.w = (lw + rw) / 2
            node.add_all_points(node.l_child.points)
            node.add_all_points(node.r_child.points)
            node.tree = RangeTree()
            node.tree.root = RangeTree.create_tree_with_points(node.get_all_points())
            return node

    def insert(self, point: RangePoint):
        if self.root.w is None:
            # self.root.w = point.x + point.x / 2
            self.root.l_child = RangeLeaf(point)
            self.root.tree = RangeTree()
            self.root.tree.insert(point)
        else:
            current_node = self.root
            while current_node is not None and not current_node.isLeaf():
                if point.x <= current_node.w:
                    if not current_node.childIsLeafOrNone('left'):
                        current_node.tree.insert(point)
                        current_node = current_node.l_child
                    else:
                        break
                else:
                    if not current_node.childIsLeafOrNone('right'):
                        current_node.tree.insert(point)
                        current_node = current_node.r_child
                    else:
                        break
            if point.x <= current_node.w:
                if current_node.tree is None:
                    current_node.tree = RangeTree()
                current_node.tree.insert(point)
                if current_node.l_child is None:
                    current_node.l_child = RangeLeaf(point)
                elif current_node.l_child.isLeaf():
                    old_point = current_node.l_child.range_point
                    current_node.l_child = RangeNode()
                    current_node = current_node.l_child
                    current_node.w = (point.x + old_point.x) / 2
                    if old_point.x != point.x:
                        current_node.addChild(old_point, 'x')
                        current_node.addChild(point, 'x')
                    else:
                        current_node.l_child = RangeLeaf(old_point)
                        current_node.r_child = RangeLeaf(point)
                    current_node.tree = RangeTree()
                    current_node.tree.insert(point)
                    current_node.tree.insert(old_point)
            else:
                if current_node.tree is None:
                    current_node.tree = RangeTree()
                current_node.tree.insert(point)
                if current_node.r_child is None:
                    current_node.r_child = RangeLeaf(point)
                elif current_node.r_child.isLeaf():
                    old_point = current_node.r_child.range_point
                    current_node.r_child = RangeNode()
                    current_node = current_node.r_child
                    current_node.w = (point.x + old_point.x) / 2
                    if old_point.x != point.x:
                        current_node.addChild(old_point, 'x')
                        current_node.addChild(point, 'x')
                    else:
                        current_node.l_child = RangeLeaf(old_point)
                        current_node.r_child = RangeLeaf(point)
                    current_node.tree = RangeTree()
                    current_node.tree.insert(point)
                    current_node.tree.insert(old_point)

    def query(self, x1, x2, y1, y2):
        split_node, visited_nodes = self.get_split_node(x1, x2)
        if split_node is None:
            return []
        if split_node.isLeaf():
            return [[split_node.range_point], visited_nodes]
        points = split_node.tree.query(y1, y2)
        return [[point for point in points if x1 <= point.x <= x2 and y1 <= point.y <= y2], visited_nodes]

    def get_split_node(self, r1, r2):
        visited_nodes = deque()
        if r1 > r2:
            return [None, visited_nodes]
        current_node = self.root
        visited_nodes.append(current_node)
        while current_node is not None and not current_node.isLeaf():
            if r1 <= current_node.w <= r2:
                return [current_node, visited_nodes]
            else:
                if r1 > current_node.w:
                    current_node = current_node.r_child
                    visited_nodes.append(current_node)
                elif r2 < current_node.w:
                    current_node = current_node.l_child
                    visited_nodes.append(current_node)
        return [current_node, visited_nodes]
