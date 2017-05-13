from typing import List, Tuple, Optional, Dict
from copy import deepcopy

from .network_layer import NetworkLayer
from ..transference import TransferenceFunction
from ..transference import factory as activation_factory
from ..mean_squared_error import calculate_mean_squared_error


def _init_layers(n_inputs: int,
                 layer_configuration: List[Tuple[int, TransferenceFunction, Optional[List[Dict[str, List[float]]]]]]):
    """
    Initialize all the network layers (input, hidden (if applicable) and output.
    We need to initialize the input layer separately from the rest since it behaves a bit differently
    from the next layers since it is the only layer that doesn't explicitly depend on the previous layer
    configuration.
    :param layer_configuration: A list of tuples consisting of the amount of neurons that the network layer
     contains and the transference function that should be used.
    :return: a list of layers
    """
    n_input_neurons, input_transference_function, weights = layer_configuration[0]
    layers = [NetworkLayer(n_input_neurons, n_inputs, input_transference_function, weights)]  # Input layer
    for i in range(1, len(layer_configuration)):  # Hidden and output layers
        n_neurons, transference_function, weights = layer_configuration[i]
        last_layer_n_neurons = len(layers[-1].neurons)
        layers.append(NetworkLayer(n_neurons, last_layer_n_neurons, transference_function, weights))
    return layers


class Network:
    def __init__(self, n_inputs: int, layer_configuration: List[Tuple[int, TransferenceFunction, Optional[List[float]]]],
                 eta: float, momentum: float = 0.0, adaptive_bold: bool = False, adaptive_annealing: int = 0,
                 adaptive_a: float = 0.001, adaptive_b: float = 0.1):
        self.eta = eta
        self._original_eta = eta
        self.layers = _init_layers(n_inputs, layer_configuration)
        self.momentum = momentum
        self._do_adaptive_bold = adaptive_bold
        self._adaptive_a = adaptive_a
        self._adaptive_b = adaptive_b
        self._do_adaptive_annealing = adaptive_annealing > 0
        self._adaptive_annealing_k = adaptive_annealing


    def print_structure(self):
        print("============ Neural Network ============")
        print("Properties:")
        print("    η: {}".format(self.eta))
        print("    momentum (α): {}".format(self.momentum))
        print("Layers:")
        for i, layer in enumerate(self.layers):
            print("> Layer {}:\n{}".format(i, layer))


    """
    This method trains the network one epoch
    @:param previous_error is used for the eta adaptation
    """
    def train(self, data, expected_output, previous_errors: List = []):
        if self._do_adaptive_bold:
            self._previous_layers = deepcopy(self.layers)

        for x_i, expected_i in zip(data, expected_output):
            self._feed_forward(x_i)
            self._back_propagate(x_i, expected_i)


        if self._do_adaptive_bold:
            self._adapt_eta_bold(data, expected_output, previous_errors)
        if self._do_adaptive_annealing:
            self._adapt_eta_annealing(data, expected_output, previous_errors)


    def predict(self, value):
        return self._feed_forward(value)


    def _feed_forward(self, x_i):
        V_m = x_i
        for layer in self.layers:
            V_m = layer.process(V_m)  # Each neuron saves it's output after this
        return V_m


    def _back_propagate(self, x_i, expected):
        # TODO: Error statistics
        self._update_deltas(expected)  # Each neuron saves it's delta after this
        self._update_errors(x_i)


    def _update_deltas(self, expected):
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            errors = list()
            if i != len(self.layers) - 1:  # Hidden layers
                for j in range(len(layer.neurons)):
                    error = 0.0
                    for neuron in self.layers[i + 1].neurons:
                        error += (neuron.weights[j] * neuron.delta)
                    errors.append(error)
            else:  # Output layer
                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(expected[j] - neuron.output)
            for j in range(len(layer.neurons)):
                neuron = layer.neurons[j]
                d = layer.transference_fn.apply_derived(neuron.output)
                if abs(d) < 0.01:
                    print('Neuron {} saturated in layer {}: derivative {}'.format(j, i, d))
                neuron.delta = errors[j] * d


    def _update_errors(self, data):
        for i in range(len(self.layers)):
            inputs = data if i == 0 else [neuron.output for neuron in self.layers[i - 1].neurons]
            for neuron in self.layers[i].neurons:
                for j in range(len(inputs)):
                    delta_weight = self.eta * neuron.delta * inputs[j]
                    neuron.weights[j] += delta_weight + neuron.last_weight_deltas[j] * self.momentum
                    neuron.last_weight_deltas[j] = delta_weight

                neuron.bias += self.eta * neuron.delta


    @classmethod
    def create_from_json(cls, json_value):
        if 'eta' not in json_value:
            raise ValueError("Missing 'eta' key in network json")
        if 'inputs' not in json_value:
            raise ValueError("Missing 'inputs' key in network json")
        if 'layers' not in json_value:
            raise ValueError("Missing 'layers' key in network json")
        network_configuration = _parse_layers(json_value["layers"])
        return Network(json_value['inputs'], network_configuration, json_value['eta'], json_value['momentum'])


    def _parse_layers(cls, json_value):
        out_val = []
        for i, layer in enumerate(json_value):
            if 'activation_function' not in layer:
                raise ValueError("Missing 'activation_function' key from layers[{}]".format(i))
            activation_function = activation_factory.create_from_json(layer["activation_function"])
            if 'neurons' not in layer or not isinstance(layer['neurons'], int):
                raise ValueError("Missing  or invalid 'neurons' key from layers[{}]".format(i))
            out_val.append((
                layer["neurons"],
                activation_function,
                layer["neuron_weights"] if 'neuron_weights' in layer and isinstance(layer["neuron_weights"], list) else None
            ))
        return out_val


    def _adapt_eta_bold(self, data, expected_output, previous_errors):
        if len(previous_errors) > 0:
            a = 0.005
            b = 0.1

            current_error = calculate_mean_squared_error(self, data, expected_output)

            if (current_error - previous_errors[-1]) > 0:
                self.eta -= self._adaptive_b * self.eta
                # self.eta *= 0.5
                # self.eta *= (1 - self._adaptive_b)

                self.layers = self._previous_layers
            elif (current_error - previous_errors[-1]) < 0:
                self.eta += self._adaptive_a
                # self.eta *= (1 + self._adaptive_a)


    def _adapt_eta_annealing(self, data, expected_output, previous_errors):
        if len(previous_errors) >= self._adaptive_annealing_k:
            self.eta = self._original_eta / (1 + ((len(previous_errors) - 1) / self._adaptive_annealing_k))
