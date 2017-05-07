from transference.transference_function import TransferenceFunction


class IdentityFunction(TransferenceFunction):
    def apply(self, value):
        return value

    def apply_derived(self, value):
        TransferenceFunction.apply_derived(self, value)
