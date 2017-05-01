from typing import List

from transference.transference_function import TransferenceFunction


class Network:
    def __init__(self, layer_configuration: List[int], transference_fn: TransferenceFunction):
        self.layer_configuration = layer_configuration
        self.n_layers = len(layer_configuration)
        self.transference_fn = transference_fn
