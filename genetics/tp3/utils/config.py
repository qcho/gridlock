import pkg_resources
import json
from data import __data_pkg__


class Config:
    def __init__(self, filename):
        self.filename = filename
        self._parse_config()


    def _parse_config(self):
        with open(pkg_resources.resource_filename(__data_pkg__, self.filename), 'r') as fp:
            json_object = json.load(fp)
            self.population_size = json_object['population_size']
            self.special_modifiers = {
                'special_strength': json_object['special_modifiers']['special_strength'],
                'special_agility': json_object['special_modifiers']['special_agility'],
                'special_expertise': json_object['special_modifiers']['special_expertise'],
                'special_resistance': json_object['special_modifiers']['special_resistance'],
                'special_life': json_object['special_modifiers']['special_life']
            }