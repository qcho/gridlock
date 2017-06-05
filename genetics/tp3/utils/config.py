import pkg_resources
import json
from ..data import __data_pkg__


class Config:
    def __init__(self, filename):
        self.filename = filename
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
            self.breed_selection_method_1 = json_object['breed_selection_method_1']
            self.breed_selection_method_2 = json_object['breed_selection_method_2']
            self.a_ratio = json_object["A_ratio"]
            self.generation_gap_selection_method_1 = json_object['generation_gap_selection_method_1']
            self.generation_gap_selection_method_2 = json_object['generation_gap_selection_method_2']
            self.b_ratio = json_object["B_ratio"]
            self.child_to_keep_selection_method_1 = json_object['child_to_keep_selection_method_1']
            self.child_to_keep_selection_method_2 = json_object['child_to_keep_selection_method_2']
            self.c_ratio = json_object["C_ratio"]
            self.replacement_method_1 = json_object["replacement_method_1"]
            self.replacement_method_2 = json_object["replacement_method_2"]
            self.d_ratio = json_object["D_ratio"]
            self.crossover_type = json_object['crossover_type']
            self.special_modifiers = {
                'special_strength': json_object['special_modifiers']['special_strength'],
                'special_agility': json_object['special_modifiers']['special_agility'],
                'special_expertise': json_object['special_modifiers']['special_expertise'],
                'special_resistance': json_object['special_modifiers']['special_resistance'],
                'special_life': json_object['special_modifiers']['special_life']
            }
            self.randomness = json_object['tournaments_stochastic_randomness']
            self.tournaments_group_size = json_object['tournaments_group_size']
            self.boltzmann_starting_temp = json_object['boltzmann_starting_temp']
            self.boltzmann_minimum_temp = json_object['boltzmann_minimum_temp']
            self.boltzmann_cooling_step = json_object['boltzmann_cooling_step']
