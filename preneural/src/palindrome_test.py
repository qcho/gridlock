import numpy as np
from typing import List

from gen_bin_dataset import gen_bin_array
from network import Network
from transference.hyperbolic_tangent import HyperbolicTangent


def is_palindrome(x: List[int]):
    return np.allclose(x, x[::1])


def xor_output(x: List[int]):
    return x[0] ^ x[1]

if __name__ == '__main__':
    dataset = np.asarray(gen_bin_array(2))
    results = np.asarray([xor_output(x) for x in dataset])
    # TODO: This network configuration is incorrect, find out why
    input_layer_length = len(dataset[0])
    output_layer_length = 1  # True/False
    network = Network([
        (input_layer_length, HyperbolicTangent()),
        (2, HyperbolicTangent()),
        (output_layer_length, HyperbolicTangent())], eta=0.2)
    network.print_structure()
    # network.train(dataset, results)
