import json
import os.path
from typing import Tuple, Dict

import neural_network
from game_config import Direction
from neural_network import *
from vision import VisionLine, get_parameters_in_nn_input_form_2d


class TrainingExample:
    def __init__(self, board: np.ndarray, current_direction: Direction, vision_lines: List[VisionLine], predictions: List[float]):
        self.board = board
        self.current_direction = current_direction
        self.vision_lines = vision_lines
        self.predictions = predictions


def read_training_data_and_train(network: NeuralNetwork, file_path: str) -> None:
    x, y = read_training_data_json(file_path)

    # example for points
    # x is (10000,2) 10000 lines, 2 columns ; 10000 examples each with x coord and y coord
    # when using a single example x_test from x, x_test is (2,)
    # resizing can be done for the whole training data resize(10000,2,1)
    # or for just one example resize(2,1)

    input_neuron_count = network.get_dense_layers()[0].input_size
    output_neuron_count = network.get_dense_layers()[-1].output_size

    x = np.reshape(x, (len(x), input_neuron_count, 1))
    y = np.reshape(y, (len(y), output_neuron_count, 1))

    network.train(mse, mse_prime, x, y, 0.5)

    # for x_test, y_test in zip(x, y):
    #     output = network.feed_forward(x_test)
    #     output_index = list(output).index(max(list(output)))
    #     target_index = list(y_test).index(max(list(y_test)))
    #     print(f"target = {target_index}, output = {output_index}")
    #     print("============================================")


def write_examples_to_json_4d(examples: List[TrainingExample], output_file_location: str) -> None:
    dictionary_list: List[Dict] = []

    for example in examples:
        up = example.predictions[0]
        down = example.predictions[1]
        left = example.predictions[2]
        right = example.predictions[3]

        vision_lines = []
        for line in example.vision_lines:
            line_dict = {
                "direction": line.direction.name,
                "wall_coord": line.wall_coord,
                "wall_distance": line.wall_distance,
                "apple_coord": line.apple_coord,
                "apple_distance": line.apple_distance,
                "segment_coord": line.segment_coord,
                "segment_distance": line.segment_distance
            }
            vision_lines.append(line_dict)

        example_dictionary: Dict = {
            "current_direction": example.current_direction.name,
            "vision_lines": vision_lines,
            "up": up,
            "down": down,
            "left": left,
            "right": right
        }
        dictionary_list.append(example_dictionary)

    output_file = open(output_file_location, "w")
    json.dump(dictionary_list, output_file)
    output_file.close()


def read_training_data_json(file_location) -> Tuple[List, List]:
    json_file = open(file_location, "r")
    json_object = json.load(json_file)

    x = []
    y = []
    if json_object:
        for example in json_object:
            real_direction = Direction[example["current_direction"]]

            vision_lines = []
            for line in example["vision_lines"]:
                line = VisionLine(line["wall_coord"], line["wall_distance"], line["apple_coord"], line["apple_distance"], line["segment_coord"], line["segment_distance"], Direction[line["direction"]])
                vision_lines.append(line)

            x.append(get_parameters_in_nn_input_form_2d(vision_lines, real_direction))

            outputs = [example["up"], example["down"], example["left"], example["right"]]
            y.append(outputs)

    json_file.close()

    return x, y


def save_neural_network_to_json(data_to_save: Dict, network: NeuralNetwork, path: str) -> None:
    network_list = []
    for i, layer in enumerate(network.layers):
        if type(layer) is Activation:
            layer_dict = {
                "layer": "activation",
                "activation": layer.activation.__name__,
                "activation_prime": layer.activation_prime.__name__
            }
        else:
            layer_dict = {
                "layer": "dense",
                "input_size": layer.input_size,
                "output_size": layer.output_size,
                "weights": layer.weights.tolist(),
                "bias": layer.bias.tolist()
            }
        network_list.append(layer_dict)

    option_dict = {"generation": data_to_save["generation"],
                   "board_size": data_to_save["initial_board_size"],
                   "snake_size": data_to_save["initial_snake_size"],
                   "input_direction_count": data_to_save["input_direction_count"],
                   "apple_return_type": data_to_save["apple_return_type"],
                   "segment_return_type": data_to_save["segment_return_type"],
                   "distance_function": data_to_save["distance_function"],
                   "network": network_list}

    path_tokens = path.split("/")
    path_tokens = path_tokens[:-1]
    real_path: str = ""
    for token in path_tokens:
        real_path += token + "/"

    if not os.path.exists(real_path):
        os.makedirs(real_path)

    network_file = open(path + ".json", "w")
    json.dump(option_dict, network_file)
    network_file.close()


def write_genetic_training(data: str, path: str, overwrite: bool):
    path = path + "/genetic_data.txt"
    if overwrite:
        with open(path, 'w') as file:
            file.write(data + "\n")
    else:
        with open(path, 'a') as file:
            file.write(data + "\n")


def read_all_from_json(path: str) -> Dict:
    json_file = open(path, "r")
    json_object = json.load(json_file)

    output_network = NeuralNetwork()
    if json_object:
        for layer in json_object["network"]:
            if layer["layer"] == "dense":
                input_size = layer["input_size"]
                output_size = layer["output_size"]
                weights = np.reshape(layer["weights"], (layer["output_size"], layer["input_size"]))
                bias = np.reshape(layer["bias"], (layer["output_size"], 1))
                dense_layer = Dense(input_size, output_size)
                dense_layer.weights = weights
                dense_layer.bias = bias
                output_network.add_layer(dense_layer)
            else:
                activation_str = layer["activation"]
                activation_prime_str = layer["activation_prime"]

                activation = getattr(neural_network, activation_str)
                activation_prime = getattr(neural_network, activation_prime_str)

                activation_layer = Activation(activation, activation_prime)
                output_network.add_layer(activation_layer)

    output = json_object
    output["network"] = output_network
    return output
