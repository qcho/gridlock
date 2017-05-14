from typing import Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from tpe2.network import Network
from ..util import Parser


def plot_terrain(network_and_resolution: Optional[Tuple[Network, float]]):
    parser = Parser()
    inputs, outputs = parser.get_all()
    x = [x[0] for x in inputs]
    y = [x[1] for x in inputs]
    z = [x[0] for x in outputs]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, s=2, c=(0, 0, 1, 1))

    if network_and_resolution is not None:
        network, resolution = network_and_resolution
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
        ax.scatter(X, Y, Z, s=5, c=(0, 1, 0, 0.5))
    plt.show()