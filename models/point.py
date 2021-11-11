from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f'<{self.__class__.__name__} object: x={self.x} y={self.y}>'

    def length_to(self, point):
        return sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

    def get_vector_to(self, point):
        vector_x = point.x - self.x
        vector_y = point.y - self.y
        return vector_x, vector_y

    def get_dict(self):
        return {'x': self.x, 'y': self.y}


class GradientPoint(Point):
    def add_psi(self, value):
        if not hasattr(self, '_psi'):
            setattr(self, '_psi', [])
        self._psi.append(value)

    def get_psi(self, index):
        if not hasattr(self, '_psi') or not self.psi:
            return None
        return self.psi[index]
