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
        self.generations_limit = config.generations_limit
        self.bsm = sele.selection_function_dictionary[config.breed_selection_method]
        self.gsm = sele.selection_function_dictionary[config.generation_gap_selection_method]
        self.csm = sele.selection_function_dictionary[config.child_to_keep_selection_method]
        self.cof = cross.crossover_function_dictionary[config.crossover_type]
        self.child = list()
        self.items = items

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
        parents_count = round(self.N * self.G)
        child_count = self.N - parents_count
        new_pop = list()
        new_pop.append(self.gsm(self.population, parents_count))
        new_pop.append(self.csm(self.child, child_count))
        self.population = new_pop
        self.child.clear()

# TODO estandarizar parametros de cof y de las func de selection
