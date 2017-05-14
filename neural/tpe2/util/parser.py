from typing import Tuple, Optional, List, Callable, Any

import pkg_resources

from ..data import __data_pkg__


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


class Parser:
    def __init__(self, file_name='terrain05.data'):
        self.file_name = file_name
        self.data, self.err = _parse(file_name)
        self.data_size = len(list(self.data))

    def get(self, filter_fn: Optional[Callable[[List[Any]], Any]]=None,
            order_fn: Optional[Callable[[List[Any]], Any]]=None):
        data = self.data
        if filter_fn is not None:
            data = filter_fn(data)
        if order_fn is not None:
            data = order_fn(data)
        return _zip(data)
