from typing import Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from tpe2.network import Network
from ..util import Parser


class TerrainPlot:
    @classmethod
    def _basic(cls, X, Y, Z, title=''):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(X, Y, Z, s=2, c=Z, cmap=plt.get_cmap('plasma'))
        plt.title(title)
        plt.show()

    @classmethod
    def _original_data(cls):
        parser = Parser()
        return parser.get()

    @classmethod
    def _get_min_max(cls, array):
        return np.floor(min(array)), np.ceil(max(array))

    @classmethod
    def _get_meshgrid(cls, x, y, resolution):
        min_x, max_x = cls._get_min_max(x)
        min_y, max_y = cls._get_min_max(y)
        x = np.arange(min_x, max_x, resolution)
        y = np.arange(min_y, max_y, resolution)
        return np.meshgrid(x, y)

    @classmethod
    def only_original(cls):
        inputs, outputs = cls._original_data()
        x = [x[0] for x in inputs]
        y = [x[1] for x in inputs]
        z = [x[0] for x in outputs]

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(x, y, z, s=6, c=z, cmap=plt.get_cmap('viridis'))
        plt.show()


    @classmethod
    def only_network(cls, network, resolution: float = 0.05, title=''):
        inputs, outputs = cls._original_data()
        x = [x[0] for x in inputs]
        y = [x[1] for x in inputs]
        X, Y = cls._get_meshgrid(x, y, resolution)
        Z = []
        for x_i, y_i in zip(X, Y):
            for x_j, y_j in zip(x_i, y_i):
                Z.append(network.predict([x_j, y_j]))
        cls._basic(X, Y, Z, title)

    @classmethod
    def network_and_original(cls, network_and_resolution: Optional[Tuple[Network, float]]):
        inputs, outputs = cls._original_data()
        x = [x[0] for x in inputs]
        y = [x[1] for x in inputs]
        z = [x[0] for x in outputs]

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(x, y, z, s=7, c=(0, 0, 1, 1))

        if network_and_resolution is not None:
            network, resolution = network_and_resolution
            X, Y = cls._get_meshgrid(x, y, resolution)
            Z = []
            for x_i, y_i in zip(X, Y):
                for x_j, y_j in zip(x_i, y_i):
                    Z.append(network.predict([x_j, y_j]))
            ax.scatter(X, Y, Z, s=5, c=(0, 1, 0, 0.5))
        plt.show()
