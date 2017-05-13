from .transference_function import TransferenceFunction


class LinearFunction(TransferenceFunction):
    TYPE = "linear"

    @classmethod
    def from_json_value(cls, _):
        return LinearFunction()

    def apply(self, value):
        return value

    def apply_derived(self, value):
        return 1
