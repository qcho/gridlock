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


def _tournaments_deterministic(population, amount: int, times: int):
    result = []
    for _ in range(times):
        small_group = sample(population, amount)
        best = elite_sample(small_group, 1)
        result.append(best[0])

    return result


def _tournaments_stochastic(population, amount: int, times: int, randomness: float = 0.75):
    result = []
    for _ in range(times):
        small_group = sample(population, 2)
        best = elite_sample(small_group, 2)
        r = random()
        if r < randomness:
            result.append(best[0])
        else:
            result.append(best[1])

    return result


def _ranking(population, amount: int):
    sort = list(reversed(sorted(population, key=lambda x: x.fitness)))
    N = len(sort)
    probabilities = []
    for i in range(N):
        probabilities.append((N - i) / (N*(N+1)/2))
    accumulated_probabilities =list(accumulate(probabilities))

    result = []
    for _ in range(amount):
        r = random()
        i = _between(accumulated_probabilities, r)
        result.append(sort[i])

    return result


def stochastic_sample(population, amount: int, type: str, times: int = 1, randomness: float = 0.75):
    switcher = {
        'roulette': _roulette,
        'universal': _universal,
        'boltzmann': _boltzmann,
        'tournaments-deterministic': _tournaments_deterministic,
        'tournaments-stochastic': _tournaments_stochastic,
        'ranking': _ranking
    }
    func = switcher[type]
    return func(population, amount=amount, times=times, randomness=randomness)

#TODO completar el diccionario
selection_function_dictionary = {
    'elite_sample': elite_sample,
    'random_sample': random_sample,
}