from math import sqrt
import quads
from LocalQuadTree import LocalQuadTree
from Circle import Circle


class QuadKnnAlgorithm:

    tree: LocalQuadTree
    x: quads.Point
    k: int
    c: Circle
    stack: []
    nn_list: []
    i: int

    def __init__(self, tree: LocalQuadTree, x: quads.Point, k: int = 1):
        self.tree = tree
        self.x = x
        self.k = k
        self.c = Circle(x, sqrt(tree.width ** 2 + tree.height ** 2))
        self.stack = []
        self.nn_list = []
        self.i = 0

    def nn_query(self):
        current_node = self.tree.getRoot()
        self.stack = [current_node]
        self.nn_list = []

        while len(self.stack) > 0:
            self.process(current_node.ll)
            self.process(current_node.ul)
            self.process(current_node.lr)
            self.process(current_node.ur)

            current_node = self.stack.pop()
            self.i = self.i + 1

        return self.nn_list

    def process(self, node: quads.QuadNode):
        if node is None or len(node.all_points()) == 0:
            return
        if self.nodeIsLeaf(node):
            points = self.getAllPoints(node)
            for point in points:
                dist = quads.euclidean_distance(self.x, point)
                if dist < self.c.radius:
                    self.addPoint(point)
        else:
            if self.nodeInCircle(node):
                self.stack.append(node)

    def addPoint(self, point: quads.Point):
        if len(self.nn_list) < self.k:
            self.nn_list.append(point)
            if len(self.nn_list) == self.k:
                self.c.radius = self.getMaxDistance()
        else:
            self.nn_list.remove(max(self.nn_list, key=self.getPointDistance))
            self.nn_list.append(point)
            self.c.radius = self.getMaxDistance()

    def getPointDistance(self, point: quads.Point):
        if point is None:
            return None
        return quads.euclidean_distance(self.x, point)

    def getMaxDistance(self):
        max_dist = 0
        for point in self.nn_list:
            if self.getPointDistance(point) > max_dist:
                max_dist = self.getPointDistance(point)
        return max_dist

    def nodeInCircle(self, node):
        half_height = node.height / 2
        half_width = node.width / 2
        half_diagonal = sqrt(half_height**2 + half_width**2)
        approximate_dist = half_diagonal + self.c.radius
        return quads.euclidean_distance(self.c.center, node.center) <= approximate_dist

    @staticmethod
    def getAllPoints(arg: [quads.QuadNode, quads.Point]):
        if type(arg) is quads.Point:
            return [arg]
        if arg is None or len(arg.all_points()) == 0:
            return []
        else:
            return arg.all_points()

    @staticmethod
    def nodeIsLeaf(node: quads.QuadNode):
        return node.ll is None and node.ul is None and node.lr is None and node.ur is None
