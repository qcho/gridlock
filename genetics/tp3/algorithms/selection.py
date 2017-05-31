from itertools import accumulate
from random import sample, random
from ..utils.relative_aptitude import relative_aptitude


CONSTANTS = {
    'randomness': 0.75,
    'tournaments_times': 20,
}


def _between(array, value):
    # Special first case
    if value < array[0]:
        return 0
    # Rest of cases
    for i in range(1, len(array)):
        if array[i - 1] < value < array[i]:
            return i


################################################################################
#                                 Algorithms                                   #
################################################################################
def _accumulated_relative_fitness(population):
    relative_fitness = relative_aptitude(population)
    return list(accumulate(relative_fitness))


def _elite_sample(population, amount: int):
    data = list(reversed(sorted(population, key=lambda x: x.fitness)))
    return data[:amount]


def _random_sample(population, amount: int):
    result = []
    for _ in range(amount):
        result.append(sample(population, 1))

    return result


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


def _tournaments_deterministic(population, amount: int):
    result = []
    for _ in range(CONSTANTS['tournaments_times']):
        small_group = sample(population, amount)
        best = _elite_sample(small_group, 1)
        result.append(best[0])

    return result


def _tournaments_stochastic(population, amount: int):
    result = []
    for _ in range(amount):
        small_group = sample(population, 2)
        best = _elite_sample(small_group, 2)
        r = random()
        if r < CONSTANTS['randomness']:
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


def selection_switcher(type: str):
    switcher = {
        'elite_sample': _elite_sample,
        'random_sample': _random_sample,
        'roulette': _roulette,
        'universal': _universal,
        'boltzmann': _boltzmann,
        'tournaments-deterministic': _tournaments_deterministic,
        'tournaments-stochastic': _tournaments_stochastic,
        'ranking': _ranking,
    }

    return switcher[type]


def set_constants(randomness: float = 0.75, tournaments_times: int = 20):
    CONSTANTS['randomness'] = randomness
    CONSTANTS['tournaments_times'] = tournaments_times
