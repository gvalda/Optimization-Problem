from matplotlib import pyplot as plt
from celluloid import Camera


class Plotter:
    def __init__(self, figure_x_size=(-15, 15), figure_y_size=(-15, 15)):
        self._fig, self._ax = plt.subplots()
        self._ax.set_xlim(*figure_x_size)
        self._ax.set_ylim(*figure_y_size)
        self._camera = Camera(self._fig)

    def set_immutable_surface(self, surface):
        self._immutable_surface = surface

    def snap_mutable_surface(self, surface):
        self._set_mutable_surface(surface)
        self._scatter_immutable_surface()
        self._scatter_mutable_surface()
        self._build_lines_between()
        self._snap_with_camera()

    def _set_mutable_surface(self, surface):
        self._mutable_surface = surface

    def _scatter_immutable_surface(self):
        self._scatter_surface(self._immutable_surface, 'orangered')

    def _scatter_mutable_surface(self):
        self._scatter_surface(self._mutable_surface, 'royalblue')

    def _scatter_surface(self, surface, color):
        x = []
        y = []
        for point in surface:
            x.append(point.x)
            y.append(point.y)

        # x, y = surface.get_x_and_y_lists()
        self._ax.scatter(x, y, c=color)

    def _build_lines_between(self):
        self._build_lines_between_immutable_and_mutable()
        self._build_lines_between_mutable()
        self._build_lines_between_immutable()

    def _build_lines_between_immutable_and_mutable(self):
        for immut_point in self._immutable_surface:
            for mut_point in self._mutable_surface:
                self._build_line(immut_point, mut_point, 'silver')

    def _build_lines_between_mutable(self):
        for index, mut_point1 in enumerate(self._mutable_surface):
            for mut_point2 in self._mutable_surface[index:]:
                if mut_point1 is not mut_point2:
                    self._build_line(mut_point1, mut_point2, 'silver')

    def _build_lines_between_immutable(self):
        for index, immut_point1 in enumerate(self._immutable_surface):
            for immut_point2 in self._immutable_surface[index:]:
                if immut_point1 is not immut_point2:
                    self._build_line(immut_point1, immut_point2, 'silver')

    def _build_line(self, point1, point2, color):
        self._ax.plot([point1.x, point2.x], [
                      point1.y, point2.y], c=color, zorder=-1, alpha=0.5)

    def _snap_with_camera(self):
        self._camera.snap()

    def save(self, destination):
        animation = self._camera.animate()
        animation.save(destination, writer='imagemagick')
