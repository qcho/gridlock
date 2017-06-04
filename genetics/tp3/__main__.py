import numpy as np
from .algorithms.genetic import Genetic
from .models.characters import Character, Warrior, Archer, Defender, Assassin
from .models.items import ItemType
from .utils.parser import parse
from random import sample
from .utils.config import Config
from .algorithms.selection import set_tournament_constants, set_elite_roulette_constants, set_boltzmann_constants
from.executor import Executor
from copy import deepcopy


selection_algorithms = [
    'elite-sample',
    'random-sample',
    'roulette',
    'universal',
    'boltzmann',
    'tournaments-deterministic',
    'tournaments-stochastic',
    'ranking',
    'elitist-roulette'
]


crossover_algorithms = [
    'one_point',
    'two_points',
    'uniform',
    'annular'
]


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
    # Set constants
    config = Config("config.json")
    set_tournament_constants(randomness=config.randomness, tournaments_group_size=config.tournaments_group_size)
    set_boltzmann_constants(config.boltzmann_starting_temp, config.boltzmann_minimum_temp, config.boltzmann_cooling_step)
    set_elite_roulette_constants(config.elitist_roulette_ratio)
    items = databases(config)
    population_size = config.population_size
    Character.set_special_modifiers(config.special_modifiers)
    population_class = config.population_class
    # Randomize
    executors = []
    population = generate_individuals(population_size, items, population_class)
    for breed in selection_algorithms:
        for gap in selection_algorithms:
            for child_to_keep in selection_algorithms:
                for crossover in crossover_algorithms:
                    config.breed_selection_method = breed
                    config.generation_gap_selection_method = gap
                    config.child_to_keep_selection_method = child_to_keep
                    config.crossover_type = crossover
                    experiment = Genetic(config, deepcopy(population), items)
                    executors.append(Executor(items, experiment, name="{} {} {} {}".format(breed, gap, child_to_keep, crossover)))

    best = None
    of = None
    for ex in executors:
        best_child = ex.run(config.generations_limit)
        if best == None or best_child.fitness > best.fitness:
            best = best_child
            of = ex.name

    print("The best was:")
    print(best)
    print(of)


if __name__ == "__main__":
    main()
