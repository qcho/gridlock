import numpy as np

from transference.transference_function import TransferenceFunction


class LogisticFunction(TransferenceFunction):

    def apply(self, value):
        return np.divide(1, 1 + np.exp(-value))

    def apply_derived(self, value):
        return self.apply(value) * (1 - self.apply(value))
