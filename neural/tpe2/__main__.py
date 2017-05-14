import numpy as np
from pickle import Pickler, Unpickler

from .util import Parser
from .network import Network
from .config import Config
from .transference import HyperbolicTangent
from .transference import LinearFunction
from .view.training import plot_errors
from .view.terrain import plot_terrain

network_filename = "tpe2/network_dumps/net.obj"
should_load_network = False
config = Config("config.json")


def get_generic_network():
    return Network(
        n_inputs=2,
        layer_configuration=[
            (8, HyperbolicTangent(a=1), None),
            (8, HyperbolicTangent(a=1), None),
            (1, LinearFunction(), None)
        ],
        eta=0.04,
        # momentum=0.9
    )


def load_network(filename):
    with open(filename, "rb") as fh:
        old_network = Unpickler(fh).load()

    new_network = get_generic_network()
    for old_layer, new_layer in zip(old_network.layers, new_network.layers):
        old_layer.transference_fn = new_layer.transference_fn

    old_network.eta = new_network.eta
    old_network.momentum = new_network.momentum

    return old_network


def serialize_network_layers(network: Network, filename):
    with open(filename, "wb") as serialized_network:
        Pickler(serialized_network, 2).dump(network)


def mean_squared_error(network, inputs, results):
    predicted_values = np.array(list(map(lambda x: network.predict(x), inputs)))
    errors = (results - predicted_values) ** 2
    return np.sum(errors) * 0.5 / len(errors)


def train_and_print(network, training_inputs, training_results, test_inputs, test_results):
    epochs = 0
    epochs_limit = 5000

    expected_error = 1e-3
    error_limit = (expected_error ** 2) / 2

    training_error = mean_squared_error(network, training_inputs, training_results)
    prev_training_error = None
    test_error = mean_squared_error(network, test_inputs, test_results)
    prev_test_error = None

    training_errors = [training_error]
    test_errors = [test_error]

    pr = True
    prints = 0
    training_step = 1
    print_every = 10

    while test_error > error_limit and epochs < epochs_limit:
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
        else:
            print(epochs)

    print('* Training error: {}'.format(mean_squared_error(network, training_inputs, training_results)))
    print('* Test     error: {}'.format(mean_squared_error(network, test_inputs, test_results)))
    plot_errors(network, training_errors, test_errors)


def maintain_same_weights():
    load = True
    filename = 'tpe2/network_dumps/weights_test.obj'
    parser = Parser()
    training_inputs, training_results = parser.get_half_data()
    test_inputs, test_results = parser.get_half_data(half='last')

    if load:
        network = load_network(filename)
    else:
        network = get_generic_network()
        # serialize_network_layers(network, filename)

    network.print_structure()
    print("---------TRAINING---------")
    train_and_print(network, training_inputs, training_results, test_inputs, test_results)
    serialize_network_layers(network, filename)


def test_network_terrain():
    network = load_network('tpe2/network_dumps/weights_test_2.obj')
    plot_terrain((network, 0.2))


def xor():
    if not should_load_network:
        network, err = config.parse_network()
    else:
        network = load_network('tpe2/network_dumps/xor_net.obj')

    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    results = [[-1], [1], [1], [-1]]

    network.print_structure()
    print("---------TRAINING---------")
    network.train(inputs, results, 10000)
    print("---------TRAINED---------")
    network.print_structure()

    for x_i, result_i in zip(inputs, results):
        print("For {} expecting {} got {}".format(x_i, result_i, network.predict(x_i)))

    serialize_network_layers(network, 'tpe2/network_dumps/xor_net.obj')


if __name__ == "__main__":
    # main()
    # xor()
    # maintain_same_weights()
    #plot_terrain(None)
    test_network_terrain()
