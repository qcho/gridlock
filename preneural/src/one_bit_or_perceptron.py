from numpy import array
from perceptron import Perceptron

if __name__ == '__main__':
    training_data = [
        (array([0, 0]), 0),
        (array([0, 1]), 1),
        (array([1, 0]), 1),
        (array([1, 1]), 1),
    ]

    data, expected = zip(*training_data)
    # To make it easier to read, we use 0 as the negative class to better show those values that map to 0
    perceptron = Perceptron(negative_class=0)
    perceptron.train(array(data), array(expected))
    print("Errors when training:", perceptron.errors_)

    for x, _ in training_data:
        result = perceptron.predict(x)
        print("{}: {} -> {} (log: {})".format(x, perceptron.net_input(x), perceptron.predict(x),
                                              perceptron.logistic_activation(x)))
