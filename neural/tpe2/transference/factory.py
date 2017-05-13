from transference import *


factory_map = {
    'htan': HyperbolicTangent.from_json_value,
    'logistic': LogisticFunction.from_json_value,
    'linear': LinearFunction.from_json_value,
    'sign': SignFunction.from_json_value,
    'step': StepFunction.from_json_value
}


def create_from_json(json_value):
    if 'type' not in json_value:
        raise ValueError("Missing 'type' key from activation_function json")
    if json_value['type'] not in factory_map.keys():
        raise ValueError("Invalid type: {}".format(json_value['type']))
    return factory_map[json_value['type']](json_value)
