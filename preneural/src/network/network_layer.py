from transference.transference_function import TransferenceFunction
import numpy as np


class Neuron:
    def __init__(self, n_inputs):
        self.weights = np.zeros(1 + n_inputs)

    def process(self, neuron_input):
        return np.dot(neuron_input, self.weights[1:]) + self.weights[0]

    def __str__(self):
        return "{}-input neuron"


class NetworkLayer:
    def __init__(self, n_neurons: int, n_inputs: int, transference_function: TransferenceFunction):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]
        self.transference_fn = transference_function
        self.deltas = []

    def get_deltas(self):
        return self.deltas

    def set_deltas(self, deltas):
        self.deltas = deltas

    def gen_deltas(self, H):
        pass

    def process(self, neuron_input):
        V = []
        H = []
        for neuron in self.neurons:
            h_i = neuron.process(neuron_input)
            v_i = self.transference_fn.apply(h_i)
            H.append(h_i)
            V.append(v_i)
        return V, H

    def __str__(self):
        return "{}-neuron layer".format(len(self.neurons))