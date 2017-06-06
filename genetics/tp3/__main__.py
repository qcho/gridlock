from random import sample

from multiprocessing import freeze_support

from .algorithms.genetic import Genetic
from .algorithms.selection import set_tournament_constants, set_boltzmann_constants
from .models.characters import Character, Warrior, Archer, Defender, Assassin
from .utils.Hud import Hud
from .utils.config import Config
from .utils.parser import databases
import cProfile


def generate_individuals(amount, items, population_class):
    population = []
    for _ in range(amount):
        individual = class_setter(population_class)
        individual.set_item(sample(items[0], 1)[0])
        individual.set_item(sample(items[1], 1)[0])
        individual.set_item(sample(items[2], 1)[0])
        individual.set_item(sample(items[3], 1)[0])
        individual.set_item(sample(items[4], 1)[0])
        population.append(individual)
    return population


def class_setter(population_class):
    return {
        'warrior': Warrior(),
        'archer': Archer(),
        'defender': Defender(),
        'assassin': Assassin(),
    }[population_class]


def main():
    freeze_support()
    config = Config("config.json")
    set_tournament_constants(randomness=config.randomness, tournaments_group_size=config.tournaments_group_size)
    set_boltzmann_constants(config.boltzmann_starting_temp, config.boltzmann_minimum_temp, config.boltzmann_cooling_step)
    items = databases(config.dataset)
    population_size = config.population_size
    Character.set_special_modifiers(config.special_modifiers)
    population_class = config.population_class
    population = generate_individuals(population_size, items, population_class)
    experiment = Genetic(config, population, items)
    hud = Hud(config)
    experiment.natural_selection(hud)

if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort='cumtime')
