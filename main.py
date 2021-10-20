import sys
from models.surface import Surface
from models.point import Point
from utils.random import generate_n_points
from utils.plotter import Plotter
from utils.algorithms import SteepestGradientDescent

FIGURE_X_SIZE = (-12, 12)
FIGURE_Y_SIZE = (-12, 12)

POINTS_MAX_POSITION = 10
POINTS_MIN_POSITION = -10

DESTINATION = 'plot.gif'


def main():
    if len(sys.argv) > 2:
        n_points, m_points = sys.argv[:2]
    else:
        n_points, m_points = 50, 3

    plotter = Plotter(FIGURE_X_SIZE, FIGURE_Y_SIZE)
    immutable_surface = get_points_surface(
        n_points, POINTS_MIN_POSITION, POINTS_MAX_POSITION)

    plotter.set_immutable_surface(immutable_surface)
    mutable_surface = get_points_surface(
        m_points, POINTS_MIN_POSITION, POINTS_MAX_POSITION)
    plotter.snap_mutable_surface(mutable_surface)
    sgd = SteepestGradientDescent(immutable_surface)
    for _ in range(50):
        mutable_surface = sgd.get_new_mutable_surface(mutable_surface)
        plotter.snap_mutable_surface(mutable_surface)

    plotter.save(DESTINATION)


def get_points_surface(points_num, start, stop):
    points = generate_n_points(points_num, start, stop)
    surface = Surface(points)
    return surface


if __name__ == '__main__':
    main()
