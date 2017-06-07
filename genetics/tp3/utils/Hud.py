from abc import ABCMeta
import sys
from operator import attrgetter

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
    fig = None
    axs = None
    min_line = None
    avg_line = None
    max_line = None
    str_line = None
    height_line = None
    agi_line = None
    exp_line = None
    res_line = None
    life_line = None
    points = None
    initialized = False
    references = 0

    def __init__(self, config: Config):
        super().__init__(config)
        PlotOutput.references += 1
        if PlotOutput.initialized:
            self.points.append((0, 0.0, 0.0, 0.0, 0.0))
            self.stats.append((0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            return

        PlotOutput.fig, PlotOutput.axs = plt.subplots(2, sharex=True)
        PlotOutput.fig.canvas.set_window_title("TPE3 - GENETICS")

        self.points.append((0, 0.0, 0.0, 0.0, 0.0))
        PlotOutput.min_line, = PlotOutput.axs[0].plot([0], [0], label="Min")
        PlotOutput.avg_line, = PlotOutput.axs[0].plot([0], [0], label="Avg")
        PlotOutput.max_line, = PlotOutput.axs[0].plot([0], [0], label="Max")
        PlotOutput.axs[0].set_ylabel("Fitness")
        PlotOutput.axs[0].set_xlabel("Generation")
        PlotOutput.axs[0].set_xlim(0, config.generations_limit)
        PlotOutput.axs[0].set_ylim(0, config.goal_score)

        self.stats.append((0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        PlotOutput.height_line, = PlotOutput.axs[1].plot([0], [0], label="Height")
        PlotOutput.str_line, = PlotOutput.axs[1].plot([0], [0], label="Strength")
        PlotOutput.agi_line, = PlotOutput.axs[1].plot([0], [0], label="Agility")
        PlotOutput.exp_line, = PlotOutput.axs[1].plot([0], [0], label="Expertise")
        PlotOutput.res_line, = PlotOutput.axs[1].plot([0], [0], label="Resilience")
        PlotOutput.life_line, = PlotOutput.axs[1].plot([0], [0], label="Life")
        PlotOutput.axs[1].set_ylabel("Best individual stats")
        PlotOutput.axs[1].set_xlabel("Generation")
        PlotOutput.axs[1].set_xlim(0, config.generations_limit)
        PlotOutput.axs[1].set_ylim(0, 100)
        PlotOutput.axs[1].set_yscale("symlog")
        PlotOutput.initialized = True

    def _update(self, _):
        self._set_texts()
        PlotOutput.min_line.set_xdata([p[0] for p in self.points])
        PlotOutput.min_line.set_ydata([p[1] for p in self.points])
        PlotOutput.avg_line.set_xdata([p[0] for p in self.points])
        PlotOutput.avg_line.set_ydata([p[2] for p in self.points])
        PlotOutput.max_line.set_xdata([p[0] for p in self.points])
        PlotOutput.max_line.set_ydata([p[3] for p in self.points])

        PlotOutput.min_line.set_xdata([p[0] for p in self.points])
        PlotOutput.min_line.set_ydata([p[1] for p in self.points])
        PlotOutput.avg_line.set_xdata([p[0] for p in self.points])
        PlotOutput.avg_line.set_ydata([p[2] for p in self.points])
        PlotOutput.max_line.set_xdata([p[0] for p in self.points])
        PlotOutput.max_line.set_ydata([p[3] for p in self.points])

        PlotOutput.height_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.height_line.set_ydata([p[1] for p in self.stats])
        PlotOutput.str_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.str_line.set_ydata([p[2] for p in self.stats])
        PlotOutput.agi_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.agi_line.set_ydata([p[3] for p in self.stats])
        PlotOutput.exp_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.exp_line.set_ydata([p[4] for p in self.stats])
        PlotOutput.res_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.res_line.set_ydata([p[5] for p in self.stats])
        PlotOutput.life_line.set_xdata([p[0] for p in self.stats])
        PlotOutput.life_line.set_ydata([p[6] for p in self.stats])

        return PlotOutput.min_line, PlotOutput.avg_line, PlotOutput.max_line, \
            PlotOutput.height_line, \
            PlotOutput.str_line, \
            PlotOutput.agi_line, \
            PlotOutput.exp_line, \
            PlotOutput.res_line, \
            PlotOutput.life_line

    def _set_texts(self):
        PlotOutput.axs[0].set_title("Generation: ${}$".format(self.get_generation()))
        PlotOutput.min_line.set_label("Min: ${0:.2f}$".format(self.get_min_fitness()))
        PlotOutput.avg_line.set_label("Avg: ${0:.2f}$".format(self.get_avg_fitness()))
        PlotOutput.max_line.set_label("Max: ${0:.2f}$".format(self.get_max_fitness()))
        if self.best_individual is not None:
            PlotOutput.height_line.set_label("Height: ${0:.2f}$".format(self.best_individual.height))
            PlotOutput.str_line.set_label("Strength: ${0:.2f}$".format(self.best_individual.strength))
            PlotOutput.agi_line.set_label("Agility: ${0:.2f}$".format(self.best_individual.agility))
            PlotOutput.exp_line.set_label("Expertise: ${0:.2f}$".format(self.best_individual.expertise))
            PlotOutput.res_line.set_label("Resilience: ${0:.2f}$".format(self.best_individual.resistance))
            PlotOutput.life_line.set_label("Life: ${0:.2f}$".format(self.best_individual.life))

        PlotOutput.axs[0].legend(handles=[PlotOutput.max_line, PlotOutput.avg_line, PlotOutput.min_line])
        PlotOutput.axs[1].legend(handles=[
            PlotOutput.height_line,
            PlotOutput.str_line,
            PlotOutput.agi_line,
            PlotOutput.exp_line,
            PlotOutput.res_line,
            PlotOutput.life_line,
        ])

    def finish(self):
        super().finish()
        PlotOutput.references -= 1
        if PlotOutput.references == 0:
            plt.close()
            PlotOutput.fig = None
            PlotOutput.axs = None
            PlotOutput.min_line = None
            PlotOutput.avg_line = None
            PlotOutput.max_line = None
            PlotOutput.str_line = None
            PlotOutput.height_line = None
            PlotOutput.agi_line = None
            PlotOutput.exp_line = None
            PlotOutput.res_line = None
            PlotOutput.life_line = None
            PlotOutput.points = None
            PlotOutput.initialized = False


class RealtimeOutput(PlotOutput):
    def __init__(self, config: Config):
        super().__init__(config)
        self.print_interval = config.print_interval
        _ = animation.FuncAnimation(PlotOutput.fig, self._update, interval=100)
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
        super().finish()


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
        super().finish()


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
        self.points = []
        self.stats = []
        self.output_methods = _init_output_methods(config)

    def add_points_get_max(self, generation, population):
        fitness_list = []
        best_individual = None
        for individual in population:
            if best_individual is None or best_individual.fitness < individual.fitness:
                best_individual = individual
            fitness_list.append(individual.fitness)
        self.points.append((
            generation,
            np.min(fitness_list),
            np.average(fitness_list),
            np.max(fitness_list),
        ))
        self.stats.append((
            generation,
            best_individual.height,
            best_individual.strength,
            best_individual.agility,
            best_individual.expertise,
            best_individual.resistance,
            best_individual.life
        ))
        for output_method in self.output_methods:
            output_method.process_generation(self.points, self.stats, best_individual)
        return self.get_max_fitness()

    def get_max_fitness(self):
        return _max_fitness(self.points)

    def finish(self):
        for output_method in self.output_methods:
            output_method.finish()
