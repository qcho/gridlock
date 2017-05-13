from ..transference.transference_function import TransferenceFunction
import numpy as np


class Neuron:
    def __init__(self, n_inputs):
        self._init_weights(n_inputs)
        self.bias = -1
        self.output = 0
        self.delta = 0

    @property
    def weights(self):
        return self._weights

    def process(self, neuron_input):
        return np.dot(neuron_input, self.weights) + self.bias

    def __str__(self):
        return "{}-input neuron"

    def _init_weights(self, n_inputs):
        self._weights = np.random.rand(n_inputs)
        for i, weight in enumerate(self._weights):
            self._weights[i] = self._weights[i] - 0.5
        self.last_weight_deltas = np.zeros(n_inputs)


class NetworkLayer:
    def __init__(self, n_neurons: int, n_inputs: int, transference_function: TransferenceFunction):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]
        self.transference_fn = transference_function

    def process(self, neuron_input):
        V = []
        for neuron in self.neurons:
            h_i = neuron.process(neuron_input)
            v_i = self.transference_fn.apply(h_i)
            neuron.output = v_i
            V.append(v_i)
        return V

    def __str__(self):
        out_val = "{}-neuron layer:".format(len(self.neurons))
        for i, neuron in enumerate(self.neurons):
            out_val += "\nneuron {} has {} weights: {} and bias {}".format(i, len(neuron.weights), neuron.weights, neuron.bias)
        return out_val

    def reduced_description(self):
        return '{} N {}'.format(len(self.neurons), self.transference_fn)
