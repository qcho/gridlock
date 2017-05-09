import numpy as np
from ..transference.transference_function import TransferenceFunction

class StepFunction(TransferenceFunction):

    def apply(self, value):
        if value > 0.5:
            return 1
        else:
            return -1

    def apply_derived(self, value):
        return 1
