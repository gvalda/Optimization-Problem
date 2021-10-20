from random import random
from models.point import Point


def randfloat(start, stop):
    return random() * abs(stop-start) + start


def generate_point(start, stop):
    x = randfloat(start, stop)
    y = randfloat(start, stop)
    p = Point(x, y)
    return p


def generate_n_points(n, start, stop):
    points = []
    for _ in range(n):
        p = generate_point(start, stop)
        points.append(p)
    return points
