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
                self._feed_forward(x_i)
                self._back_propagate(x_i, expected_i)

    def predict(self, value):
        return self._feed_forward(value)

    def _feed_forward(self, x_i):
        V_m = x_i
        for layer in self.layers:
            V_m = layer.process(V_m)
        return V_m

    def _back_propagate(self, x_i, expected):
        # TODO: Error statistics
        self._update_deltas(expected)
        self._update_errors(x_i)

    def _update_deltas(self, expected):
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            errors = list()
            if i != len(self.layers) - 1:  # Hidden layers
                for j in range(len(layer.neurons)):
                    error = 0.0
                    for neuron in self.layers[i + 1].neurons:
                        error += neuron.weights[j] * neuron.delta
                    errors.append(error)
            else:  # Output layer
                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(expected[j] - neuron.output)
            for j in range(len(layer.neurons)):
                neuron = layer.neurons[j]
                neuron.delta = errors[j] * layer.transference_fn.apply_derived(neuron.output)

    def _update_errors(self, data):
        for i in range(len(self.layers)):
            inputs = data if i == 0 else [neuron.output for neuron in self.layers[i - 1].neurons]
            for neuron in self.layers[i].neurons:
                for j in range(len(inputs)):
                    neuron.weights[j] += self.eta * neuron.delta * inputs[j]
                neuron.bias += self.eta * neuron.delta
