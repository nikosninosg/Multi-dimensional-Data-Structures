import quads


class Circle:
    center: quads.Point
    radius: float

    def __init__(self, center: quads.Point, radius: float):
        self.center = center
        self.radius = radius


