from typing import Tuple, Optional, List, Callable, Any

import pkg_resources

from ..data import __data_pkg__
from ..util.data_filters import half as filter_half, z_ordered


def _zip(data):
    return zip(*[((x[0], x[1]), [x[2]]) for x in data])


def _parse(file_name) -> Tuple[Optional[List[List[float]]], Optional[IOError]]:
    """
    Parse a terrain file, skipping the first line. Expects file to exist
    :return: array of [x1, x2, z]
    """
    try:
        with open(pkg_resources.resource_filename(__data_pkg__, file_name)) as file_handler:
            next(file_handler)
            return [[float(x) for x in line.split(" ") if len(x) > 0] for line in file_handler], None
    except IOError as err:
        return None, err


input_strategies = {
    "all": (None, None),
    "first_half": (filter_half(first_half=True), None),
    "second_half": (filter_half(first_half=False), None),
    "z_ascending": (None, z_ordered(ascending=True)),
    "z_descending": (None, z_ordered(ascending=False))
}


class Parser:
    def __init__(self, file_name='terrain05.data'):
        self.file_name = file_name
        self.data, self.err = _parse(file_name)
        self.data_size = len(list(self.data))

    def get_with_strategy(self, strategy):
        filter_fn, order_fn = input_strategies[strategy]
        return self.get(filter_fn=filter_fn, order_fn=order_fn)

    def get(self, filter_fn = None, order_fn = None):
        data = self.data
        if filter_fn is not None:
            data = filter_fn(data)
        if order_fn is not None:
            data = order_fn(data)
        return _zip(data)
