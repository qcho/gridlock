import numpy as np
from .selection import selection_switcher
import tp3.algorithms.crossover as cross
import random as r
from .selection import mark_new_gen


class Genetic:

    def __init__(self, config, population, items):
        super().__init__()
        replacement_method_dictionary = {
            'method_1': self.replacement_method_1,
            'method_2': self.replacement_method_2,
            'method_3': self.replacement_method_3,
        }
        self.population = population
        self.k = config.child_per_generation
        self.Cc = config.crossover_chance
        self.Mc = config.mutation_chance
        self.N = config.population_size
        self.goal = config.goal_score
        self.A = config.a_ratio
        self.B = config.b_ratio
        self.C = config.c_ratio
        self.generations_limit = config.generations_limit
        self.breed_fn_1 = selection_switcher(config.breed_selection_method_1)
        self.breed_fn_2 = selection_switcher(config.breed_selection_method_2)
        self.generation_fn_1 = selection_switcher(config.generation_gap_selection_method_1)
        self.generation_fn_2 = selection_switcher(config.generation_gap_selection_method_2)
        self.child_selection_fn_1 = selection_switcher(config.child_to_keep_selection_method_1)
        self.child_selection_fn_2 = selection_switcher(config.child_to_keep_selection_method_2)
        self.replacement_type = replacement_method_dictionary[config.replacement_method_1]
        self.crossover_fn = cross.crossover_function_dictionary[config.crossover_type]
        self.children = list()
        self.items = items
        self.print_interval = config.print_interval

    def generate_children(self):
        amount_a = round(self.k*self.A)
        parents = self.breed_fn_1(self.population, amount=amount_a)
        parents = parents + self.breed_fn_2(self.population, amount=(self.k-amount_a))
        r.shuffle(parents)
        for i in range(int(self.k/2)):
            if r.random() < self.Cc:
                [self.children.append(x) for x in self.crossover_fn(parents.pop(), parents.pop())]
            else:
                self.children.append(parents.pop())
                self.children.append(parents.pop())

    def mutate_children(self):
        for child in self.children:
            if r.random() < self.Mc:
                child.height = r.uniform(1.3, 2.0)
            for i in range(len(child.items)):
                if r.random() < self.Mc:
                    child.set_item(r.sample(self.items[i], 1)[0])


    def natural_selection(self):
        generation = 0
        max_fitness = self.goal - 1
        fitness_list = list()
        while max_fitness < self.goal and generation < self.generations_limit:
            self.replacement_type()
            for individual in self.population:
                individual.calculate_fitness()
            generation += 1
            fitness_list.clear()
            for individual in self.population:
                fitness_list.append(individual.fitness)
            max_fitness = np.max(fitness_list)
            if generation % self.print_interval == 0:
                avg_fitness = np.average(fitness_list)
                min_fitness = np.min(fitness_list)
                print("Generation:", generation)
                print("Avg fitness: {}".format(avg_fitness))
                print("Max fitness: {}".format(max_fitness))
                print("Min fitness: {}".format(min_fitness))
            mark_new_gen()
        if self.generations_limit == generation:
            print("Max generation reached...Exiting with a best score of: {}".format(max_fitness))
            individual = list(filter(lambda x: x.fitness == max_fitness, self.population))
            print("The individual stats are: \n{}".format(individual[0]))
        else:
            print("The target score was surpassed in generation: {} with a score of: {}".format(generation, max_fitness))
            individual = list(filter(lambda x: x.fitness == max_fitness, self.population))
            print("The individual stats are: \n{}".format(individual[0]))


    def replacement_method_1(self):
        parents = self.population
        new_pop = list()
        r.shuffle(parents)
        for i in range(int(self.N / 2)):
            if r.random() < self.Cc:
                [new_pop.append(x) for x in self.crossover_fn(parents.pop(), parents.pop())]
            else:
                new_pop.append(parents.pop())
                new_pop.append(parents.pop())
        self.population = new_pop


    def replacement_method_2(self):
        self.generate_children()
        self.mutate_children()
        for child in self.children:
            child.calculate_fitness()
        parents_count = self.N - self.k
        children_count = (self.N - parents_count)
        amount_b = round(parents_count * self.B)
        amount_c = (children_count * self.C)
        new_pop = list()
        [new_pop.append(x) for x in self.generation_fn_1(self.population, amount=amount_b)]
        [new_pop.append(x) for x in self.generation_fn_2(self.population, amount=parents_count - amount_b)]
        [new_pop.append(x) for x in self.child_selection_fn_1(self.children, amount=amount_c)]
        [new_pop.append(x) for x in self.child_selection_fn_2(self.children, amount=children_count - amount_c)]
        self.population =  new_pop
        self.children.clear()


    def replacement_method_3(self):
        self.generate_children()
        self.mutate_children()
        for child in self.children:
            child.calculate_fitness()
        parents_count = self.N - self.k
        children_count = (self.N - parents_count)
        amount_b = round(parents_count * self.B)
        amount_c = (children_count * self.C)
        new_pop = list()
        [new_pop.append(x) for x in self.generation_fn_1(self.population, amount=amount_b)]
        [new_pop.append(x) for x in self.generation_fn_2(self.population, amount=parents_count - amount_b)]
        [new_pop.append(x) for x in self.child_selection_fn_1(self.children + self.population, amount=amount_c)]
        [new_pop.append(x) for x in self.child_selection_fn_2(self.children + self.population, amount=children_count - amount_c)]
        self.population = new_pop
        self.children.clear()

