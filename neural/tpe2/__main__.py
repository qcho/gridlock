import numpy as np
from pickle import Pickler, Unpickler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .data import Parser
from .network import Network
from .config import Config
from .transference import HyperbolicTangent
from .transference import LinearFunction
from .transference import StepFunction

network_filename = "network_dumps/net.obj"
should_load_network = False
config = Config("data/config.json")


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


def plot_errors(network, training_errors, test_errors):
    colors = ['r', 'b']
    markers = ['x', 'o']

    training_size = len(training_errors)
    plt.scatter(range(training_size), training_errors, c=colors[0], marker=markers[0])

    test_size = len(test_errors)
    plt.scatter(range(test_size), test_errors, c=colors[1], marker=markers[1])

    plt.ylabel('Error')
    plt.xlabel('Epochs')
    plt.ylim([0, 0.1])

    hidden_layers = 2
    title = '{} HLayers: {}, eta: {}'.format(hidden_layers, [x.reduced_description() for x in network.layers[:hidden_layers]], network.eta)
    plt.title(title)
    plt.show()


def plot_terrain(X, Y, Z):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(X, Y, Z)
    plt.show()


def network_plot_complete_terrain(network):
    resolution = 0.05
    parser = Parser()
    inputs, outputs = parser.get_all()
    x = [x[0] for x in inputs]
    y = [x[1] for x in inputs]
    min_x = np.floor(min(x))
    max_x = np.ceil(max(x))
    min_y = np.floor(min(y))
    max_y = np.ceil(max(y))
    x = np.arange(min_x, max_x, resolution)
    y = np.arange(min_y, max_y, resolution)
    X, Y = np.meshgrid(x, y)
    Z = []
    for x_i, y_i in zip(X, Y):
        for x_j, y_j in zip(x_i, y_i):
            Z.append(network.predict([x_j, y_j]))
    plot_terrain(X, Y, Z)


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
    filename = 'network_dumps/weights_test.obj'
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


def test_plot_terrain():
    parser = Parser()
    inputs, outputs = parser.get_all()
    X = [x[0] for x in inputs]
    Y = [x[1] for x in inputs]
    Z = [x[0] for x in outputs]
    plot_terrain(X, Y, Z)


def test_network_terrain():
    network = load_network('network_dumps/weights_test.obj')
    network_plot_complete_terrain(network)


def xor():
    if not should_load_network:
        network, err = config.parse_network()
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
    xor()
    # maintain_same_weights()
    # test_plot_terrain()
    # test_network_terrain()
