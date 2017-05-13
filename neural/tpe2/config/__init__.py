import json
from typing import Optional, Tuple

from network import Network


class Config:
    def __init__(self, file_path):
        self._file_path = file_path

    def parse_network(self) -> Tuple[Optional[Network], Optional[IOError]]:
        try:
            return self._parse(), None
        except IOError as err:
            return None, err

    def _parse(self):
        with open(self._file_path, 'r') as fh:
            json_obj = json.load(fh)
            if 'network' not in json_obj:
                raise ValueError("Missing network configuration parameters")
            return Network.create_from_json(json_obj['network'])

    def write_network(self, network: Network):
        with open(self._file_path, 'r') as fh:
            json.dump(network.to_json(), fh)
