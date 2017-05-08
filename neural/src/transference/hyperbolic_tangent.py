import numpy as np

from transference.transference_function import TransferenceFunction


class HyperbolicTangent(TransferenceFunction):

    def __init__(self, beta: float = 0.5):
        self.beta = beta

    def apply(self, value):
        return np.tanh(self.beta * value)

    def apply_derived(self, value):
        return self.beta * (1 - np.power(self.apply(value), 2))
