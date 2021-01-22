import quads


class LocalQuadTree(quads.QuadTree):
    def getRoot(self):
        return self._root
