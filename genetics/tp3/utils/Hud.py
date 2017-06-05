import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style
import numpy as np


class Hud:

    def __init__(self, print_interval: int) -> None:
        super().__init__()
        self.print_interval = print_interval
        self.fitness_list = []
        # print(plt.style.available)
        # style.use('fivethirtyeight')
        #self.fig, self.ax = plt.subplots()
        #self.line, = self.ax.plot([0])
        #self.ax.set_ylim(0, 1)

        #ani = animation.FuncAnimation(self.fig, self.update, interval=1000)
        #plt.ion()
        #plt.show()

    #def update(self):
    #    self.line.set_ydata(self.line.get_ydata())
    #    return self.line,

    # def add_point(self):
    #    while True:
    #       yield

    def add_points_get_max(self, generation, population):
        self.fitness_list = [individual.fitness for individual in population]
        max_fitness = self.get_max_fitness()
        if generation % self.print_interval == 0:
            print("Generation:", generation)
            print("Avg fitness: {}".format(self.get_avg_fitness()))
            print("Max fitness: {}".format(max_fitness))
            print("Min fitness: {}".format(self.get_min_fitness()))
        return max_fitness

    def get_min_fitness(self):
        return np.max(self.fitness_list)

    def get_max_fitness(self):
        return np.min(self.fitness_list)

    def get_avg_fitness(self):
        return np.average(self.fitness_list)