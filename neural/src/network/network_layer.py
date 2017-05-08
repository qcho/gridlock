from transference.transference_function import TransferenceFunction
import numpy as np


class Neuron:
    def __init__(self, n_inputs):
        self.weights = np.random.rand(n_inputs) - 0.5
        self.bias = 0
        self.output = 0
        self.delta = 0

    def process(self, neuron_input):
        return np.dot(neuron_input, self.weights) + self.bias

    def __str__(self):
        return "{}-input neuron"


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
