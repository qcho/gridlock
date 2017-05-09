import numpy as np
from ..transference.transference_function import TransferenceFunction

class SignFunction(TransferenceFunction):

    def apply(self, value):
        return np.sign(value)

    def apply_derived(self, value):
        return 1
