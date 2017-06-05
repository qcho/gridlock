from random import sample

from .algorithms.genetic import Genetic
from .algorithms.selection import set_tournament_constants, set_boltzmann_constants
from .models.characters import Character, Warrior, Archer, Defender, Assassin
from .models.items import ItemType
from .utils.Hud import Hud
from .utils.config import Config
from .utils.parser import parse


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

def run(config: Config):


def main():
    if ()

    config = Config("config.json")
    set_tournament_constants(randomness=config.randomness, tournaments_group_size=config.tournaments_group_size)
    set_boltzmann_constants(config.boltzmann_starting_temp, config.boltzmann_minimum_temp, config.boltzmann_cooling_step)
    items = databases(config)
    population_size = config.population_size
    Character.set_special_modifiers(config.special_modifiers)
    population_class = config.population_class
    population = generate_individuals(population_size, items, population_class)
    experiment = Genetic(config, population, items)
    hud = Hud(
        config.print_interval,
        config.generations_limit,
        config.goal_score
    )
    experiment.natural_selection(hud)
    hud.wait()

if __name__ == "__main__":
    main()
