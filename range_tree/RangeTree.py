from collections import deque

from range_tree.RangePoint import RangePoint


class RangeNode:

    def __init__(self):
        self.l_child: [RangeNode, None] = None
        self.r_child: [RangeNode, None] = None
        self.tree: [RangeTree, None] = None
        self.w: [float, None] = None
        self.points = []

    def isLeaf(self):
        return False

    def childIsLeafOrNone(self, child: str):
        if child == 'left':
            return self.l_child is None or self.l_child.isLeaf()
        elif child == 'right':
            return self.r_child is None or self.r_child.isLeaf()
        return False

    def addChild(self, point: RangePoint, axis: str):
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
        return self.points
        # points = []
        # for child in [self.l_child, self.r_child]:
        #     if child is not None and child.isLeaf():
        #         points.append(child.range_point)
        #     elif child is not None and not child.isLeaf():
        #         new_points = child.get_all_points()
        #         for point in new_points:
        #             points.append(point)
        # return points

    def printNode(self):
        for child in [self.l_child, self.r_child]:
            if child is not None and child.isLeaf():
                print("(" + str(child.range_point.x)
                      + ", " + str(child.range_point.y)
                      + ") data: " + str(child.range_point.data))
            elif child is not None and not child.isLeaf():
                child.printNode()

    def add_point(self, point: RangePoint):
        self.points.append(point)

    def add_all_points(self, points: [RangePoint]):
        for point in points:
            self.points.append(point)


class RangeLeaf(RangeNode):

    def __init__(self, range_point: RangePoint):
        super(RangeLeaf, self).__init__()
        self.range_point: RangePoint = range_point

    def isLeaf(self):
        return True

    def get_all_points(self):
        return [self.range_point]


class RangeTree:

    def __init__(self):
        self.root = RangeNode()
        # we choose 5 cause our data's y ranges from 0 to 10
        self.root.w = 5

    @staticmethod
    def create_tree(df) -> [RangeNode, None]:
        points = []
        for index, row in df.iterrows():
            points.append(RangePoint(row['x'], row['y'], data=row['row_id']))
        return RangeTree.create_tree_with_points(points)

    @staticmethod
    def create_tree_with_points(points: [RangePoint]) -> [RangeNode, None]:
        sorted_points = sorted(points, key=lambda p: p.y)
        if len(sorted_points) == 2:
            points = sorted_points
            node = RangeNode()
            node.w = (points[0].x + points[1].x) / 2
            if points[0].x != points[1].x:
                node.addChild(points[0], 'y')
                node.addChild(points[1], 'y')
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
            return node

    def insert(self, point: RangePoint):
        if self.root.w is None:
            # self.root.w = point.y + point.y / 2
            self.root.l_child = RangeLeaf(point)
        else:
            current_node = self.root
            while current_node is not None and not current_node.isLeaf():
                if point.y <= current_node.w:
                    if not current_node.childIsLeafOrNone('left'):
                        current_node = current_node.l_child
                    else:
                        break
                else:
                    if not current_node.childIsLeafOrNone('right'):
                        current_node = current_node.r_child
                    else:
                        break
            if point.y <= current_node.w:
                if current_node.l_child is None:
                    current_node.l_child = RangeLeaf(point)
                elif current_node.l_child.isLeaf():
                    old_point = current_node.l_child.range_point
                    current_node.l_child = RangeNode()
                    current_node = current_node.l_child
                    current_node.w = (point.y + old_point.y) / 2
                    if old_point.y != point.y:
                        current_node.addChild(old_point, 'y')
                        current_node.addChild(point, 'y')
                    else:
                        current_node.l_child = RangeLeaf(old_point)
                        current_node.r_child = RangeLeaf(point)
            else:
                if current_node.r_child is None:
                    current_node.r_child = RangeLeaf(point)
                elif current_node.r_child.isLeaf():
                    old_point = current_node.r_child.range_point
                    current_node.r_child = RangeNode()
                    current_node = current_node.r_child
                    current_node.w = (point.y + old_point.y) / 2
                    if old_point.y != point.y:
                        current_node.addChild(old_point, 'y')
                        current_node.addChild(point, 'y')
                    else:
                        current_node.l_child = RangeLeaf(old_point)
                        current_node.r_child = RangeLeaf(point)

    def query(self, r1, r2):
        split_node, visited_nodes = self.get_split_node(r1, r2)
        if split_node is None:
            return []
        points = split_node.get_all_points()
        # print(len(points))
        return [point for point in points if r1 <= point.y <= r2]

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


