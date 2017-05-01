import numpy as np

from transference.transference_function import TransferenceFunction


class LogisticFunction(TransferenceFunction):

    def __init__(self, x0=0, L=1, k=1):
        self.x0 = x0
        self.L = L
        self.k = k

    def apply(self, value):
        return np.divide(self.L, 1 + np.exp(-self.k * (value - self.x0)))

    def apply_inverse(self, value):
        return TransferenceFunction.apply_inverse(value)  # TODO
