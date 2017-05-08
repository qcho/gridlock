from ..transference.transference_function import TransferenceFunction

class LinearFunction(TransferenceFunction):
    def apply(self, value):
        return value

    def apply_derived(self, value):
        return 1
