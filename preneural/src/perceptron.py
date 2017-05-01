import numpy as np


class Perceptron:
    def __init__(self, eta=0.01, n_iter=10, positive_class=1, negative_class=-1):
        """
        Initialize a perceptron network
        :param eta: learning rate
        :param n_iter: iterations to be performed for the fit function
        """
        self.eta = eta
        self.n_iter = n_iter
        self.p_class = positive_class
        self.n_class = negative_class
        self.weights_ = None
        self.errors_ = None

    def train(self, data, expected):
        """
            Trains the network with a given set of data and expected outputs
        :param data: data matrix
        :param expected: expected values array
        :return: self
        """
        # We need an extra weight to include theta so that:
        # w_0 = -theta and x_0 = 1
        self.weights_ = np.zeros(1 + data.shape[1])
        self.errors_ = []
        for _ in range(self.n_iter):
            errors = 0
            for x_i, expected_i in zip(data, expected):
                w_update = self.eta * (expected_i - self.predict(x_i))
                self.weights_[1:] += w_update * x_i
                # We update w_0 separately since we don't modify the data array to add x_0 value
                self.weights_[0] += w_update
                errors += int(w_update != 0.0)
            self.errors_.append(errors)
        return self

    def _logistic(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def logistic_activation(self, data):
        z = self.net_input(data)
        return self._logistic(z)

    def net_input(self, data):
        """Calculates the network input"""
        # dot(X, w) + x_0 * w_0
        # We also need to do the extra sum since we don't modify X to add for the extra value
        return np.dot(data, self.weights_[1:]) + self.weights_[0]

    def predict(self, data):
        """Predicts to what class the input belongs to"""
        return self.p_class if self.net_input(data) >= 0 else self.n_class
