import numpy as np


def relative_aptitude(population):
    all_fitness = np.sum([x.fitness for x in population])
    return [x.fitness / all_fitness for x in population]
