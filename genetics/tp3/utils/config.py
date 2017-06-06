import pkg_resources
import json
from ..data import __data_pkg__


class Config:
    def __init__(self, filename):
        self.filename = "configs/{}".format(filename)
        self._parse_config()

    def _parse_config(self):
        with open(pkg_resources.resource_filename(__data_pkg__, self.filename), 'r') as fp:
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
