from typing import List, Optional, Dict

from ..transference import TransferenceFunction
import numpy as np


class Neuron:
    def __init__(self, n_inputs):
        self.bias = -1
        self.output = 0
        self.delta = 0
        self.weights = np.random.rand(n_inputs) - 0.5
        self.last_weight_deltas = np.zeros(n_inputs)


    def process(self, neuron_input):
        return np.dot(neuron_input, self.weights) + self.bias


    def __str__(self):
        return "{}-input neuron"

    def to_json(self):
        return {
            "bias": self.bias,
            "weights": self.weights
        }


class NetworkLayer:
    def __init__(self, n_neurons: int, n_inputs: int, transference_function: TransferenceFunction,
                 weights: Optional[List[Dict[str, List[float]]]]):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]
        self.transference_fn = transference_function
        if weights is not None and len(weights) > 0:
            self._init_weights(weights)

    def _init_weights(self, weights):
        if len(weights) != len(self.neurons):
            raise ValueError("Invalid amount of neuron weights received."
                             "Got {}, expected {}".format(len(weights), len(self.neurons)))
        if len(weights) == 0:
            return
        print(weights)
        for neuron, weights in zip(self.neurons, weights):
            if len(weights["weights"]) != len(neuron.weights):
                raise ValueError("Invalid amount of input weights received."
                                 "Got {}, expected {}".format(len(weights), len(neuron.weights)))
            neuron.weights = weights["weights"]
            neuron.bias = weights["bias"]


    def process(self, neuron_input):
        V = []
        for neuron in self.neurons:
            h_i = neuron.process(neuron_input)
            v_i = self.transference_fn.apply(h_i)
            neuron.output = v_i
            V.append(v_i)
        return V


    def __str__(self):
        out_val = "Properties:\n"
        out_val += "    neurons: {}\n    inputs: {}\n    activation: {}"\
            .format(len(self.neurons), len(self.neurons[0].weights), self.transference_fn)
        out_val += "\nNeurons:"
        for i, neuron in enumerate(self.neurons):
            out_val += "\n- neuron {} has {} weights: " \
                       "{}; bias {}".format(i, len(neuron.weights), neuron.weights, neuron.bias)
        return out_val


    def reduced_description(self):
        return '{} N {}'.format(len(self.neurons), self.transference_fn)

    def to_json(self):
        return {
            "neurons": len(self.neurons),
            "activation_function": self.transference_fn.to_json(),
            "neuron_weights": [neuron.to_json() for neuron in self.neurons]
        }
