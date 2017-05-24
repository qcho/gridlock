from random import random


class Individual:
    def __init__(self):
        self.fitness = random()


    def __repr__(self):
        return "I: {}".format(self.fitness)
