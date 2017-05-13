import json
from typing import Optional, Tuple

import pkg_resources

from ..network import Network
from ..data import __data_pkg__


class Config:
    def __init__(self, file_path):
        self._file_path = file_path

    def parse_network(self, path=None) -> Tuple[Optional[Network], Optional[IOError]]:
        try:
            return self._parse(path), None
        except IOError as err:
            return None, err

    def _parse(self, path):
        with pkg_resources.resource_stream(__data_pkg__, path if path is not None else self._file_path) as stream:
            json_obj = json.load(stream)
            if 'network' not in json_obj:
                raise ValueError("Missing network configuration parameters")
            return Network.create_from_json(json_obj['network'])

    def write_network(self, network: Network, file_path=None):
        file_path = file_path if file_path is not None else self._file_path
        with open(pkg_resources.resource_filename(__data_pkg__, file_path), 'w') as fh:
            json.dump(network.to_json(), fh, indent=2)
