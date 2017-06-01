import numpy as np
from .algorithms.genetic import Genetic
from .models.characters import Character, Warrior, Archer, Defender, Assassin
from .models.items import ItemType
from .utils.parser import parse
from random import sample
from .utils.config import Config
from .algorithms.selection import set_tournament_constants
from .algorithms.selection import set_boltzmann_constants


def print_stats(population):
    fitness_list = []
    for character in population:
        fitness_list.append(character.fitness)

    avg_fitness = np.average(fitness_list)
    max_fitness = np.max(fitness_list)
    min_fitness = np.min(fitness_list)
    print("Avg fitness: {}".format(avg_fitness))
    print("Max fitness: {}".format(max_fitness))
    print("Min fitness: {}".format(min_fitness))


def generate_individuals(amount, items, population_class):
    population = []
    for _ in range(amount):
        individual = class_setter(population_class)
        individual.set_item(sample(items[0], 1)[0])
        individual.set_item(sample(items[1], 1)[0])
        individual.set_item(sample(items[2], 1)[0])
        individual.set_item(sample(items[3], 1)[0])
        individual.set_item(sample(items[4], 1)[0])
        individual.calculate_fitness()
        population.append(individual)
    return population


def class_setter(population_class):
    return {
        'warrior': Warrior(),
        'archer': Archer(),
        'defender': Defender(),
        'assassin': Assassin(),
    }[population_class]


def databases(config: Config):
    def build_items(src_file, item_type):
        data, err = parse("{}/{}.tsv".format(config.dataset, src_file), item_type)
        if err is not None:
            raise err
        return data
    weapons = build_items("armas", ItemType.WEAPON)
    boots = build_items("botas", ItemType.BOOTS)
    helmets = build_items("cascos", ItemType.HELMET)
    gloves = build_items("guantes", ItemType.GLOVES)
    armours = build_items("pecheras", ItemType.ARMOUR)
    return weapons, boots, helmets, gloves, armours


def main():
    config = Config("config.json")
    set_tournament_constants(randomness=config.randomness, tournaments_times=config.tournaments_times)
    set_boltzmann_constants(config.boltzmann_starting_temp, config.boltzmann_minimum_temp, config.boltzmann_cooling_step)
    items = databases(config)
    population_size = config.population_size
    Character.set_special_modifiers(config.special_modifiers)
    population_class = config.population_class
    population = generate_individuals(population_size, items, population_class)
    experiment = Genetic(config, population, items)
    experiment.natural_selection()


if __name__ == "__main__":
    main()
