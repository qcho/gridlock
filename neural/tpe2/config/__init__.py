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


def validate_config(json_config):
    with open(pkg_resources.resource_filename(__data_pkg__, "config.schema.json"), 'r') as fp:
        validation_json = json.load(fp)
        validate(json_config, validation_json)


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self._parse_config()

    def _parse_config(self):
        with open(pkg_resources.resource_filename(__data_pkg__, self.file_path), 'r') as fp:
            json_object = json.load(fp)
            validate_config(json_object)
            self.epochs = json_object["training_epochs"]
            self.network_path = json_object["input_network"]
            self.input_strategy = json_object["input_strategy"]
            self.print_progress_every = json_object["print_progress_every"]
            self.trained_network_name = json_object["trained_network_name"]
            self.chart_types = json_object["plot"] if 'plot' in json_object else []

    def parse_network(self, path=None) -> Tuple[Optional[Network], Optional[Exception]]:
        try:
            return self._parse(path), None
        except Exception as err:
            return None, err

    def write_network(self, network: Network, file_path=None):
        file_path = file_path if file_path is not None else self.trained_network_name
        with open(pkg_resources.resource_filename(__data_pkg__, file_path + ".json"), 'w') as fh:
            json.dump(network.to_json(), fh, indent=2)

    def _parse(self, path):
        self.network_path = path if path is not None else self.network_path
        with open(pkg_resources.resource_filename(__data_pkg__, self.network_path + ".json"), 'r') as fp:
            json_obj = json.load(fp)
            if 'network' not in json_obj:
                raise ValueError("Missing network configuration parameters")
            validate_network(json_obj["network"])
            return Network.create_from_json(json_obj['network'])

    def __str__(self):
        return "Config:\nnetwork: {}\nepochs: {}\ninput_strategy: {}"\
            .format(self.network_path, self.epochs, self.input_strategy)