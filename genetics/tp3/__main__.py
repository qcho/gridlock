import numpy as np
from algorithms.selection import stochastic_sample
from .models.characters import Warrior
from models.items import Armour, Boots, Gloves, Helmet, Weapon


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


def generate_individuals(amount):
    armour = Armour(1, 0.1, 0.2, 0.3, 0.4, 0.5)
    boots = Boots(1, 0.1, 0.2, 0.3, 0.4, 0.5)
    gloves = Gloves(1, 0.1, 0.2, 0.3, 0.4, 0.5)
    helmet = Helmet(1, 0.1, 0.2, 0.3, 0.4, 0.5)
    weapon = Weapon(1, 0.1, 0.2, 0.3, 0.4, 0.5)
    population = []
    for _ in range(amount):
        w = Warrior()
        w.add_item(armour)
        w.add_item(boots)
        w.add_item(gloves)
        w.add_item(helmet)
        w.add_item(weapon)
        w.calculate_fitness()
        population.append(w)
    return population


def main():
    population = generate_individuals(10)
    stochastic_sample(population, 5, type='universal')
    print_stats(population)


if __name__ == "__main__":
    main()
