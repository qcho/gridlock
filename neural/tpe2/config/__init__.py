import json
from typing import Optional, Tuple
from jsonschema import validate

import pkg_resources

from ..network import Network
from ..data import __data_pkg__


def validate_network(json_network):
    with open(pkg_resources.resource_filename(__data_pkg__, "network.schema.json"), 'r') as fp:
        validation_json = json.load(fp)
        validate(json_network, validation_json)


class Config:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_network(self, path=None) -> Tuple[Optional[Network], Optional[Exception]]:
        try:
            return self._parse(path), None
        except Exception as err:
            return None, err

    def _parse(self, path):
        self.file_path = path if path is not None else self.file_path
        with open(pkg_resources.resource_filename(__data_pkg__, self.file_path), 'r') as fp:
            json_obj = json.load(fp)
            if 'network' not in json_obj:
                raise ValueError("Missing network configuration parameters")
            validate_network(json_obj["network"])
            return Network.create_from_json(json_obj['network'])

    def write_network(self, network: Network, file_path=None):
        file_path = file_path if file_path is not None else self.file_path
        with open(pkg_resources.resource_filename(__data_pkg__, file_path), 'w') as fh:
            json.dump(network.to_json(), fh, indent=2)
