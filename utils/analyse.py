import multiprocessing
from time import time

LOGICAL_CORES = multiprocessing.cpu_count()


def analyze_one(iterable, iterations=10):
    start = time()
    step_timings = [start]
    for _ in iterable:
        step = time()
        step_timings.append(step)
        iterations -= 1
        if iterations <= 0:
            break
    step_durations = [step_timings[i+1] - step_timings[i]
                      for i in range(len(step_timings)-1)]
    return step_durations


def analyze_all(data, analyzedClass, iterations=10):
    for num, ds in data:
        ds = list(ds)
        ds_size = len(ds[0])*2
        for threads_quantity in range(1, LOGICAL_CORES+1, 3):
            step_durations = []
            while True:
                analyzedObject = analyzedClass(
                    *ds, threads_quantity=threads_quantity)
                step_durations.extend(analyze_one(
                    analyzedObject(), iterations=iterations))
                if(len(step_durations) >= iterations):
                    break
            yield(step_durations, num, ds_size, threads_quantity)
