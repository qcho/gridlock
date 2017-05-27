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
        self.bsm = sele.selection_function_dictionary[config.breed_selection_method]
        self.gsm = sele.selection_function_dictionary[config.generation_gap_selection_method]
        self.csm = sele.selection_function_dictionary[config.child_to_keep_selection_method]
        self.cof = cross.crossover_function_dictionary[config.crossover_type]
        self.child = list()
        self.items = items
        self.print_interval = config.print_interval

# TODO add interval printing

    def generate_children(self):
        for i in range(0, self.k, 1):
            couple = self.csm(self.population, 2)
            if r.random() < self.Cc:
                self.child.append(self.cof(couple[0], couple[1], self.items))
            else:
                self.child.append(couple)

    def mutate_children(self):
        for child in self.child:
            if r.random() < self.Mc:
                child.height = r.uniform(1.3, 2.0)
            for i in range(0, child.items.length):
                if r.random() < self.Mc:
                    child.add_item(r.sample(self.items[i], 1)[0])

    def select_new_generation(self):
        parents_count = round(self.N * (1-self.G))
        child_count = self.N - parents_count
        new_pop = list()
        new_pop.append(self.gsm(self.population, parents_count))
        new_pop.append(self.csm(self.child, child_count))
        self.population = new_pop
        self.child.clear()

    def natural_selection(self):
        generation = 0
        max_fitness = self.goal - 1
        fitness_list = list()
        while max_fitness < self.goal and generation < self.generations_limit:
            self.generate_children()
            self.mutate_children()
            for child in self.child:
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
            individual = filter(lambda x: x.fitness == max_fitness, self.population)
            print("The individual is: {}", individual[0])


