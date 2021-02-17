from collections import deque

from range_tree.RangeTree import *


class TwoDRangeTree:

    def __init__(self):
        self.root = RangeNode()
        # we choose 5 because our data's x ranges from 0 to 10
        self.root.w = 5

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
                    current_node.addChild(old_point, 'x')
                    current_node.addChild(point, 'x')
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
                    current_node.addChild(old_point, 'x')
                    current_node.addChild(point, 'x')
                    current_node.tree = RangeTree()
                    current_node.tree.insert(point)
                    current_node.tree.insert(old_point)

    def query(self, x1, x2, y1, y2):
        split_node, visited_nodes = self.get_split_node(x1, x2)
        # print(split_node.isLeaf())
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
