import sys
from time import time
from models.surface import Surface
from models.point import Point
from utils.random import generate_n_points
from utils.algorithms import *

POINTS_MAX_POSITION = 10
POINTS_MIN_POSITION = -10

N_POINTS = 100
M_POINTS = 100

THREADS_NUMBER = 16


def main():
    if len(sys.argv) > 2:
        n_points, m_points, n_threads = (int(p) for p in sys.argv[1:4])
    else:
        n_points, m_points, n_threads = N_POINTS, M_POINTS, THREADS_NUMBER

    immutable_surface = get_points_surface(
        n_points, POINTS_MIN_POSITION, POINTS_MAX_POSITION)

    mutable_surface = get_points_surface(
        m_points, POINTS_MIN_POSITION, POINTS_MAX_POSITION)
    gdo = GradientDescentOptimization(immutable_surface, threads_num=n_threads)

    start = time()
    prev_step = start
    for surface, psi in gdo.get_new_mutable_surfaces(mutable_surface):
        step = time()
        print(f'Elapsed since start { step-start:.3f}s')
        print(f'Elapsed since previous iteration {step-prev_step:.3f}s')
        prev_step = step


def get_points_surface(points_num, start, stop):
    points = generate_n_points(points_num, start, stop)
    surface = Surface(points)
    return surface


if __name__ == '__main__':
    main()
