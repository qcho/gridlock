def parse(data_path):
    """
    Parse a terrain file, skipping the first line. Expects file to exist
    :param data_path: Path to the data file.
    :return: array of [x1, x2, z]
    """
    try:
        with open(data_path) as file_handler:
            next(file_handler)
            return [[float(x) for x in line.split(" ") if len(x) > 0] for line in file_handler], None
    except IOError as err:
        return None, err
