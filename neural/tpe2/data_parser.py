import pkg_resources

def parse():
    """
    Parse a terrain file, skipping the first line. Expects file to exist
    :param data_path: Path to the data file.
    :return: array of [x1, x2, z]
    """
    try:
        with open(pkg_resources.resource_filename(__name__, 'terrain05.data')) as file_handler:
            next(file_handler)
            return [[float(x) for x in line.split(" ") if len(x) > 0] for line in file_handler], None
    except IOError as err:
        return None, err
