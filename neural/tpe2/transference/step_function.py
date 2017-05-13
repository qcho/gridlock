from .transference_function import TransferenceFunction


class StepFunction(TransferenceFunction):

    @classmethod
    def from_json_value(cls, _):
        return StepFunction()

    def apply(self, value):
        if value > 0.5:
            return 1
        else:
            return -1

    def apply_derived(self, value):
        return 1
