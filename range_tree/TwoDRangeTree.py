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
