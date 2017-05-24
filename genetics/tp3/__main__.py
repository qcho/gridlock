from algorithms.selection import stochastic_sample
from .models.individual import Individual


def generate_individuals(amount):
    return list(map(lambda x: Individual(), list(range(amount))))


def main():
    population = generate_individuals(10)
    print(population)
    stochastic_sample(population, 5, type='universal')


if __name__ == "__main__":
    main()