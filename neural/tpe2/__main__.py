import numpy as np
from pickle import Pickler, Unpickler
import matplotlib.pyplot as plt

from .data_parser import parse
from .network import Network
from .transference.hyperbolic_tangent import HyperbolicTangent
from .transference.linear_function import LinearFunction
from .transference.step_function import StepFunction


network_filename = "network_dumps/net.obj"
should_load_network = False


def get_generic_network():
    return Network(
        n_inputs=2,
        layer_configuration=[
            (8, HyperbolicTangent(beta=1, a=1)),
            (8, HyperbolicTangent(beta=1, a=1)),
            (1, LinearFunction())
        ],
        eta=0.01,
        # momentum=0.9
    )


def get_parsed_data(to_, from_: int = 0):
    data, err = parse()
    if err is not None:
        print("Error opening file:", err)
        exit(1)
    return zip(*[((x[0], x[1]), [x[2]]) for x in data[from_:to_]])


def load_network(filename):
    with open(filename, "rb") as fh:
        old_network = Unpickler(fh).load()

    new_network = get_generic_network()
    for old_layer, new_layer in zip(old_network.layers, new_network.layers):
        old_layer.transference_fn = new_layer.transference_fn

    return old_network


def serialize_network_layers(network: Network, filename):
    with open(filename, "wb") as serialized_network:
        Pickler(serialized_network, 2).dump(network)


def mean_squared_error(network, inputs, results):
    errors = []

    for x_i, o_i in zip(inputs, results):
        prediction = network.predict(x_i)
        errors.append((o_i[0] - prediction[0])**2)

    ans = np.sum(errors)
    ans /= len(errors)

    return ans


def plot_errors(training_errors, test_errors):
    colors = ['r', 'b']
    markers = ['x', 'o']

    training_size = len(training_errors)
    plt.scatter(range(training_size), training_errors, c=colors[0], marker=markers[0])

    test_size = len(test_errors)
    plt.scatter(range(test_size), test_errors, c=colors[1], marker=markers[1])

    plt.ylabel('Error')
    plt.xlabel('Epochs')
    plt.ylim([0, 0.1])
    plt.show()


def train_and_print(network, training_inputs, training_results, test_inputs, test_results):
    epochs = 0
    epochs_limit = 1000

    expected_error = 1e-8
    error_limit = np.sqrt(2 * expected_error)

    training_error = 9999999
    prev_training_error = None
    test_error = training_error
    prev_test_error = None

    training_errors = []
    test_errors = []

    pr = False
    prints = 0
    training_step = 1
    print_every = 1

    while training_error > error_limit and epochs < epochs_limit:
        network.train(training_inputs, training_results, training_step)
        epochs += training_step

        prev_training_error = training_error
        prev_test_error = test_error
        training_error = mean_squared_error(network, training_inputs, training_results)
        test_error = mean_squared_error(network, test_inputs, test_results)

        training_errors.append(training_error)
        test_errors.append(test_error)

        if pr:
            if prints % print_every == 0:
                str = '[-]' if training_error < prev_training_error else '[+]'
                print('{} Training error: {}'.format(str, training_error))
                str = '[-]' if test_error < prev_test_error else '[+]'
                print('{} Test     error: {}'.format(str, test_error))
                print('    Training {} Test'.format('>' if training_error > test_error else '<'))
                print('    Expected {}'.format(error_limit))
            prints += 1

    print('* Training error: {}'.format(training_error))
    print('* Test     error: {}'.format(test_error))
    plot_errors(training_errors, test_errors)


def maintain_same_weights():
    load = False
    filename = 'network_dumps/weights_test.obj'
    training_inputs, training_results = get_parsed_data(to_=220)
    test_inputs, test_results = get_parsed_data(from_=220, to_=441)

    if load:
        network = load_network(filename)
    else:
        network = get_generic_network()
        serialize_network_layers(network, filename)

    network.print_structure()
    print("---------TRAINING---------")
    train_and_print(network, training_inputs, training_results, test_inputs, test_results)


def main():
    inputs, results = get_parsed_data(20)
    network = get_generic_network() if not should_load_network else load_network(network_filename)

    network.print_structure()
    print("---------TRAINING---------")

    train_and_print(network, inputs, results)

    serialize_network_layers(network, network_filename)


def xor():
    if not should_load_network:
        network = Network(
            n_inputs=2,
            layer_configuration=[
                (2, HyperbolicTangent()),
                (1, StepFunction())
            ],
            eta=0.01
        )
    else:
        network = load_network('network_dumps/xor_net.obj')

    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    results = [[-1], [1], [1], [-1]]

    network.print_structure()
    print("---------TRAINING---------")
    network.train(inputs, results, 10000)
    print("---------TRAINED---------")
    network.print_structure()

    for x_i, result_i in zip(inputs, results):
        print("For {} expecting {} got {}".format(x_i, result_i, network.predict(x_i)))

    serialize_network_layers(network, 'network_dumps/xor_net.obj')


if __name__ == "__main__":
    # main()
    # xor()
    maintain_same_weights()