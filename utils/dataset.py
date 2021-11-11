from utils.jsonIO import read_json
from config import DATASET_PATH_TEMPLATE, MIN_DATASET_NUMBER, MAX_DATASET_NUMBER


def is_dataset_exists(number):
    return number >= MIN_DATASET_NUMBER and number <= MAX_DATASET_NUMBER


def read_dataset(number):
    if not is_dataset_exists(number):
        raise Exception('Inappropriate dataset number')
    print('Reading dataset from a file')
    return read_json(DATASET_PATH_TEMPLATE(number))


def read_all_datasets():
    for num in range(MIN_DATASET_NUMBER, MAX_DATASET_NUMBER+1):
        yield num, read_dataset(num)
