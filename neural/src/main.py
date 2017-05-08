from data_parser import parse
from network import Network
from transference.hyperbolic_tangent import HyperbolicTangent

if __name__ == '__main__':
    data, err = parse("../data/terrain05.data")
    if err is not None:
        print("Error opening file:", err)
        exit(1)
    inputs, results = zip(*[((x[0], x[1]), [x[2]]) for x in data[:20]])
    network = Network(n_inputs=2, layer_configuration=[
        (7, HyperbolicTangent()),
        (7, HyperbolicTangent()),
        (1, HyperbolicTangent())], eta=0.2)
    network.print_structure()
    print("---------TRAINING---------")
    network.train(inputs, results, 20000)
    print("---------TRAINED---------")
    network.print_structure()
    for x_i, result_i in zip(inputs, results):
        print("For {} expecting {} got {}".format(x_i, result_i, network.predict(x_i)))


