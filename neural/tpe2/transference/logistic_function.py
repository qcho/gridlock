import numpy as np
from .transference_function import TransferenceFunction


class LogisticFunction(TransferenceFunction):
    TYPE = "logistic"

    def to_json(self):
        return {
            "type": LogisticFunction.TYPE,
            "a": self.a
        }

    @classmethod
    def from_json_value(cls, json_value):
        out_val = LogisticFunction()
        if 'a' in json_value:
            out_val.a = json_value['a']
        return out_val

    def __init__(self, a: float = 1.7159):
        self.a = a

    def apply(self, value):
        return np.divide(1, 1 + np.exp(-1 * self.a * value))

    def apply_derived(self, value):
        return self.a * self.apply(value) * (1 - self.apply(value))
