from typing import List, Tuple, Optional, Dict

from .network_layer import NetworkLayer
from ..transference import TransferenceFunction
from ..transference import factory as activation_factory
from ..util.mean_squared_error import calculate_mean_squared_error


def _parse_layers(json_value):
    out_val = []
    for i, layer in enumerate(json_value):
        activation_function = activation_factory.create_from_json(layer["activation_function"])
        out_val.append((
            layer["neurons"],
            activation_function,
            layer["neuron_weights"] if 'neuron_weights' in layer and isinstance(layer["neuron_weights"], list) else None
        ))
    return out_val


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


class AdaptiveBold:
    def __init__(self, a: float, b: float, k: int):
        self.a = a
        self.b = b
        self.k = k
        self._enabled = True

    @classmethod
    def from_json(cls, json_value):
        return None if json_value is None else AdaptiveBold(json_value["a"], json_value["b"], json_value["k"])

    def to_json(self):
        return {
            "a": self.a,
            "b": self.b,
            "k": self.k
        }

    def delta_eta(self, eta, current_error, previous_errors):
        if len(previous_errors) > 0:
            delta_error = (current_error - previous_errors[-1])
            if delta_error <= 0:
                self._enabled = True
            if not self._enabled:
                return 0
            if delta_error > 0:
                print("reversed! old:{}, delta:{}".format(eta, self.b * eta))
                self._enabled = False
                return -(self.b * eta)
            if len(previous_errors) >= self.k:
                consistent = True
                for error in previous_errors[-self.k:]:
                    consistent = consistent and current_error - error < 0
                if consistent:
                    print("Consistent!!!")
                    return self.a
        return 0

    def __str__(self):
        return "AdaptiveBold(a:{}, b:{}, k:{})".format(self.a, self.b, self.k)


class Network:
    def __init__(self, n_inputs: int,
                 layer_configuration: List[Tuple[int, TransferenceFunction, Optional[List[float]]]],
                 eta: float, momentum: float = 0.0, adaptive_annealing: int = None,
                 adaptive_bold: AdaptiveBold = None, epochs: int=0):
        self.eta = eta
        self._original_eta = eta
        self.layers = _init_layers(n_inputs, layer_configuration)
        self.n_inputs = n_inputs
        self.momentum = momentum
        self._adaptive_bold = adaptive_bold
        self._adaptive_annealing_k = adaptive_annealing
        self._epochs = epochs

    def print_structure(self):
        print("============ Neural Network ============")
        print("Properties:")
        print("    η: {}".format(self.eta))
        print("    momentum (α): {}".format(self.momentum))
        print("    adaptive_bold: {}".format(self._adaptive_bold))
        print("    adaptive_annealing: {}".format(self._adaptive_annealing_k))
        print("    epochs: {}".format(self._epochs))
        print("Layers:")
        for i, layer in enumerate(self.layers):
            print("> Layer {}:\n{}".format(i, layer))

    def train(self, data, expected_output, previous_errors: List=list()):
        """
            This method trains the network one epoch
            @:param previous_error is used for the eta adaptation
        """
        for x_i, expected_i in zip(data, expected_output):
            self._feed_forward(x_i)
            self._back_propagate(x_i, expected_i)

        if self._do_adaptive_bold():
            self._adapt_eta_bold(data, expected_output, previous_errors)
        if self._do_adaptive_annealing():
            self._adapt_eta_annealing(previous_errors)
        self._epochs += 1

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
        network_configuration = _parse_layers(json_value["layers"])
        return Network(
            n_inputs=json_value['inputs'],
            layer_configuration=network_configuration,
            eta=json_value['eta'],
            momentum=json_value['momentum'],
            adaptive_annealing=json_value['adaptive_annealing'] if 'adaptive_annealing' in json_value else None,
            adaptive_bold=AdaptiveBold.from_json(json_value['adaptive_bold']) if 'adaptive_bold' in json_value else None,
            epochs=json_value['epochs'] if 'epochs' in json_value else 0)

    def to_json(self):
        return {
            "network": {
                "epochs": self._epochs,
                "inputs": len(self.layers[0].neurons[0].weights),
                "eta": self.eta,
                "momentum": self.momentum,
                "adaptive_bold": self._adaptive_bold.to_json() if self._adaptive_bold is not None else None,
                "adaptive_annealing": self._adaptive_annealing_k,
                "layers": [layer.to_json() for layer in self.layers]
            }
        }

    def _adapt_eta_bold(self, data, expected_output, previous_errors):
        current_error = calculate_mean_squared_error(self, data, expected_output)
        delta_eta = self._adaptive_bold.delta_eta(self.eta, current_error, previous_errors)
        self.eta += delta_eta

    def _adapt_eta_annealing(self, previous_errors):
        if len(previous_errors) >= self._adaptive_annealing_k:
            self.eta = self._original_eta / (1 + ((len(previous_errors) - 1) / self._adaptive_annealing_k))

    def _do_adaptive_annealing(self):
        return self._adaptive_annealing_k is not None

    def _do_adaptive_bold(self):
        return self._adaptive_bold is not None
