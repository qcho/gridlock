import numpy as np
from .algorithms.genetic import Genetic

class Executor:
    def __init__(self, items, experiment: Genetic, name: str):
        self.items = items
        self.experiment = experiment
        self.name = name


    def run(self, generations: int):
        for _ in range(generations):
            fitness_list = self.experiment.generation()


        avg_fitness = np.average(list(map(lambda x: x.fitness, fitness_list)))
        max_fitness = np.max(list(map(lambda x: x.fitness, fitness_list)))
        min_fitness = np.min(list(map(lambda x: x.fitness, fitness_list)))
        print(self.name)
        print("Avg fitness: {}".format(avg_fitness))
        print("Max fitness: {}".format(max_fitness))
        print("Min fitness: {}".format(min_fitness))
        print("--------------------------------------------------------------------------------")
        for x in fitness_list:
            if x.fitness == max_fitness:
                return x
        return None