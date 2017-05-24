from .character import Character

class Warrior(Character):
    def __init__(self, special_modifiers):
        super().__init__(special_modifiers)


    def calculate_fitness(self):
        self.fitness = 0.6 * self.get_attack() + 0.4 * self.get_defense()
