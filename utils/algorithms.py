from multiprocessing import Pool
from itertools import product, combinations
from models.surface import Surface
from models.point import Point
import tqdm


def check_threads_quantity(quantity):
    if quantity < 1:
        raise Exception('Quantity of threads cannot be less than 1')


class GradientDescentOptimization:
    def __init__(self, immutable_surface=None, mutable_surface=None, ds=0.0001, h=0.01, accuracy=0.005, threads_quantity=1, show_PSI=True):
        self._ds = ds
        self._h = h
        self._accuracy = accuracy
        self._immutable_surface = immutable_surface
        self._mutable_surface = mutable_surface
        self._threads_quantity = threads_quantity
        self._show_PSI = show_PSI

    def __call__(self, surface=None):
        if surface:
            self._mutable_surface = surface
        if not hasattr(self, '_mutable_surface') or not self._mutable_surface:
            return
        self._mutable_surface_psi = self._get_psi(self._mutable_surface)
        with Pool(self._threads_quantity) as p:
            while True:
                new_points = []
                check_threads_quantity(self._threads_quantity)
                for point in tqdm.tqdm(p.map(self._get_new_point, self._mutable_surface), total=len(self._mutable_surface)):
                    new_points.append(point)
                new_surface = Surface(new_points)
                new_psi = self._get_psi(new_surface)
                if self._show_PSI:
                    print(f'PSI: {new_psi}')
                yield new_surface, new_psi
                if abs(self._mutable_surface_psi - new_psi)/new_psi*100 < self._accuracy:
                    break
                self._mutable_surface = new_surface
                self._mutable_surface_psi = new_psi

    def _get_new_point(self, point):
        x_shifted_point = self._get_x_shifted_point(point)
        vector_x = self._get_gradient(point, x_shifted_point)
        new_x = self._calculate_new_value(point.x, vector_x)

        y_shifted_point = self._get_y_shifted_point(point)
        vector_y = self._get_gradient(point, y_shifted_point)
        new_y = self._calculate_new_value(point.y, vector_y)

        new_point = Point(new_x, new_y)
        return new_point

    def _get_x_shifted_point(self, point):
        return Point(point.x + self._h, point.y)

    def _get_y_shifted_point(self, point):
        return Point(point.x, point.y + self._h)

    def _get_gradient(self, point, shifted_point):
        muttable_surface = self._mutable_surface
        new_surface = self._get_surface_with_replaced_point(
            muttable_surface, point, shifted_point)
        shift_psi = self._get_psi(new_surface)
        vector = (shift_psi - self._mutable_surface_psi) / self._h
        return vector

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
        for mut_point, immut_point in product(mut_surf, immut_surf):
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
