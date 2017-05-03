from typing import List
import numpy as np

from transference.transference_function import TransferenceFunction


def _net_input(weights, data):
    return np.dot(weights[1:], data) + weights[0]

# TODO: Add momentum (Clase 5, 25/71)

class Network:
    def __init__(self, layer_configuration: List[int], transference_fn: TransferenceFunction, eta: float):
        self.layer_weights = [np.zeros(1 + layer_info) for layer_info in layer_configuration]
        self.n_layers = len(self.layer_weights)
        self.transference_fn = transference_fn
        self.eta = eta

    def train(self, data, expected_output, iterations: int = 1000):
        for _ in range(iterations):
            for x_i, expected_i in zip(data, expected_output):
                V, H = self._feed_forward(x_i)
                self._back_propagate(V, H, expected_i)

    def predict(self, value):
        V, _ = self._feed_forward(value)
        return V[-1]  # TODO: Should this be processed? Since this won't return a real value

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

    def _feed_forward(self, x_i):
        V = [x_i]
        H = []
        for m in range(1, self.n_layers):
            H.append(_net_input(self.layer_weights[m], V[m - 1]))
            V.append(self.transference_fn.apply(H[-1]))  # Getting last element from H
        return V, H
