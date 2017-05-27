import pkg_resources
from data import __data_pkg__


def parse(file_name):
    try:
        with open(pkg_resources.resource_filename(__data_pkg__, file_name)) as file_handler:
            next(file_handler)
            return [[float(x) for x in line.split("	") if len(x) > 0] for line in file_handler], None
    except IOError as err:
        return None, err
