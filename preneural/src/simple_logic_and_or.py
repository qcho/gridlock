from typing import List
from gen_bin_dataset import gen_bin_array
from perceptron import Perceptron
from numpy import asarray


def compute_result(data: List[int], join_fn) -> int:
    out = data[0]
    for bit in data[1:]:
        out = join_fn(out, bit)
    return out


def or_join(x, y):
    return x | y


def and_join(x, y):
    return x & y

if __name__ == '__main__':
    """Single layer perceptron implementation of logical and/or"""
    dataset = asarray(gen_bin_array(5))
    results = asarray([compute_result(number, or_join) for number in dataset])
    net = Perceptron(negative_class=0, n_iter=1000)
    net.train(dataset, results)
    data_res = list(zip(dataset, results))
    for i in range(len(dataset)):
        subject = data_res[i]  # (number, expected)
        print("For {} expecting {} got {}".format(subject[0], subject[1], net.predict(asarray(subject[0]))))