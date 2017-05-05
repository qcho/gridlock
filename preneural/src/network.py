from typing import List, Tuple
import numpy as np

from transference.transference_function import TransferenceFunction


def _net_input(weights, data):
    return np.dot(weights[1:], data) + weights[0]


def _init_layers(layer_configuration: List[Tuple[int, TransferenceFunction]]):
    """
    Initialize all the network layers (input, hidden (if applicable) and output.
    We need to initialize the input layer separately from the rest since it behaves a bit differently
    from the next layers since it is the only layer that doesn't explicitly depend on the previous layer
    configuration.
    :param layer_configuration: A list of tuples consisting of the amount of neurons that the network layer
     contains and the transference function that should be used.
    :return: a list of layers
    """
    n_inputs, input_transference_function = layer_configuration[0]
    layers = [NetworkLayer(n_inputs, n_inputs, input_transference_function)]  # Input layer
    for i in range(1, len(layer_configuration)):  # Hidden and output layers
        n_neurons, transference_function = layer_configuration[i]
        last_layer_n_neurons = len(layers[-1].neurons)
        layers.append(NetworkLayer(n_neurons, last_layer_n_neurons, transference_function))
    return layers


class Neuron:
    def __init__(self, n_inputs):
        self.weights = np.zeros(1 + n_inputs)


class NetworkLayer:
    def __init__(self, n_neurons: int, n_inputs: int, transference_function: TransferenceFunction):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]
        self.transference_function = transference_function


# TODO: Add momentum (Clase 5, 25/71)
# TODO: Add some way of initializing a trained network with weights from storage (saving/loading networks)
class Network:
    def __init__(self, layer_configuration: List[Tuple[int, TransferenceFunction]], eta: float):
        self.eta = eta
        self.layers = _init_layers(layer_configuration)

    def print_structure(self):
        for i in range(len(self.layers)):
            print("Layer {}: {} neurons".format(i, len(self.layers[i].neurons)))

    def train(self, data, expected_output, iterations: int = 1000):
        for _ in range(iterations):
            for x_i, expected_i in zip(data, expected_output):
                V, H = self._feed_forward(x_i)
                self._back_propagate(V, H, expected_i)

    def predict(self, value):
        V, _ = self._feed_forward(value)
        return V[-1]  # TODO: Should this be processed? Since this won't return a real value

    def _feed_forward(self, x_i):
        V = [x_i]
        H = []
        for m in range(1, self.n_layers):
            for i in range(len(V[-1])):  # Always use the amount of neurons of the last layer
                H.append(_net_input(self.layer_weights[m], V[m - 1]))
                V.append(self.transference_fn.apply(H[-1]))  # Getting last element from H
        return V, H

    def _back_propagate(self, V, H, expected):
        # TODO: Error statistics
        deltas = [self.transference_fn.apply_inverse(H[-1]) * (expected - V[-1])]
        # Since python is 0-based, we shift by 1 upper and lower bounds
        for m in range(self.n_layers - 1, 0, -1):
            # deltas[0] is always "delta_m" since it is the current delta
            g_inverse = self.transference_fn.apply_inverse(H[m - 1])
            delta = g_inverse * np.dot(self.layer_weights[m][1:], deltas[0])
            deltas.insert(0, delta)
        for i in range(self.n_layers):
            delta_w = self.eta * deltas[i]
            self.layer_weights[i][1:] += self.eta * delta_w * V[i]
            self.layer_weights[i][0] += delta_w
