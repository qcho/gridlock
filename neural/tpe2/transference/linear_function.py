from ..transference.transference_function import TransferenceFunction

class LinearFunction(TransferenceFunction):
    def __init__(self):
        self.beta = 0

    def apply(self, value):
        return value

    def apply_derived(self, value):
        return 1
