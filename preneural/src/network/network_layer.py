from transference.transference_function import TransferenceFunction
import numpy as np


class Neuron:
    def __init__(self, n_inputs):
        self.weights = np.random.rand(n_inputs)
        self.bias = 0
        self.output = 0

    def process(self, neuron_input):
        # self.weights[0] is bias
        return np.dot(neuron_input, self.weights) + self.bias

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
            neuron.output = v_i
            H.append(h_i)
            V.append(v_i)
        return V, H

    def __str__(self):
        out_val = "{}-neuron layer:".format(len(self.neurons))
        for i, neuron in enumerate(self.neurons):
            out_val += "\nneuron {} has {} weights: {} and bias {}".format(i, len(neuron.weights), neuron.weights, neuron.bias)
        return out_val

    def update_weights(self, eta, V_m_1):
        for i, neuron in enumerate(self.neurons):
            for j, _ in enumerate(neuron.weights):
                delta_w = self.deltas[i] * eta
                neuron.weights[j] = delta_w * V_m_1[j]
                neuron.bias += delta_w
