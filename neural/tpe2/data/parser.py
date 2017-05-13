import pkg_resources
from math import floor
from random import sample


class Parser:
    def __init__(self, file_name='terrain05.data'):
        self.file_name = file_name
        self.data, self.err = self._parse()
        self.data_size = len(list(self.data))

    def _parse(self):
        """
        Parse a terrain file, skipping the first line. Expects file to exist
        :return: array of [x1, x2, z]
        """
        try:
            with open(pkg_resources.resource_filename(__name__, self.file_name)) as file_handler:
                next(file_handler)
                return [[float(x) for x in line.split(" ") if len(x) > 0] for line in file_handler], None
        except IOError as err:
            return None, err

    def get_data(self, to_, from_: int = 0):
        return self._zip(self.data[from_:to_])

    def get_all(self):
        return self.get_data(to_=self.data_size)

    def _zip(self, data):
        return zip(*[((x[0], x[1]), [x[2]]) for x in data])

    def get_half_data(self, half = 'first'):
        size = floor(self.data_size / 2)
        return (self.get_data(to_=size) if half == 'first' else self.get_data(from_=size, to_=self.data_size))

    def get_random_data(self, amount):
        return self._zip(sample(self.data, amount))

    def get_alternate(self, amount=None, pair=True):
        to = self.data_size if amount is None else amount * 2
        ans = []
        r = range(0, to, 2) if pair else range(1, to, 2)
        for i in r:
            ans.append(self.data[i])
        return self._zip(ans)
