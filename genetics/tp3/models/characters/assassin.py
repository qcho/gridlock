from . import Character


class Assassin(Character):

    def __init__(self):
        super().__init__()

    def calculate_fitness(self):
        self.fitness = 0.7 * self.attack + 0.3 * self.defense

    def __str__(self):
        return "Fitness: {} \n".format(self.fitness) + super().__str__()


