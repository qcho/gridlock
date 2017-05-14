import numpy as np


def calculate_mean_squared_error(network, inputs, results):
    predicted_values = np.array(list(map(lambda x: network.predict(x), inputs)))
    errors = (results - predicted_values) ** 2
    return np.sum(errors) * 0.5 / len(errors)
