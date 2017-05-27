import pkg_resources
from ..models.items import Item, ItemType
from ..data import __data_pkg__


def parse(file_name, item_type: ItemType):
    data, err = _parse(file_name)
    if err is not None:
        return None, err
    return list(map(lambda x: Item(int(x[0]), x[1], x[2], x[3], x[4], x[5], item_type), data)), err


def _parse(file_name):
    try:
        with open(pkg_resources.resource_filename(__data_pkg__, file_name)) as file_handler:
            next(file_handler)
            return [[float(x) for x in line.split("	") if len(x) > 0] for line in file_handler], None
    except IOError as err:
        return None, err
