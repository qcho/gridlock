from multiprocessing import freeze_support
from random import sample
import argparse
from .algorithms.genetic import Genetic
from .algorithms.selection import set_tournament_constants, set_boltzmann_constants
from .models.characters import Character, Warrior, Archer, Defender, Assassin
from .utils.Hud import Hud
from .utils.config import Config, all_configs
from .utils.parser import databases


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


def _run(config: Config):
    set_tournament_constants(randomness=config.randomness, tournaments_group_size=config.tournaments_group_size)
    set_boltzmann_constants(config.boltzmann_starting_temp, config.boltzmann_minimum_temp,
                            config.boltzmann_cooling_step)
    items = databases(config.dataset)
    population_size = config.population_size
    Character.set_special_modifiers(config.special_modifiers)
    population_class = config.population_class
    population = generate_individuals(population_size, items, population_class)
    experiment = Genetic(config, population, items)
    hud = Hud(config)
    experiment.natural_selection(hud)
    hud.finish()


def arg_parser():
    parser = argparse.ArgumentParser(description="SIA: Algorítmos genéticos")
    parser.add_argument('--config', metavar='config', nargs='?', default='default.json', help="Config to load")
    parser.add_argument('--all', help="Run all configs", action='store_true')
    return parser


def main():
    freeze_support()
    argument_parser = arg_parser()
    arguments = argument_parser.parse_args()
    config_files = [arguments.config] if not arguments.all else all_configs()

    for config_name in config_files:
        _run(Config(config_name))

if __name__ == "__main__":
    main()
