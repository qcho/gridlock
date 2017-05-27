import numpy as np
import tp3.algorithms.selection as sele
import tp3.algorithms.crossover as cross
import random as r


class Genetic:

    def __init__(self, config, population, items):
        super().__init__()
        self.population = population
        self.k = config.child_per_generation
        self.G = config.generation_gap
        self.Cc = config.crossover_chance
        self.Mc = config.mutation_chance
        self.N = config.population_size
        self.goal = config.goal_score
        self.generations_limit = config.generations_limit
        self.breed_fn = sele.selection_function_dictionary[config.breed_selection_method]
        self.generation_fn = sele.selection_function_dictionary[config.generation_gap_selection_method]
        self.child_selection_fn = sele.selection_function_dictionary[config.child_to_keep_selection_method]
        self.crossover_fn = cross.crossover_function_dictionary[config.crossover_type]
        self.children = list()
        self.items = items
        self.print_interval = config.print_interval

# TODO add interval printing

    def generate_children(self):
        for i in range(0, self.k, 1):
            couple = self.breed_fn(self.population, 2)
            if r.random() < self.Cc:
                [self.children.append(x) for x in self.crossover_fn(couple[0], couple[1], r.randint(0, 6))]
            else:
                [self.children.append(x) for x in couple]

    def mutate_children(self):
        for child in self.children:
            if r.random() < self.Mc:
                child.height = r.uniform(1.3, 2.0)
            print(child)
            for i in range(0, len(child.items)):
                if r.random() < self.Mc:
                    child.set_item(r.sample(self.items[i], 1)[0])

    def select_new_generation(self):
        parents_count = round(self.N * (1-self.G))
        child_count = self.N - parents_count
        new_pop = list()
        [new_pop.append(x) for x in self.generation_fn(self.population, parents_count)]
        [new_pop.append(x) for x in self.child_selection_fn(self.children, child_count)]
        self.population = new_pop
        self.children.clear()

    def natural_selection(self):
        generation = 0
        max_fitness = self.goal - 1
        fitness_list = list()
        while max_fitness < self.goal and generation < self.generations_limit:
            self.generate_children()
            self.mutate_children()
            for child in self.children:
                child.calculate_fitness()
            self.select_new_generation()
            generation += 1
            fitness_list.clear()
            for individual in self.population:
                fitness_list.append(individual.fitness)
            max_fitness = np.max(fitness_list)
            if generation % self.print_interval == 0:
                avg_fitness = np.average(fitness_list)
                min_fitness = np.min(fitness_list)
                print("Avg fitness: {}".format(avg_fitness))
                print("Max fitness: {}".format(max_fitness))
                print("Min fitness: {}".format(min_fitness))
        if self.generations_limit == generation:
            print("Max generation reached...Exiting with a best score of: {}".format(max_fitness))
        else:
            print("The target score was surpassed with a score of: {}".format(max_fitness))
            individual = list(filter(lambda x: x.fitness == max_fitness, self.population))
            print("The individual is: {}".format(individual[0]))


