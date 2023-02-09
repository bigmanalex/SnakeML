from Neural.train_network import *
from Neural.train_network import train_network
from model import *
from view import View


# TODO add options for using different neural networks
# TODO add options for using different directions 4,8,16
class Controller:
    def __init__(self, model: Model, view: View):
        self.running = True
        self.model = model
        self.view = view

    def run(self) -> None:
        training_examples = []
        while self.running:
            self.view.clear_window()

            vision_lines = get_vision_lines(self.model.board)

            neural_net_prediction = self.model.get_nn_output(vision_lines)
            nn_input = get_parameters_in_nn_input_form(vision_lines, self.model.snake.direction)

            # max maximum in neural net output 1, others 0
            example_prediction = np.where(neural_net_prediction == np.max(neural_net_prediction), 1, 0)
            example = TrainingExample(copy.deepcopy(self.model.board), example_prediction.ravel().tolist(), self.model.snake.direction)
            training_examples.append(example)

            if ViewConsts.DRAW:
                self.view.draw_board(self.model.board)
                self.view.draw_vision_lines(self.model, vision_lines)
                self.view.draw_neural_network(self.model, vision_lines, nn_input, neural_net_prediction)
                self.view.draw_score(self.model.snake.score)
                self.view.update_window()

            next_direction = self.model.get_nn_output_4directions(neural_net_prediction)
            self.running = self.model.move_in_direction(next_direction)

            if not self.running:
                if ViewConsts.DRAW:
                    self.view.draw_dead(self.model.board)

                evaluate_live_examples_4d(training_examples)
                training_examples = []

                # TODO BAD REINIT, TO BE REMOVED
                # TODO train data , search file like a dictionary to find if there are conflicting data
                self.model.snake.brain.reinit_weights_and_biases()
                train_network(self.model.snake.brain)

                # TODO add reinit function in model
                self.model = Model(BOARD_SIZE, START_SNAKE_SIZE, self.model.snake.brain)

                self.running = True
