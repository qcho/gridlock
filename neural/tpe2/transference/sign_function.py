import numpy as np
from .transference_function import TransferenceFunction


class SignFunction(TransferenceFunction):
    TYPE = "sign"

    @classmethod
    def from_json_value(cls, _):
        return SignFunction()

    def apply(self, value):
        return np.sign(value)

    def apply_derived(self, value):
        return 1
