import json


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
