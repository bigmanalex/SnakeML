from typing import List

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core.utility import create_resource_path
from pygame_gui.elements import UILabel, UIButton, UITextEntryLine
from pygame_gui.windows import UIFileDialog

import vision
from States.base_state import BaseState
from file_operations import read_all_from_json
from game_config import State, ViewSettings, GameSettings
from model import Model
from view import draw_board, draw_neural_network_complete, draw_vision_lines
from vision import get_vision_lines_snake_head


# TODO add ratio graph
class RunPretrained(BaseState):
    def __init__(self, ui_manager: UIManager):
        super().__init__(State.RUN_PRETRAINED)

        self.max_distance = None
        self.network = None
        self.ui_manager = ui_manager
        self.state_target = None
        self.max_dist = None

        self.overwrite = True
        self.file_path = None

        self.model = None
        self.execute_network = False
        self.input_direction_count = None
        self.segment_return_type = None
        self.distance_function = None
        self.apple_return_type = None

        self.score_counter = None
        self.button_back = None
        self.button_run = None
        self.button_load = None
        self.file_dialog = None

        self.board_size_entry = None
        self.board_size_label = None

        self.snake_size_entry = None
        self.snake_size_label = None

        self.button_draw_network = None
        self.draw_network = False
        self.rect_draw_network = None

        self.button_draw_vision_lines = None
        self.draw_vision_lines = True
        self.rect_draw_vision_lines = None

        self.label_return_type: UILabel = None
        self.label_distance: UILabel = None

        self.x_steps = []
        self.y_ratio = []
        self.x_score = []

    @staticmethod
    def print_vision_line(vision_line: vision.VisionLine):
        print(f" {vision_line.direction} w_c {vision_line.wall_coord} w_d {vision_line.wall_distance} || a_c {vision_line.apple_coord} a_d {vision_line.apple_distance} || s_c {vision_line.segment_coord} s_d {vision_line.segment_distance} ")

    def print_all_vision_lines(self, vision_lines: List[vision.VisionLine]):
        for line in vision_lines:
            self.print_vision_line(line)

    def start(self):
        self.x_steps = []
        self.y_ratio = []
        self.x_score = []

        self.state_target = self.data_received["state"]
        self.button_back = UIButton(pygame.Rect(ViewSettings.BUTTON_BACK_POSITION, ViewSettings.BUTTON_BACK_DIMENSION), "BACK", self.ui_manager)
        self.label_return_type = UILabel(pygame.Rect((50, 25), (250, 35)), "", self.ui_manager)
        self.label_distance = UILabel(pygame.Rect((50, 50), (250, 35)), "", self.ui_manager)

        self.button_draw_network = UIButton(pygame.Rect((50, 400), (175, 30)), "Draw Network", self.ui_manager)
        self.rect_draw_network = pygame.Rect((250, 400), (30, 30))

        self.button_draw_vision_lines = UIButton(pygame.Rect((50, 500), (175, 30)), "Draw Vision Lines", self.ui_manager)
        self.rect_draw_vision_lines = pygame.Rect((250, 500), (30, 30))

        self.score_counter = UILabel(pygame.Rect((150, 100), (150, 35)), "Score: ", self.ui_manager)

        self.button_load = UIButton(pygame.Rect((25, 100), (125, 35)), "Load Network", self.ui_manager)
        self.button_run = UIButton(pygame.Rect((25, 150), (125, 35)), "Run Network", self.ui_manager)
        self.button_run.disable()

        self.board_size_label = UILabel(pygame.Rect((25, 250), (125, 35)), "Board Size", self.ui_manager)
        self.board_size_entry = UITextEntryLine(pygame.Rect((25, 300), (125, 35)), self.ui_manager)

        self.snake_size_label = UILabel(pygame.Rect((175, 250), (125, 35)), "Snake Size", self.ui_manager)
        self.snake_size_entry = UITextEntryLine(pygame.Rect((175, 300), (125, 35)), self.ui_manager)

    def end(self):
        self.ui_manager.clear_and_reset()
        self.execute_network = False

    def run_network(self, surface):
        vision_lines = get_vision_lines_snake_head(self.model.board, self.model.snake.body[0], self.input_direction_count,
                                                   max_dist=self.max_distance, apple_return_type=self.apple_return_type, segment_return_type=self.segment_return_type, distance_function=self.distance_function)

        if self.model.snake.brain.get_dense_layers()[0].input_size == 14:
            nn_input = vision.get_parameters_in_nn_input_form_2d(vision_lines, self.model.snake.direction)
        else:
            nn_input = vision.get_parameters_in_nn_input_form_4d(vision_lines, self.model.snake.direction)
        neural_net_prediction = self.model.snake.brain.feed_forward(nn_input)
        
        self.print_all_vision_lines(vision_lines)
        print(self.model.board)
        print(nn_input)
        print(neural_net_prediction)
        print("")

        if ViewSettings.DRAW:
            draw_board(surface, self.model.board, ViewSettings.BOARD_POSITION[0], ViewSettings.BOARD_POSITION[1])
            if self.draw_vision_lines:
                draw_vision_lines(surface, self.model.snake.body[0], vision_lines, ViewSettings.BOARD_POSITION[0], ViewSettings.BOARD_POSITION[1])
            if self.draw_network:
                draw_neural_network_complete(surface, self.model, vision_lines, ViewSettings.NN_POSITION[0], ViewSettings.NN_POSITION[1])

        next_direction = self.model.get_nn_output_4directions(neural_net_prediction)
        is_alive = self.model.move(next_direction)

        self.x_steps.append(self.model.snake.steps_taken)
        self.y_ratio.append(self.model.snake.score / self.model.snake.steps_taken if self.model.snake.steps_taken > 0 else 0)
        self.x_score.append(self.model.snake.score)

        self.score_counter.set_text("Score: " + str(self.model.snake.score))

        if not is_alive:
            print(self.model.snake.score / self.model.snake.steps_taken if self.model.snake.steps_taken > 0 else 0)
            self.model = Model(int(self.board_size_entry.text), int(self.snake_size_entry.text), True, self.model.snake.brain)

            # fig1 = plt.figure(figsize=(16, 9))
            # plt.plot(self.x_steps, self.y_ratio, )
            # plt.xlabel("Steps")
            # plt.ylabel("Ratio")
            # plt.savefig(os.path.dirname(self.file_path) + "/" + "step_ratio.pdf")
            # plt.show()
            #
            # fig2 = plt.figure(figsize=(16, 9))
            # plt.plot(self.x_score, self.y_ratio, "b")
            # plt.xlabel("Score")
            # plt.ylabel("Ratio")
            # plt.savefig(os.path.dirname(self.file_path) + "/" + "score_ratio.pdf")
            # plt.show()

            self.x_steps = []
            self.y_ratio = []
            self.x_score = []

    def run(self, surface, time_delta):
        if ViewSettings.DRAW:
            surface.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))
            pygame.draw.rect(surface, ViewSettings.COLOR_GREEN if self.draw_network else ViewSettings.COLOR_RED, self.rect_draw_network)
            pygame.draw.rect(surface, ViewSettings.COLOR_GREEN if self.draw_vision_lines else ViewSettings.COLOR_RED, self.rect_draw_vision_lines)

        if self.execute_network:
            self.run_network(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_target_state_name(State.QUIT)
                self.trigger_transition()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_target_state_name(State.QUIT)
                    self.trigger_transition()

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button_back:
                    if self.state_target == "genetic":
                        self.set_target_state_name(State.GENETIC_MENU)
                    else:
                        self.set_target_state_name(State.BACKPROPAGATION_MENU)
                    self.trigger_transition()

                if event.ui_element == self.button_run:
                    self.model = Model(int(self.board_size_entry.text), int(self.snake_size_entry.text), True, self.network)
                    # TODO dynamic max distance
                    self.max_dist = 10
                    self.execute_network = True
                    # ViewSettings.MAX_FPS = 0.5

                if event.ui_element == self.button_draw_network:
                    self.draw_network = not self.draw_network

                if event.ui_element == self.button_draw_vision_lines:
                    self.draw_vision_lines = not self.draw_vision_lines

                if event.ui_element == self.button_load:
                    self.execute_network = False
                    self.button_run.disable()

                    if self.state_target == "genetic":
                        file_path = "Genetic_Networks/"
                    else:
                        file_path = GameSettings.BACKPROPAGATION_NETWORK_FOLDER

                    self.file_dialog = UIFileDialog(pygame.Rect((150, 50), (450, 450)), self.ui_manager, window_title="Load Network", initial_file_path=file_path,
                                                    allow_picking_directories=False,
                                                    allow_existing_files_only=True)

            if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                try:
                    self.file_path = create_resource_path(event.text)
                    config = read_all_from_json(self.file_path)
                    self.network = config["network"]
                    self.input_direction_count = config["input_direction_count"]
                    self.apple_return_type = config["apple_return_type"]
                    self.segment_return_type = config["segment_return_type"]
                    self.distance_function = getattr(vision, config["distance_function"])
                    self.board_size_entry.set_text(str(config["board_size"]))
                    self.snake_size_entry.set_text(str(config["snake_size"]))
                    self.label_return_type.set_text("Segment: " + self.segment_return_type + " Apple: " + self.apple_return_type)
                    self.label_distance.set_text("Distance: " + config["distance_function"])
                    self.button_load.enable()
                    self.button_run.enable()

                except pygame.error:
                    pass

        if ViewSettings.DRAW:
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(surface)
