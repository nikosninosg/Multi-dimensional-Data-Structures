from range_tree.RangePoint import RangePoint


class RangeTree:

    def __init__(self):
        self.root = RangeNode()
        # we choose 5 cause our data's y ranges from 0 to 10
        self.root.w = 5

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
                    current_node.addChild(old_point, 'y')
                    current_node.addChild(point, 'y')
            else:
                if current_node.r_child is None:
                    current_node.r_child = RangeLeaf(point)
                elif current_node.r_child.isLeaf():
                    old_point = current_node.r_child.range_point
                    current_node.r_child = RangeNode()
                    current_node = current_node.r_child
                    current_node.w = (point.y + old_point.y) / 2
                    current_node.addChild(old_point, 'y')
                    current_node.addChild(point, 'y')


class RangeNode:

    def __init__(self):
        self.l_child: [RangeNode, None] = None
        self.r_child: [RangeNode, None] = None
        self.tree: [RangeTree, None] = None
        self.w: [float, None] = None

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

    def printNode(self):
        for child in [self.l_child, self.r_child]:
            if child is not None and child.isLeaf():
                print("(" + str(child.range_point.x)
                      + ", " + str(child.range_point.y)
                      + ") data: " + str(child.range_point.data))
            elif child is not None and not child.isLeaf():
                child.printNode()


class RangeLeaf(RangeNode):

    def __init__(self, range_point: RangePoint):
        super(RangeLeaf, self).__init__()
        self.range_point: RangePoint = range_point

    def isLeaf(self):
        return True
