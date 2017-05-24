import numpy as np

def relative_aptitude(population):
    all_fitness = np.sum(list(map(lambda x: x.fitness, population)))
    return list(map(lambda x: x.fitness / all_fitness, population))