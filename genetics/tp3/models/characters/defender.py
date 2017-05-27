from .character import Character


class Defender(Character):

    def __init__(self):
        super().__init__()

    def calculate_fitness(self):
        self.fitness = 0.1 * self.get_attack() + 0.9 * self.get_defense()
