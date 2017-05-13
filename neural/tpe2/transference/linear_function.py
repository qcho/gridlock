from .transference_function import TransferenceFunction


class LinearFunction(TransferenceFunction):
    TYPE = "linear"

    def to_json(self):
        return {
            "type": LinearFunction.TYPE
        }

    @classmethod
    def from_json_value(cls, _):
        return LinearFunction()

    def apply(self, value):
        return value

    def apply_derived(self, value):
        return 1

    def __str__(self):
        return "linear"
