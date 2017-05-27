from .character import Character


class Archer(Character):

    def __init__(self, special_modifiers):
        super().__init__(special_modifiers)

    def calculate_fitness(self):
        self.fitness = 0.9 * self.get_attack() + 0.1 * self.get_defense()

