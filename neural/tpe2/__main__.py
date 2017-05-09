from pickle import Pickler, Unpickler

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
            (7, HyperbolicTangent()),
            (7, HyperbolicTangent()),
            (1, LinearFunction())
        ],
        eta=0.2,
        momentum=0.9
    )

def get_parsed_data(amount: int):
    data, err = parse()
    if err is not None:
        print("Error opening file:", err)
        exit(1)
    return zip(*[((x[0], x[1]), [x[2]]) for x in data[:amount]])


def load_network(filename):
    with open(filename, "rb") as fh:
        return Unpickler(fh).load()


def serialize_network(network: Network, filename):
    with open(filename, "wb") as serialized_network:
        Pickler(serialized_network, 2).dump(network)


def calculate_error(network, inputs, results, pr: bool = False):
    error_fun = lambda d, x: 0.5 * (d - x) ** 2

    error_sum = 0
    error_amount = 0

    for x_i, result_i in zip(inputs, results):
        prediction = network.predict(x_i)
        if pr:
            print('For {} expected {} got {}'.format(x_i, result_i, prediction))
        error_sum += error_fun(result_i[0], prediction[0])
        error_amount += 1

    return (error_sum, error_amount)

def practice_1(network, inputs, results):
    training_count = 0
    expected_error = 1e-6
    total_error = 9999999
    prints = 0
    training_step = 100
    print_every = 1

    while total_error > expected_error:
        network.train(inputs, results, training_step)
        training_count += training_step

        error_sum, error_amount = calculate_error(network, inputs, results)
        prev_error = total_error
        total_error = error_sum / error_amount

        if prints % print_every == 0:
            str = None
            if total_error < prev_error:
                str = '[-]'
            else:
                str = '[+]'
            print('{} Total error: {}'.format(str, total_error))
        prints += 1

    print('TRAINING FINISHED. IT REQUIRED: {} EPOCHS'.format(training_count))
    network.print_structure()

    print('Complete predictions:')
    inputs, results = get_parsed_data(442)

    error_sum, error_amount = calculate_error(network, inputs, results, True)

    total_error = error_sum / error_amount
    print('Total error: {}'.format(total_error))


def main():
    inputs, results = get_parsed_data(200)
    network = get_generic_network() if not should_load_network else load_network(network_filename)

    network.print_structure()
    print("---------TRAINING---------")

    practice_1(network, inputs, results)

    serialize_network(network, network_filename)


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

    serialize_network(network, 'network_dumps/xor_net.obj')


if __name__ == "__main__":
    main()
    # xor()