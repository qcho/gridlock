from itertools import accumulate
from random import sample, random
from ..utils.relative_aptitude import relative_aptitude


def elite_sample(population, amount: int):
    data = list(reversed(sorted(population, key=lambda x: x.fitness)))
    return data[:amount]


def random_sample(population, amount: int):
    return sample(population, amount)


def _between(array, value):
    # Special first case
    if value < array[0]:
        return 0
    # Rest of cases
    for i in range(1, len(array)):
        if array[i - 1] < value < array[i]:
            return i


def _accumulated_relative_fitness(population):
    relative_fitness = relative_aptitude(population)
    return list(accumulate(relative_fitness))


def _roulette(population, amount: int):
    accumulated = _accumulated_relative_fitness(population)

    result = []
    for _ in range(amount):
        r = random()
        i = _between(accumulated, r)
        result.append(population[i])

    return result


def _universal(population, amount: int):
    accumulated = _accumulated_relative_fitness(population)
    r = random()
    randoms = []
    for i in range(amount):
        randoms.append((r + i) / amount)

    result = []
    for r in randoms:
        i = _between(accumulated, r)
        result.append(population[i])

    return result


def _boltzmann(population, amount: int):
    return 1


def _tournaments(population, amount: int):
    return 1


def _ranking(population, amount: int):
    return 1


def stochastic_sample(population, amount: int, type: str):
    switcher = {
        'roulette': _roulette,
        'universal': _universal,
        'boltzmann': _boltzmann,
        'tournaments': _tournaments,
        'ranking': _ranking
    }
    func = switcher[type]
    return func(population, amount)

#TODO completar el diccionario
selection_function_dictionary = {
    'elite_sample': elite_sample,
    'random_sample': random_sample,
}