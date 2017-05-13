import json
from typing import Optional, Tuple

import pkg_resources

from ..network import Network
from ..data import __data_pkg__


class Config:
    def __init__(self, file_path):
        self._file_path = file_path

    def parse_network(self) -> Tuple[Optional[Network], Optional[IOError]]:
        try:
            return self._parse(), None
        except IOError as err:
            return None, err

    def _parse(self):
        with pkg_resources.resource_stream(__data_pkg__, self._file_path) as stream:
            json_obj = json.load(stream)
            if 'network' not in json_obj:
                raise ValueError("Missing network configuration parameters")
            return Network.create_from_json(json_obj['network'])

    def write_network(self, network: Network):
        with open(self._file_path, 'r') as fh:
            json.dump(network.to_json(), fh)
