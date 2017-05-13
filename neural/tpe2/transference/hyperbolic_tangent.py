import numpy as np
from ..transference.transference_function import TransferenceFunction


class HyperbolicTangent(TransferenceFunction):

    def __init__(self, beta: float = 2/3, a: float = 1.7159):
        self.beta = beta
        self.a = a

    def apply(self, value):
        return self.a * np.tanh(self.beta * value)

    def apply_derived(self, value):
        return self.a * self.beta * (1 - np.power(np.tanh(self.beta * value), 2))

    def __str__(self):
        return "tanh (β:{} a:{})".format(round(self.beta, 2), round(self.a, 2))
