from .character import Character


class Assassin(Character):

    def __init__(self, special_modifiers):
        super().__init__(special_modifiers)

    def calculate_fitness(self):
        self.fitness = 0.7 * self.get_attack() + 0.3 * self.get_defense()

