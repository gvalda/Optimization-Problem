from time import sleep
from matplotlib import pyplot as plt

from config import GRAPHS_FOLDER


def save_ax(name, ax):
    fig = ax.get_figure()
    fig.savefig(f'{GRAPHS_FOLDER}/{name}.jpg')
    plt.show()
    fig.clf()


def plot_series(name, series, ylabel=''):
    ax = series.plot(figsize=(20, 10), ylabel=ylabel)
    save_ax(name, ax)


def plot_pivot_table(name, table, ylabel=''):
    ax = table.plot(ylabel='Time, s', figsize=(
        20, 10), xticks=table.index)
    save_ax(name, ax)
