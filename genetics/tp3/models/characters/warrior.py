from .character import Character


class Warrior(Character):

    def __init__(self):
        super().__init__()

    def calculate_fitness(self):
        self.fitness = 0.6 * self.get_attack() + 0.4 * self.get_defense()

    def spawn(self):
        return Warrior()

    def __str__(self):
        return "Fitness: {} ".format(self.fitness) + super().__str__()
