import sys
from statistics import mean
from models.point import Point
from models.surface import Surface
from config import RESULTS_PATH_TEMPLATE
from utils.analyse import analyze_all, analyze_one
from utils.graph import plot_pivot_table, plot_series, save_ax
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


def display_result(dataset_number, threads_quantity, step_durations):
    print(f'Dataset number: {dataset_number}')
    print(f'Threads quantity: {threads_quantity}')
    print(build_table(['Time elapsed'], [[step]
                                         for step in step_durations], row_numbers=True))
    total_time = sum(step_durations)
    average_time = total_time / len(step_durations)
    print(f'Total time: {total_time}')
    print(f'Average time: {average_time}')


def analyze_one_dataset(argv):
    if len(argv) < 3:
        raise Exception('Not enough paramenters for specified mode')
    dataset_number, threads_quantity = (int(arg) for arg in argv[1:3])
    dataset = read_dataset(dataset_number)
    immutable_surface, mutable_surface = split_dataset_into_surfaces(dataset)
    gdo = GradientDescentOptimization(
        immutable_surface, mutable_surface, threads_quantity=threads_quantity)
    step_durations = analyze_one(gdo())
    display_result(dataset_number, threads_quantity, step_durations)


def analyze_everything():
    datasets = read_all_datasets()
    data = ((num, split_dataset_into_surfaces(dataset))
            for num, dataset in datasets)
    for step_durations, dataset_number, dataset_size, threads_quantity in analyze_all(data, GradientDescentOptimization, 10):
        display_result(dataset_number, threads_quantity, step_durations)
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

    df['Mean'] = df.apply(lambda row: mean(row['measured-results']), axis=1)
    threads_q_by_dataset = df.pivot_table(
        index='threads-quantity', columns='dataset', values='Mean')
    for dataset, row in threads_q_by_dataset.iteritems():
        plot_series(f'dataset-{dataset}', row, ylabel='Time, s')
    plot_pivot_table('cumulative_graphs_by_threads',
                     threads_q_by_dataset, 'Time, s')
    size_by_threads_q = df.pivot_table(
        index='size', columns='threads-quantity', values='Mean')
    plot_pivot_table('cumulative_graphs_by_size', size_by_threads_q, 'Time, s')
    print('Graphs are build!')


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
