import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIButton

from States.base_state import BaseState
from States.state_manager import StateManager
from constants import BoardConsts, State
from model import Model
from settings import SnakeSettings
from train_network import read_neural_network_from_json
from view import draw_board
from vision import get_vision_lines


class GeneticRunTrainedNetwork(BaseState):
    def __init__(self, state_manager: StateManager, ui_manager: UIManager):
        super().__init__(State.GENETIC_RUN_TRAINED_NETWORK, state_manager)

        self.model = None

        self.ui_manager = ui_manager

        self.title_label = None
        self.score_counter = None
        self.button_back = None

    def start(self):
        self.title_label = UILabel(pygame.Rect((87, 40), (800, 50)), "Trained Genetic Network", self.ui_manager, object_id="#window_label")
        self.button_back = UIButton(pygame.Rect((50, 100), (150, 35)), "BACK", self.ui_manager)
        self.score_counter = UILabel(pygame.Rect((50, 150), (150, 35)), "Score: ", self.ui_manager)
        self.model = Model(BoardConsts.BOARD_SIZE, SnakeSettings.START_SNAKE_SIZE, read_neural_network_from_json())

    def end(self):
        self.title_label.kill()
        self.button_back.kill()
        self.score_counter.kill()

    def run(self, surface, time_delta):
        surface.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

        vision_lines = get_vision_lines(self.model.board)
        neural_net_prediction = self.model.get_nn_output(vision_lines)

        draw_board(surface, self.model.board, 500, 300)

        next_direction = self.model.get_nn_output_4directions(neural_net_prediction)
        is_alive = self.model.move_in_direction(next_direction)
        self.score_counter.set_text("Score: " + str(self.model.snake.score))

        if not is_alive:
            self.model = Model(BoardConsts.BOARD_SIZE, SnakeSettings.START_SNAKE_SIZE, self.model.snake.brain)

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
                    self.set_target_state_name(State.GENETIC_MENU)
                    self.trigger_transition()

        self.ui_manager.update(time_delta)

        self.ui_manager.draw_ui(surface)
