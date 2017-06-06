import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


class Hud:
    def __init__(self, print_interval: int, max_generations, max_fitness) -> None:
        super().__init__()
        self.print_interval = print_interval
        self.points = [(0, 0.0, 0.0, 0.0, 0.0)]
        print(plt.style.available)
        #plt.xkcd()
        self.fig, self.ax = plt.subplots()
        self.min_line, = self.ax.plot([0], [0], label="Min")
        self.avg_line, = self.ax.plot([0], [0], label="Avg")
        self.max_line, = self.ax.plot([0], [0], label="Max")

        self.ax.set_ylabel("Fitness")
        self.ax.set_xlabel("Generation")
        self.ax.set_xlim(0, max_generations)
        self.ax.set_ylim(0, max_fitness)
        self.fig.canvas.set_window_title("TPE3 - GENETICS")

        ani = animation.FuncAnimation(self.fig, self._update, interval=100)
        plt.ion()
        plt.draw()
        plt.show()
        plt.pause(0.01)

    def _set_texts(self):
        self.ax.set_title("Generation: ${}$".format(self.get_generation()))
        self.min_line.set_label("Min: ${0:.2f}$".format(self.get_min_fitness()))
        self.avg_line.set_label("Avg: ${0:.2f}$".format(self.get_avg_fitness()))
        self.max_line.set_label("Max: ${0:.2f}$".format(self.get_max_fitness()))
        plt.legend(handles=[self.max_line, self.avg_line, self.min_line])

    def _update(self, i):
        self._set_texts()
        self.min_line.set_xdata([p[0] for p in self.points])
        self.min_line.set_ydata([p[1] for p in self.points])

        self.avg_line.set_xdata([p[0] for p in self.points])
        self.avg_line.set_ydata([p[2] for p in self.points])

        self.max_line.set_xdata([p[0] for p in self.points])
        self.max_line.set_ydata([p[3] for p in self.points])
        return self.min_line, self.avg_line, self.max_line,

    def add_points_get_max(self, generation, population):
        fitness_list = [individual.fitness for individual in population]
        self.points.append((
            generation,
            np.min(fitness_list),
            np.average(fitness_list),
            np.max(fitness_list),
        ))
        if generation % self.print_interval == 0:
            plt.pause(0.001)
            print("Generation:", generation)
            print("Avg fitness: {}".format(self.get_avg_fitness()))
            print("Max fitness: {}".format(self.get_max_fitness()))
            print("Min fitness: {}".format(self.get_min_fitness()))
        return self.get_max_fitness()

    def get_generation(self):
        return self.points[-1][0]

    def get_min_fitness(self):
        return self.points[-1][1]

    def get_avg_fitness(self):
        return self.points[-1][2]

    def get_max_fitness(self):
        return self.points[-1][3]

    def get_last_fitness(self):
        return self.points[-1]

    def wait(self):
        plt.ioff()
        plt.show()
