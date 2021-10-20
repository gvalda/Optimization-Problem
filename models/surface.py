class Surface:
    def __init__(self, points=None):
        if points:
            self._points = points
        else:
            self._points = []

    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Surface(self._points[key])
        return self._points[key]

    def __len__(self):
        return len(self._points)

    def __str__(self):
        points_str = ' ,\n'.join(str(point) for point in self._points)
        return f'<{self.__class__.__name__} object: \n{points_str}>'

    def set_points(self, points):
        self._points = points

    def add_point(self, point):
        self._points.append(point)

    def get_points(self):
        return self._points

    def replace(self, cur_point, new_point):
        for idx, point in enumerate(self._points):
            if point == cur_point:
                self._points[idx] = new_point
