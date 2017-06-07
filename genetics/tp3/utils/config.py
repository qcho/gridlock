import pkg_resources
import json
from ..data import __data_pkg__


def all_configs():
    return pkg_resources.resource_listdir(__data_pkg__, "configs/")


class Config:
    def __init__(self, filename):
        self.filename = filename
        self._parse_config()

    def _parse_config(self):
        with open(pkg_resources.resource_filename(__data_pkg__, "configs/{}".format(self.filename)), 'r') as fp:
            json_object = json.load(fp)
            self.dataset = json_object['dataset']
            self.population_size = json_object['population_size']
            self.generations_limit = json_object['generations_limit']
            self.mutation_chance = json_object['mutation_chance']
            self.crossover_chance = json_object['crossover_chance']
            self.population_class = json_object['population_class']
            self.child_per_generation = json_object['child_per_generation']
            self.goal_score = json_object['goal_score']
            self.print_interval = json_object['print_every_n_generations']
            self.breed_selection_method_1 = json_object['breed_selection']['method_1']
            self.breed_selection_method_2 = json_object['breed_selection']['method_2']
            self.a_ratio = json_object['breed_selection']['ratio']
            self.generation_gap_selection_method_1 = json_object['generation_gap_selection']['method_1']
            self.generation_gap_selection_method_2 = json_object['generation_gap_selection']['method_2']
            self.b_ratio = json_object['generation_gap_selection']['ratio']
            self.child_to_keep_selection_method_1 = json_object['child_to_keep_selection']['method_1']
            self.child_to_keep_selection_method_2 = json_object['child_to_keep_selection']['method_2']
            self.c_ratio = json_object['child_to_keep_selection']['ratio']
            self.replacement_method = json_object["replacement_method"]
            self.output_path = json_object["output_path"]
            self.output_methods = json_object["outputs"]
            self.crossover_type = json_object['crossover_type']
            self.special_modifiers = {
                'strength': json_object['special_modifiers']['strength'],
                'agility': json_object['special_modifiers']['agility'],
                'expertise': json_object['special_modifiers']['expertise'],
                'resistance': json_object['special_modifiers']['resistance'],
                'life': json_object['special_modifiers']['life']
            }
            self.randomness = json_object['tournaments']['stochastic_randomness']
            self.tournaments_group_size = json_object['tournaments']['group_size']
            self.boltzmann_starting_temp = json_object['boltzmann']['starting_temp']
            self.boltzmann_minimum_temp = json_object['boltzmann']['minimum_temp']
            self.boltzmann_cooling_step = json_object['boltzmann']['cooling_step']

    def to_json(self):
        return {
              "dataset": self.dataset,
              "outputs": self.output_methods,
              "output_path": self.output_path,
              "population_size": self.population_size,
              "generations_limit": self.generations_limit,
              "mutation_chance": self.mutation_chance,
              "crossover_chance": self.crossover_chance,
              "child_per_generation": self.child_per_generation,
              "goal_score": self.goal_score,
              "print_every_n_generations": self.print_interval,
              "population_class": self.population_class,
              "breed_selection": {
                "method_1": self.breed_selection_method_1,
                "method_2": self.breed_selection_method_2,
                "ratio": self.a_ratio
              },
              "generation_gap_selection": {
                "method_1": self.generation_gap_selection_method_1,
                "method_2": self.generation_gap_selection_method_2,
                "ratio": self.b_ratio
              },
              "child_to_keep_selection": {
                "method_1": self.child_to_keep_selection_method_1,
                "method_2": self.child_to_keep_selection_method_2,
                "ratio": self.c_ratio
              },
              "replacement_method": self.replacement_method,
              "crossover_type": self.crossover_type,
              "special_modifiers": self.special_modifiers,
              "tournaments": {
                "group_size": self.tournaments_group_size,
                "stochastic_randomness": self.randomness
              },
              "boltzmann": {
                "starting_temp": self.boltzmann_starting_temp,
                "minimum_temp": self.boltzmann_minimum_temp,
                "cooling_step": self.boltzmann_cooling_step
              }
            }

    def write_json(self):
        with open(pkg_resources.resource_filename(__data_pkg__, "configs/{}".format(self.filename)), 'w') as fh:
            json.dump(self.to_json(), fh, indent=2)
