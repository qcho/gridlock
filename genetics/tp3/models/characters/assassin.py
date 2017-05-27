from . import Character


class Assassin(Character):

    def __init__(self):
        super().__init__()

    def calculate_fitness(self):
        self.fitness = 0.7 * self.get_attack() + 0.3 * self.get_defense()

    def __str__(self):
        return "Fitness: {} ".format(self.fitness) + super().__str__()


