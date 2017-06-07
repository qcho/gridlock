from abc import ABCMeta
import sys

import matplotlib.pyplot as plt
import numpy as np
import pkg_resources
from matplotlib import animation

from .config import Config
from ..data import __data_pkg__


def _max_fitness(points):
    return points[-1][3]


class Output:
    __metaclass__ = ABCMeta

    def __init__(self, config: Config):
        self.points = []
        self.stats = []
        self.config = config
        self.best_individual = None

    def process_generation(self, points, stats, best_individual):
        self.points = points
        self.stats = stats
        self.best_individual = best_individual

    def finish(self):
        pass

    def get_generation(self):
        return self.points[-1][0]

    def get_min_fitness(self):
        return self.points[-1][1]

    def get_avg_fitness(self):
        return self.points[-1][2]

    def get_max_fitness(self):
        return _max_fitness(self.points)


class PlotOutput(Output):
    def __init__(self, config: Config):
        super().__init__(config)

        self.fig, self.axs = plt.subplots(2, sharex=True)
        self.fig.canvas.set_window_title("TPE3 - GENETICS")

        self.points.append((0, 0.0, 0.0, 0.0, 0.0))
        self.min_line, = self.axs[0].plot([0], [0], label="Min")
        self.avg_line, = self.axs[0].plot([0], [0], label="Avg")
        self.max_line, = self.axs[0].plot([0], [0], label="Max")
        self.axs[0].set_ylabel("Fitness")
        self.axs[0].set_xlabel("Generation")
        self.axs[0].set_xlim(0, config.generations_limit)
        self.axs[0].set_ylim(0, config.goal_score)

        self.stats.append((0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        self.height_line, = self.axs[1].plot([0], [0], label="Height")
        self.str_line, = self.axs[1].plot([0], [0], label="Strength")
        self.agi_line, = self.axs[1].plot([0], [0], label="Agility")
        self.exp_line, = self.axs[1].plot([0], [0], label="Experience")
        self.res_line, = self.axs[1].plot([0], [0], label="Resilience")
        self.life_line, = self.axs[1].plot([0], [0], label="Life")
        self.axs[1].set_ylabel("Best individual stats")
        self.axs[1].set_xlabel("Generation")
        self.axs[1].set_xlim(0, config.generations_limit)
        self.axs[1].set_ylim(0, 100)
        self.axs[1].set_yscale("symlog")

    def _update(self, _):
        self._set_texts()
        self.min_line.set_xdata([p[0] for p in self.points])
        self.min_line.set_ydata([p[1] for p in self.points])
        self.avg_line.set_xdata([p[0] for p in self.points])
        self.avg_line.set_ydata([p[2] for p in self.points])
        self.max_line.set_xdata([p[0] for p in self.points])
        self.max_line.set_ydata([p[3] for p in self.points])

        self.min_line.set_xdata([p[0] for p in self.points])
        self.min_line.set_ydata([p[1] for p in self.points])
        self.avg_line.set_xdata([p[0] for p in self.points])
        self.avg_line.set_ydata([p[2] for p in self.points])
        self.max_line.set_xdata([p[0] for p in self.points])
        self.max_line.set_ydata([p[3] for p in self.points])

        self.height_line.set_xdata([p[0] for p in self.stats])
        self.height_line.set_ydata([p[1] for p in self.stats])
        self.str_line.set_xdata([p[0] for p in self.stats])
        self.str_line.set_ydata([p[2] for p in self.stats])
        self.agi_line.set_xdata([p[0] for p in self.stats])
        self.agi_line.set_ydata([p[3] for p in self.stats])
        self.exp_line.set_xdata([p[0] for p in self.stats])
        self.exp_line.set_ydata([p[4] for p in self.stats])
        self.res_line.set_xdata([p[0] for p in self.stats])
        self.res_line.set_ydata([p[5] for p in self.stats])
        self.life_line.set_xdata([p[0] for p in self.stats])
        self.life_line.set_ydata([p[6] for p in self.stats])

        return self.min_line, self.avg_line, self.max_line, \
            self.height_line, \
            self.str_line, \
            self.agi_line, \
            self.exp_line, \
            self.res_line, \
            self.life_line

    def _set_texts(self):
        self.axs[0].set_title("Generation: ${}$".format(self.get_generation()))
        self.min_line.set_label("Min: ${0:.2f}$".format(self.get_min_fitness()))
        self.avg_line.set_label("Avg: ${0:.2f}$".format(self.get_avg_fitness()))
        self.max_line.set_label("Max: ${0:.2f}$".format(self.get_max_fitness()))
        if self.best_individual is not None:
            self.height_line.set_label("Height: ${0:.2f}$".format(self.best_individual.height))
            self.str_line.set_label("Strength: ${0:.2f}$".format(self.best_individual.strength))
            self.agi_line.set_label("Agility: ${0:.2f}$".format(self.best_individual.agility))
            self.exp_line.set_label("Experience: ${0:.2f}$".format(self.best_individual.expertise))
            self.res_line.set_label("Resilience: ${0:.2f}$".format(self.best_individual.resistance))
            self.life_line.set_label("Life: ${0:.2f}$".format(self.best_individual.life))

        self.axs[0].legend(handles=[self.max_line, self.avg_line, self.min_line])
        self.axs[1].legend(handles=[
            self.height_line,
            self.str_line,
            self.agi_line,
            self.exp_line,
            self.res_line,
            self.life_line,
        ])


class RealtimeOutput(PlotOutput):
    def __init__(self, config: Config):
        super().__init__(config)
        self.print_interval = config.print_interval
        _ = animation.FuncAnimation(self.fig, self._update, interval=100)
        plt.ion()
        plt.show()
        plt.pause(0.01)

    def process_generation(self, data, stats, best_individual):
        super().process_generation(data, stats, best_individual)
        if self.get_generation() % self.print_interval == 0:
            plt.pause(0.01)

    def finish(self):
        plt.ioff()
        plt.show()


class TextOutput(Output):
    def __init__(self, config: Config, file):
        super().__init__(config)
        self.file = file
        self.print_interval = config.print_interval

    def process_generation(self, data, stats, best_individual):
        super().process_generation(data, stats, best_individual)
        if self.get_generation() % self.print_interval == 0:
            print("Generation:", self.get_generation(), file=self.file)
            print("Avg fitness: {}".format(self.get_avg_fitness()), file=self.file)
            print("Max fitness: {}".format(self.get_max_fitness()), file=self.file)
            print("Min fitness: {}".format(self.get_min_fitness()), file=self.file)

    def finish(self):
        max_fitness = self.get_max_fitness()
        if self.config.generations_limit == self.get_generation():
            print("Max generation reached...Exiting with a best score of: {}".format(max_fitness), file=self.file)
        else:
            print("The target score was surpassed in generation: {} with a score of: {}"
                  .format(self.get_generation(), max_fitness), file=self.file)
        print("The individual stats are: \n{}".format(self.best_individual), file=self.file)
        if self.file != sys.stdout:
            self.file.close()


class FileOutput(PlotOutput):
    def __init__(self, config: Config):
        super().__init__(config)
        self.text_output = TextOutput(config, open(self.out_file_name() + ".txt", "w"))

    def process_generation(self, data, stats, best_individual):
        super().process_generation(data, stats, best_individual)
        self.text_output.process_generation(data, stats, best_individual)

    def out_file_name(self):
        return pkg_resources.resource_filename(__data_pkg__, "results/{}".format(self.config.filename))

    def finish(self):
        self._update(None)
        self.text_output.finish()
        plt.draw()
        plt.savefig(self.out_file_name() + ".png", dpi=300)
        plt.close()


def _init_output_methods(config: Config):
    output_methods = []
    if "console" in config.output_methods:
        output_methods.append(TextOutput(config, sys.stdout))
    if "file" in config.output_methods:
        output_methods.append(FileOutput(config))
    if "realtime" in config.output_methods:
        output_methods.append(RealtimeOutput(config))
    return output_methods


class Hud:
    def __init__(self, config: Config) -> None:
        self.best_individual = None
        self.points = []
        self.stats = []
        self.output_methods = _init_output_methods(config)

    def add_points_get_max(self, generation, population):
        fitness_list = []
        for individual in population:
            if self.best_individual is None or self.best_individual.fitness < individual.fitness:
                self.best_individual = individual
            fitness_list.append(individual.fitness)
        self.points.append((
            generation,
            np.min(fitness_list),
            np.average(fitness_list),
            np.max(fitness_list),
        ))
        self.stats.append((
            generation,
            self.best_individual.height,
            self.best_individual.strength,
            self.best_individual.agility,
            self.best_individual.expertise,
            self.best_individual.resistance,
            self.best_individual.life
        ))
        for output_method in self.output_methods:
            output_method.process_generation(self.points, self.stats, self.best_individual)
        return self.get_max_fitness()

    def get_max_fitness(self):
        return _max_fitness(self.points)

    def finish(self):
        for output_method in self.output_methods:
            output_method.finish()
