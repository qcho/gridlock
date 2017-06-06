import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from abc import ABCMeta, abstractmethod

from tp3.utils.config import Config


def _generation(points):
    return points[-1][0]


def _min_fitness(points):
    return points[-1][1]


def _avg_fitness(points):
    return points[-1][2]


def _max_fitness(points):
    return points[-1][3]


def _last_fitness(points):
    return points[-1]

class Output:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_generation(self, data):
        pass


class RealtimeOutput(Output):
    def __init__(self, config: Config):
        self.config = config

    def process_generation(self, data):
        pass


class ConsoleOutput(Output):
    def __init__(self, config: Config):
        self.config = config

    def process_generation(self, data):
        pass


class FileOutput(Output):
    def __init__(self, config: Config):
        self.config = config

    def process_generation(self, data):
        pass


class Hud:
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.print_interval = config.print_interval
        self.points = [(0, 0.0, 0.0, 0.0, 0.0)]
        self._init_output_methods(config)
        #plt.xkcd()
        self.fig, self.ax = plt.subplots()
        self.min_line, = self.ax.plot([0], [0], label="Min")
        self.avg_line, = self.ax.plot([0], [0], label="Avg")
        self.max_line, = self.ax.plot([0], [0], label="Max")

        self.ax.set_ylabel("Fitness")
        self.ax.set_xlabel("Generation")
        self.ax.set_xlim(0, config.generations_limit)
        self.ax.set_ylim(0, config.goal_score)
        self.fig.canvas.set_window_title("TPE3 - GENETICS")

        _ = animation.FuncAnimation(self.fig, self._update, interval=100)
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

    def _update(self, _):
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
            plt.pause(0.01)
            print("Generation:", generation)
            print("Avg fitness: {}".format(self.get_avg_fitness()))
            print("Max fitness: {}".format(self.get_max_fitness()))
            print("Min fitness: {}".format(self.get_min_fitness()))
        return self.get_max_fitness()

    def get_generation(self):
        return _generation(self.points)

    def get_min_fitness(self):
        return _min_fitness(self.points)

    def get_avg_fitness(self):
        return _avg_fitness(self.points)

    def get_max_fitness(self):
        return _max_fitness(self.points)

    def get_last_fitness(self):
        return _last_fitness(self.points)

    def wait(self):
        plt.ioff()
        plt.show()

    def _init_output_methods(self, config: Config):
        if "console" in config.output_methods:
            self._init_console(config)
        if "file" in config.output_methods:
            self._init_file(config)
        if "realtime" in config.output_methods:
            self._init_realtime(config)

    def _init_console(self, config: Config):
        pass

    def _init_file(self, config: Config):
        pass

    def _init_realtime(self, config: Config):
        pass
