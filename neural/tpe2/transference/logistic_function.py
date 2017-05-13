import numpy as np
from ..transference.transference_function import TransferenceFunction


class LogisticFunction(TransferenceFunction):

    def __init__(self, a: float = 1.7159):
        self.a = a

    def apply(self, value):
        return np.divide(1, 1 + np.exp(-1 * self.a * value))

    def apply_derived(self, value):
        return self.a * self.apply(value) * (1 - self.apply(value))
