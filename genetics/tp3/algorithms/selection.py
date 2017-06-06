from itertools import accumulate
from random import sample, random
from ..utils.relative_aptitude import relative_aptitude
from math import exp
from numpy import mean


CONSTANTS = {
    'randomness': 0.75,
    'tournaments_group_size': 20,
    't': 100,
    'min_t': 50,
    'cooling_rate': 0.1,
}


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


################################################################################
#                                 Algorithms                                   #
################################################################################
def _elite_sample(population, amount: int):
    data = sorted(population, key=lambda x: x.fitness, reverse=True)
    return data[:amount]


def _random_sample(population, amount: int):
    result = []
    for _ in range(amount):
        result.append(sample(population, 1)[0])

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
    t = CONSTANTS['t']
    values = [exp(x.fitness / t) for x in population]
    boltzmann_mean = mean(values)
    for i in range(0, len(values)):
        values[i] = values[i] / boltzmann_mean
    accumulated = list(accumulate(values))

    result = []
    for _ in range(amount):
        r = random() * len(accumulated)
        i = _between(accumulated, r)
        result.append(population[i])
    return result


def _tournaments_deterministic(population, amount: int):
    result = []
    for _ in range(amount):
        small_group = sample(population, CONSTANTS['tournaments_group_size'])
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
    accumulated_probabilities = list(accumulate(probabilities))

    result = []
    for _ in range(amount):
        r = random()
        i = _between(accumulated_probabilities, r)
        result.append(sort[i])

    return result


def selection_switcher(type: str):
    switcher = {
        'elite-sample': _elite_sample,
        'random-sample': _random_sample,
        'roulette': _roulette,
        'universal': _universal,
        'boltzmann': _boltzmann,
        'tournaments-deterministic': _tournaments_deterministic,
        'tournaments-stochastic': _tournaments_stochastic,
        'ranking': _ranking,
    }

    return switcher[type]


def set_tournament_constants(randomness: float = 0.75, tournaments_group_size: int = 20):
    CONSTANTS['randomness'] = randomness
    CONSTANTS['tournaments_group_size'] = tournaments_group_size


def set_boltzmann_constants(boltzmann_starting_temp, boltzmann_minimum_temp, boltzmann_cooling_step):
    CONSTANTS['t'] = boltzmann_starting_temp
    CONSTANTS['min_t'] = boltzmann_minimum_temp
    CONSTANTS['cooling_rate'] = boltzmann_cooling_step


def set_elite_roulette_constants(ratio: float = 0.25):
    CONSTANTS['elite_roulette_ratio'] = ratio


def mark_new_gen():
    if CONSTANTS['t'] > CONSTANTS['min_t']:
        CONSTANTS['t'] -= CONSTANTS['cooling_rate']
