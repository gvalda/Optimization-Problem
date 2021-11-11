MIN_DATASET_NUMBER = 1
MAX_DATASET_NUMBER = 8


def DATASET_PATH_TEMPLATE(number): return f'./resources/dataset-{number}.json'


def RESULTS_PATH_TEMPLATE(dataset_number, threads_quantity):
    return f'./results/result-{dataset_number}-{threads_quantity}.json'
