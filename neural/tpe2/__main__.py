from pickle import Unpickler
from time import time

import numpy as np

from .config import Config
from .network import Network
from .transference import HyperbolicTangent
from .transference import LinearFunction
from .util import Parser
from .util.data_filters import half as filter_half
from .util.data_filters import skipping
from .util.data_filters import z_ordered
from .util.mean_squared_error import calculate_mean_squared_error
from .view import Charts
from .view import TerrainPlot

network_filename = "tpe2/network_dumps/net.obj"
should_load_network = False
config = Config("config.json")
adaptive_k = 100


def get_generic_network():
    return Network(
        n_inputs=2,
        layer_configuration=[
            (8, HyperbolicTangent(a=1), None),
            (8, HyperbolicTangent(a=1), None),
            (1, LinearFunction(), None)
        ],
        eta=0.25,
        # momentum=0.9,
        # adaptive_bold=AdaptativeBold(a=0.01, b=0.1, k=1),
        # adaptive_annealing=adaptive_k
    )


def load_network(filename) -> Network:
    """Deprecated: Do not use"""
    with open(filename, "rb") as fh:
        old_network = Unpickler(fh).load()

    new_network = get_generic_network()
    for old_layer, new_layer in zip(old_network.layers, new_network.layers):
        old_layer.transference_fn = new_layer.transference_fn

    if adaptive_k is None:
        old_network.eta = new_network.eta
        old_network.adaptive_k = 0
    else:
        old_network.adaptive_k = adaptive_k

    old_network.momentum = new_network.momentum

    return old_network


def ordered_alternate_training_and_test_data():
    parser = Parser()
    training_inputs, training_results = parser.get(filter_fn=skipping(amount=1, offset=0), order_fn=z_ordered(ascending=True))
    test_inputs, test_results = parser.get(filter_fn=skipping(amount=1, offset=1), order_fn=z_ordered(ascending=True))
    return training_inputs, training_results, test_inputs, test_results


def train_and_print(network, training_inputs, training_results, test_inputs, test_results):
    epochs = 0
    epochs_limit = config.epochs

    expected_error = 1e-3
    error_limit = (expected_error ** 2) / 2

    training_error = calculate_mean_squared_error(network, training_inputs, training_results)
    test_error = calculate_mean_squared_error(network, test_inputs, test_results)

    training_errors = [training_error]
    test_errors = [test_error]

    pr = True
    prints = 0
    print_every = config.print_progress_every

    while test_error > error_limit and epochs < epochs_limit:
        network.train(training_inputs, training_results, test_errors)

        prev_training_error = training_error
        prev_test_error = test_error
        training_error = calculate_mean_squared_error(network, training_inputs, training_results)
        test_error = calculate_mean_squared_error(network, test_inputs, test_results)

        training_errors.append(training_error)
        test_errors.append(test_error)

        if pr:
            if prints % print_every == 0:
                print("Epoch: {}".format(epochs))
                string = '[-]' if training_error < prev_training_error else '[+]'
                print('{} Training error: {}'.format(string, training_error))
                string = '[-]' if test_error < prev_test_error else '[+]'
                print('{} Test     error: {}'.format(string, test_error))
                print('    Training {} Test'.format('>' if training_error > test_error else '<'))
                print('    Expected {}'.format(error_limit))
                print('    eta {}'.format(network.eta))
                print('    momentum {}'.format(network.momentum))
            prints += 1
        else:
            print(epochs)
        # config.write_network(network, "{}_{}".format(config.file_path, epochs))
        if (network.momentum != 0 and network.momentum != 0.99) and (epochs % 50) == 0:
            network.momentum += 0.005
        epochs += 1

    print('* Training error: {}'.format(calculate_mean_squared_error(network, training_inputs, training_results)))
    print('* Test     error: {}'.format(calculate_mean_squared_error(network, test_inputs, test_results)))
    Charts.training_errors(network, training_errors, test_errors)
    TerrainPlot.only_network(network)


def maintain_same_weights():
    # training_inputs, training_results, test_inputs, test_results = ordered_alternate_training_and_test_data()
    print("Starting training with the following config:")
    print(config)
    training_inputs, training_results = Parser().get_with_strategy(config.input_strategy)
    test_inputs, test_results = Parser().get()

    network, err = config.parse_network()
    if err is not None:
        print("Error: ", err)
        raise err

    network.print_structure()
    print("---------TRAINING---------")
    train_and_print(network, training_inputs, training_results, test_inputs, test_results)
    print(network.print_structure())
    config.write_network(network)


def test_plot_terrain(inputs, outputs):
    x = [x[0] for x in inputs]
    y = [x[1] for x in inputs]
    z = [x[0] for x in outputs]
    TerrainPlot._basic(x, y, z)


def test_network_terrain():
    network, err = config.parse_network("weights_test.json")
    # print(network.print_structure())
    TerrainPlot.only_network(network)


def architecture_selection():
    parser = Parser()
    training_inputs, training_results = parser.get(filter_fn=filter_half())
    test_inputs, test_results = parser.get(filter_fn=filter_half(False))

    min_training_errors = []
    min_test_errors = []
    training_times = []

    etas = [0.5, 0.4, 0.3, 0.2, 0.1, 0.05]

    neurons = 10
    print('Neurons per layer {}'.format(neurons))
    for eta in etas:
        network = Network(
            n_inputs=2,
            layer_configuration=[
                (neurons, HyperbolicTangent(a=1), None),
                (neurons, HyperbolicTangent(a=1), None),
                (neurons, HyperbolicTangent(a=1), None),
                # (7, LogisticFunction(), None),
                # (7, LogisticFunction(), None),
                (1, LinearFunction(), None)
            ],
            eta=eta
        )

        epochs = 0
        epochs_limit = 1500

        expected_error = 0
        error_limit = (expected_error ** 2) / 2

        training_error = calculate_mean_squared_error(network, training_inputs, training_results)
        test_error = calculate_mean_squared_error(network, test_inputs, test_results)

        training_errors = [training_error]
        test_errors = [test_error]

        training_time = 0

        while test_error > error_limit and epochs < epochs_limit:
            st = time()
            network.train(training_inputs, training_results, test_errors)
            training_time += time() - st
            epochs += 1

            training_error = calculate_mean_squared_error(network, training_inputs, training_results)
            test_error = calculate_mean_squared_error(network, test_inputs, test_results)

            training_errors.append(training_error)
            test_errors.append(test_error)

        min_training_errors.append(min(training_errors))
        min_test_errors.append(min(test_errors))
        training_times.append(training_time)

        print('eta: {}'.format(eta))
        print('Avg time: {}'.format(round(np.average(training_times), 2)))
        print('Minimum training error: {}'.format(round(min(min_training_errors), 8)))
        print('Minimum test error: {}'.format(round(min(min_test_errors), 8)))


def xor():
    network, err = config.parse_network()
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    results = [[-1], [1], [1], [-1]]

    network.print_structure()
    print("---------TRAINING---------")
    for _ in range(1000):
        network.train(inputs, results)
    print("---------TRAINED---------")
    network.print_structure()

    for x_i, result_i in zip(inputs, results):
        print("For {} expecting {} got {}".format(x_i, result_i, network.predict(x_i)))

    config.write_network(network)


def main():
    # xor()
    maintain_same_weights()
    # inputs, outputs = Parser().get()
    # test_plot_terrain(inputs, outputs)
    # test_network_terrain()

if __name__ == "__main__":
    main()
