import sys
from models.point import Point
from models.surface import Surface
from config import RESULTS_PATH_TEMPLATE
from utils.analyse import analyze_all, analyze_one
from utils.jsonIO import read_json, write_json
from utils.algorithms import *
from utils.dataset import read_all_datasets, read_dataset
from utils.table_builder import build_table


def get_start_arguments():
    return sys.argv[1:]


def make_points_surface_from_dict(dict):
    surface = Surface([Point(**point) for point in dict])
    return surface


def split_dataset_into_surfaces(dataset):
    immutable_surface = make_points_surface_from_dict(
        dataset['immutable-points'])
    mutable_surface = make_points_surface_from_dict(dataset['mutable-points'])
    return immutable_surface, mutable_surface


def analyze_one_dataset(argv):
    if len(argv) < 3:
        raise Exception('Not enough paramenters for specified mode')
    dataset_number, threads_quantity = (int(arg) for arg in argv[1:3])
    dataset = read_dataset(dataset_number)
    immutable_surface, mutable_surface = split_dataset_into_surfaces(dataset)
    gdo = GradientDescentOptimization(
        immutable_surface, mutable_surface, threads_quantity=threads_quantity)
    analyze_one(gdo())


def analyze_everything():
    datasets = read_all_datasets()
    data = ((num, split_dataset_into_surfaces(dataset))
            for num, dataset in datasets)
    for step_durations, dataset_number, dataset_size, threads_quantity in analyze_all(data, GradientDescentOptimization, 10):
        print(f'Dataset number: {dataset_number}')
        print(f'Threads quantity: {threads_quantity}')
        print(f'Total time: {sum(step_durations)}')
        print(build_table(['Time elapsed'], [[step]
                                             for step in step_durations], row_numbers=True))
        result_dict = {
            'dataset': dataset_number,
            'size': dataset_size,
            'threads-quantity': threads_quantity,
            'measured-results': step_durations,
        }
        write_json(RESULTS_PATH_TEMPLATE(
            dataset_number, threads_quantity), result_dict)


def analyze_results():
    pass


def main():
    argv = get_start_arguments()
    if len(argv) < 1:
        raise Exception('Not enough parameters to choose execution mode')
    mode = int(argv[0])
    if mode == 0:
        analyze_one_dataset(argv)
    elif mode == 1:
        analyze_everything()
    elif mode == 2:
        analyze_results()


if __name__ == '__main__':
    main()
