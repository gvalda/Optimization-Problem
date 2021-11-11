import sys
from statistics import mean
from models.point import Point
from models.surface import Surface
from config import RESULTS_PATH_TEMPLATE
from utils.analyse import analyze_all, analyze_one
from utils.graph import plot_series, save_ax
from utils.jsonIO import read_json, write_json
from utils.algorithms import *
from utils.data_manager import read_all_datasets, read_dataset, read_all_results
from utils.table_builder import build_table
import pandas as pd
import numpy as np


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
    results = read_all_results()
    df = pd.DataFrame(results)
    df = df.sort_values(['dataset', 'threads-quantity'])

    df['MEAN'] = df.apply(lambda row: mean(row['measured-results']), axis=1)
    threads_q_by_dataset = df.pivot_table(
        index='threads-quantity', columns='dataset', values='MEAN')
    for dataset, row in threads_q_by_dataset.iteritems():
        plot_series(f'dataset-{dataset}', row, ylabel='Time, s')
    ax = threads_q_by_dataset.plot(ylabel='Time, s', figsize=(
        20, 10), xticks=threads_q_by_dataset.index)
    save_ax('cumulative_graphs_by_threads', ax)

    size_by_threads_q = df.pivot_table(
        index='size', columns='threads-quantity', values='MEAN')
    ax = size_by_threads_q.plot(ylabel='Time, s', figsize=(
        20, 10), xticks=size_by_threads_q.index)
    save_ax('cumulative_graphs_by_size', ax)


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
