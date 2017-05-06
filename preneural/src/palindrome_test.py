import numpy as np
from typing import List

from gen_bin_dataset import gen_bin_array
from network import Network
from transference.hyperbolic_tangent import HyperbolicTangent
from transference.identity_function import IdentityFunction
from transference.logistic_function import LogisticFunction


def is_palindrome(x: List[int]):
    return np.allclose(x, x[::-1])


def is_bit_par(x: List[int]):
    ones = [one for one in x if x == 1]
    return len(ones) % 2 == 0


def xor_output(x: List[int]):
    return x[0] ^ x[1]


def step_fn(value):
    return True if value > 0.5 else False


if __name__ == '__main__':
    dataset = np.asarray(gen_bin_array(5))
    results = np.asarray([[is_palindrome(x)] for x in dataset])  # Output needs to be an array
    # TODO: This network configuration is incorrect, find out why
    input_layer_length = len(dataset[0])
    network = Network([
        (input_layer_length, HyperbolicTangent()),
        (1, HyperbolicTangent())], eta=0.2)
    network.print_structure()
    print("---------TRAINING---------")
    network.train(dataset, results, 10000)
    print("---------TRAINED---------")
    network.print_structure()
    for x_i, result_i in zip(dataset, results):
        print("For {} expecting {} got {}".format(x_i, result_i, [step_fn(x) for x in network.predict(x_i)]))
