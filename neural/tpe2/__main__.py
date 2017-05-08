from pickle import Pickler, Unpickler

from .data_parser import parse
from .network import Network
from .transference.hyperbolic_tangent import HyperbolicTangent
from .transference.linear_function import LinearFunction

network_filename = "network_dumps/net.obj"
should_load_network = False


def get_generic_network():
    return Network(n_inputs=2, layer_configuration=[
        (7, HyperbolicTangent()),
        (7, HyperbolicTangent()),
        (1, LinearFunction())], eta=0.2)


def get_parsed_data():
    data, err = parse()
    if err is not None:
        print("Error opening file:", err)
        exit(1)
    return zip(*[((x[0], x[1]), [x[2]]) for x in data[:20]])


def load_network():
    with open(network_filename, "rb") as fh:
        return Unpickler(fh).load()


def serialize_network(network: Network):
    with open(network_filename, "wb") as serialized_network:
        Pickler(serialized_network, 2).dump(network)


def main():
    inputs, results = get_parsed_data()
    network = get_generic_network() if not should_load_network else load_network()

    network.print_structure()
    print("---------TRAINING---------")
    network.train(inputs, results, 10000)
    print("---------TRAINED---------")
    network.print_structure()

    for x_i, result_i in zip(inputs, results):
        print("For {} expecting {} got {}".format(x_i, result_i, network.predict(x_i)))

    serialize_network(network)


if __name__ == "__main__":
    main()
