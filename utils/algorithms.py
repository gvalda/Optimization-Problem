from multiprocessing import Pool
from itertools import product, combinations, combinations_with_replacement
from functools import partial
from statistics import mean

from models.surface import Surface
from models.point import Point


class GradientDescentOptimization:
    def __init__(self, immutable_surface=None, ds=0.01, h=0.01, accuracy=0.005):
        self._ds = ds
        self._h = h
        self._accuracy = accuracy
        self._immutable_surface = immutable_surface

    def get_new_mutable_surfaces(self, surface):
        while True:
            psi = self._get_psi(surface)
            print(psi)
            get_new_point_m = partial(
                self._get_new_point, psi=psi, surface=surface)
            with Pool() as p:
                new_points = p.map(get_new_point_m, surface)
            new_surface = Surface(new_points)
            # new_surface = Surface()
            # for point in surface:
            #     new_point = get_new_point_m(point)
            #     new_surface.add_point(new_point)
            print(1)
            yield new_surface, psi
            new_psi = self._get_psi(new_surface)
            if abs(psi - new_psi)/new_psi*100 < self._accuracy:
                break
            surface = new_surface

    def _get_new_point(self, point, psi, surface):
        vector_x, vector_y = self._get_gradient(point, psi, surface)
        new_x = self._calculate_new_value(point.x, vector_x)
        new_y = self._calculate_new_value(point.y, vector_y)
        new_point = Point(new_x, new_y)
        return new_point

    def _get_gradient(self, point, psi, mut_surf):
        vector_x = self._get_x_gradient(point, psi, mut_surf)
        vector_y = self._get_y_gradient(point, psi, mut_surf)
        return vector_x, vector_y

    def _get_x_gradient(self, point, psi, mut_surf):
        point_with_x_shift = Point(point.x+self._h, point.y)
        new_surface = self._get_surface_with_replaced_point(
            mut_surf, point, point_with_x_shift)
        shift_psi = self._get_psi(new_surface)
        vector = (shift_psi - psi) / self._h
        return vector

    def _get_y_gradient(self, point, psi, mut_surf):
        point_with_y_shift = Point(point.x, point.y+self._h)
        new_surface = self._get_surface_with_replaced_point(
            mut_surf, point, point_with_y_shift)
        shift_psi = self._get_psi(new_surface)
        vector = (shift_psi - psi) / self._h
        return vector

    def _should_recalculate(self, psi, surface, point, new_point):
        replaced_surface = self._get_surface_with_replaced_point(
            surface, point, new_point)
        new_psi = self._get_psi(replaced_surface)
        return new_psi > psi

    def _get_surface_with_replaced_point(self, surface, old_point, new_point):
        new_surface = surface[:]
        new_surface.replace(old_point, new_point)
        return new_surface

    def _calculate_new_value(self, value, vector):
        return value - self._ds * vector

    def _get_psi(self, mut_surf):
        psi = 0
        immut_surf = self._immutable_surface
        avg = self._get_avg_value(mut_surf, immut_surf)
        for mut_point, immut_point in product(mut_surf, immut_surf):
            psi += (mut_point.length_to(immut_point) - avg)**2

        for mut_point1, mut_point2 in combinations(mut_surf, 2):
            psi += (mut_point1.length_to(mut_point2)-avg)**2

        for immut_point1, immut_point2 in combinations(immut_surf, 2):
            psi += (immut_point1.length_to(immut_point2)-avg)**2

        return psi

    def _get_avg_value(self, mut_surf, immut_surf):
        total_length = 0
        count = 0
        for mut_point in mut_surf:
            for immut_point in immut_surf:
                total_length += mut_point.length_to(immut_point)
                count += 1
        for point1, point2 in combinations(mut_surf, 2):
            total_length += point1.length_to(point2)
            count += 1
        for point1, point2 in combinations(immut_surf, 2):
            total_length += point1.length_to(point2)
            count += 1
        avg_length = total_length / count
        self._avg_length = avg_length

        return avg_length
