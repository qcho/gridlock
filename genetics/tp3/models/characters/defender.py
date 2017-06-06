from . import Character


class Defender(Character):

    def __init__(self):
        super().__init__()

    def _calculate_fitness(self):
        return 0.1 * self.attack + 0.9 * self.defense

    def __str__(self):
        return "Fitness: {} \n".format(self.fitness) + super().__str__()

