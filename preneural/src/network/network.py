from typing import List, Tuple

from .network_layer import NetworkLayer
from transference.transference_function import TransferenceFunction


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
    # layers[0].set_as_input()
    for i in range(1, len(layer_configuration)):  # Hidden and output layers
        n_neurons, transference_function = layer_configuration[i]
        last_layer_n_neurons = len(layers[-1].neurons)
        layers.append(NetworkLayer(n_neurons, last_layer_n_neurons, transference_function))
    return layers


# TODO: Add momentum (Clase 5, 25/71)
# TODO: Add some way of initializing a trained network with weights from storage (saving/loading networks)
class Network:
    def __init__(self, layer_configuration: List[Tuple[int, TransferenceFunction]], eta: float):
        self.eta = eta
        self.layers = _init_layers(layer_configuration)

    def print_structure(self):
        for i, layer in enumerate(self.layers):
            print("Layer {}: {}".format(i, layer))

    def train(self, data, expected_output, iterations: int = 1000):
        for _ in range(iterations):
            for x_i, expected_i in zip(data, expected_output):
                V, H = self._feed_forward(x_i)
                self._back_propagate(V, H, expected_i)

    def predict(self, value):
        V, _ = self._feed_forward(value)
        return V[-1]  # TODO: Should this be processed? Since this won't return a real value

    def _feed_forward(self, x_i):
        V = []
        H = []
        layer_input = x_i
        for layer in self.layers:
            V_m, H_m = layer.process(layer_input)
            V.append(V_m)
            H.append(H_m)
            layer_input = V_m
        return V, H

    def _back_propagate(self, V, H, expected):
        # TODO: Error statistics
        self._gen_deltas(V, H, expected)
        for m in range(len(self.layers) - 1, 0, -1):
            self.layers[m].update_weights(self.eta, V[m - 1])

    def _gen_deltas(self, V, H, expected):
        self.layers[-1].set_deltas(self._get_exit_deltas(V, H, expected))
        for m in range(len(self.layers) - 1, 0, -1):
            deltas_m_1 = []
            for i, neuron_m_1 in enumerate(self.layers[m - 1].neurons):
                g_derived = self.layers[m - 1].transference_fn.apply_derived(H[m - 1][i])
                sum_delta_i = 0
                for j, neuron_m in enumerate(self.layers[m].neurons):
                    sum_delta_i += neuron_m.weights[i] * self.layers[m].deltas[j]
                deltas_m_1.append(g_derived * sum_delta_i)
            self.layers[m - 1].set_deltas(deltas_m_1)

    def _get_exit_deltas(self, V, H, expected):
        out_layer = self.layers[-1]
        out_deltas = []
        out_h = H[-1]
        out_v = V[-1]
        for i, _ in enumerate(out_layer.neurons):
            out_deltas.append(out_layer.transference_fn.apply_derived(out_h[i]) * (expected[i] - out_v[i]))
        return out_deltas
