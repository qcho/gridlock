from ..transference import HyperbolicTangent, LogisticFunction, LinearFunction, SignFunction, StepFunction


factory_map = {
    HyperbolicTangent.TYPE: HyperbolicTangent.from_json_value,
    LogisticFunction.TYPE: LogisticFunction.from_json_value,
    LinearFunction.TYPE: LinearFunction.from_json_value,
    SignFunction.TYPE: SignFunction.from_json_value,
    StepFunction.TYPE: StepFunction.from_json_value
}


def create_from_json(json_value):
    if 'type' not in json_value:
        raise ValueError("Missing 'type' key from activation_function json")
    if json_value['type'] not in factory_map.keys():
        raise ValueError("Invalid type: {}".format(json_value['type']))
    return factory_map[json_value['type']](json_value)
