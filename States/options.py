from typing import List, Tuple

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIButton, UIDropDownMenu, UITextEntryLine

from States.base_state import BaseState
from States.state_manager import StateManager
from game_config import *


# noinspection PyTypeChecker
class Options(BaseState):
    def __init__(self, ui_manager: UIManager):
        super().__init__(State.OPTIONS)

        self.ui_manager = ui_manager
        self.options_target = None

        self.snake_options_list: [] = []
        self.genetic_options_list: [] = []
        self.neural_network_options_list: [] = []
        self.options_state = 0

        self.title_label = None
        self.button_back: UIButton = None

        self.button_next: UIButton = None
        self.options_done = False

        self.dropdown_input_direction_count: UIDropDownMenu = None
        self.dropdown_input_direction_count_label: UILabel = None

        self.dropdown_vision_line_return_type: UIDropDownMenu = None
        self.dropdown_vision_line_return_type_label: UILabel = None

        self.population_count_entry: UITextEntryLine = None
        self.population_count_entry_label: UILabel = None

        self.mutation_rate_entry: UITextEntryLine = None
        self.mutation_rate_entry_label: UILabel = None

        self.board_size_entry: UITextEntryLine = None
        self.board_size_entry_label: UILabel = None

        self.starting_snake_size_entry: UITextEntryLine = None
        self.starting_snake_size_entry_label: UILabel = None

        self.file_name_entry: UITextEntryLine = None
        self.file_name_entry_label: UILabel = None

        self.dropdown_activation_function_hidden: UIDropDownMenu = None
        self.dropdown_activation_function_hidden_label: UILabel = None

        self.dropdown_activation_function_output: UIDropDownMenu = None
        self.dropdown_activation_function_output_label: UILabel = None

        self.crossover_operators_dropdown: UIDropDownMenu = None
        self.crossover_operators_label = None

        self.selection_operators_dropdown: UIDropDownMenu = None
        self.selection_operators_label = None

        self.mutation_operators_dropdown: UIDropDownMenu = None
        self.mutation_operators_label = None

        self.hidden_layer_count_entry: UITextEntryLine = None
        self.hidden_layer_count_entry_label: UILabel = None
        self.neural_network_layers_entries: List[Tuple[UITextEntryLine, UILabel]] = []

    def draw_entry_line(self, x_pos, y_pos, width, height, label):
        entry = UITextEntryLine(pygame.Rect((x_pos, y_pos), (width, height)), self.ui_manager)
        label = UILabel(pygame.Rect((x_pos, y_pos - 50), (250, height)), label, self.ui_manager)

        return entry, label

    def start(self):
        self.options_target = self.data_received["state"]
        self.options_state = 0

        self.title_label = UILabel(pygame.Rect(ViewSettings.TITLE_LABEL_POSITION, ViewSettings.TITLE_LABEL_DIMENSION), "", self.ui_manager)
        self.button_back = UIButton(pygame.Rect(ViewSettings.BUTTON_BACK_POSITION, ViewSettings.BUTTON_BACK_DIMENSION), "BACK", self.ui_manager)

        # ================================================
        self.starting_snake_size_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2 - 150, 350), (75, 30)), self.ui_manager)
        self.starting_snake_size_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 - 150, 300), (250, 35)), "Starting Snake Size", self.ui_manager)
        self.starting_snake_size_entry.set_text(str(GameSettings.INITIAL_SNAKE_SIZE))

        self.board_size_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2 + 150, 350), (75, 30)), self.ui_manager)
        self.board_size_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 + 150, 300), (250, 35)), "Board Size", self.ui_manager)
        self.board_size_entry.set_text(str(GameSettings.INITIAL_BOARD_SIZE))

        # ================================================
        self.dropdown_input_direction_count = UIDropDownMenu(GameSettings.AVAILABLE_INPUT_DIRECTIONS, GameSettings.AVAILABLE_INPUT_DIRECTIONS[0], pygame.Rect((ViewSettings.X_CENTER - 75 // 2 - 250, 350), (75, 30)), self.ui_manager)
        self.dropdown_input_direction_count_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 - 250, 300), (250, 35)), "Input Direction Count", self.ui_manager)

        self.dropdown_vision_line_return_type = UIDropDownMenu(GameSettings.AVAILABLE_VISION_LINES_RETURN_TYPE, GameSettings.AVAILABLE_VISION_LINES_RETURN_TYPE[0], pygame.Rect((ViewSettings.X_CENTER - 125 // 2 + 250, 150), (125, 30)),
                                                               self.ui_manager)
        self.dropdown_vision_line_return_type_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 + 250, 100), (250, 35)), "Vision Line Return Type", self.ui_manager)

        self.dropdown_activation_function_output_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2, 100), (250, 35)), "Output Activation Function", self.ui_manager)
        self.dropdown_activation_function_output = UIDropDownMenu(GameSettings.AVAILABLE_ACTIVATION_FUNCTIONS, GameSettings.AVAILABLE_ACTIVATION_FUNCTIONS[0], pygame.Rect((ViewSettings.X_CENTER - 125 // 2, 150), (125, 30)), self.ui_manager)

        self.dropdown_activation_function_hidden_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 - 250, 100), (250, 35)), "Hidden Activation Function", self.ui_manager)
        self.dropdown_activation_function_hidden = UIDropDownMenu(GameSettings.AVAILABLE_ACTIVATION_FUNCTIONS, GameSettings.AVAILABLE_ACTIVATION_FUNCTIONS[2], pygame.Rect((ViewSettings.X_CENTER - 125 // 2 - 250, 150), (125, 30)), self.ui_manager)

        self.hidden_layer_count_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2, 350), (75, 30)), self.ui_manager)
        self.hidden_layer_count_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2, 300), (250, 35)), "Hidden Layer Count", self.ui_manager)
        self.hidden_layer_count_entry.set_text("1")

        input_neuron_count = int(self.dropdown_input_direction_count.selected_option) * 3 + 4
        input_layer = UILabel(pygame.Rect((ViewSettings.X_CENTER - 75 // 2 - 250, 550), (75, 30)), str(input_neuron_count), self.ui_manager)
        input_layer_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 125 // 2 - 250, 500), (125, 30)), "Input Layer", self.ui_manager)

        output_neuron_count = 4 if int(self.dropdown_input_direction_count.selected_option) == 4 or int(self.dropdown_input_direction_count.selected_option) == 8 else 3
        output_layer = UILabel(pygame.Rect((ViewSettings.X_CENTER - 75 // 2 + 250, 550), (75, 30)), str(output_neuron_count), self.ui_manager)
        output_layer_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 125 // 2 + 250, 500), (125, 30)), "Output Layer", self.ui_manager)

        # TODO add options for more hidden layers
        first_hidden_layer_neuron_count = input_neuron_count + 8
        first_hidden_layer = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2, 550), (75, 30)), self.ui_manager)
        first_hidden_layer_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 125 // 2, 500), (125, 30)), "Hidden Layer", self.ui_manager)
        first_hidden_layer.set_text(str(first_hidden_layer_neuron_count))

        self.neural_network_layers_entries.append([input_layer, input_layer_label])
        self.neural_network_layers_entries.append([first_hidden_layer, first_hidden_layer_label])
        self.neural_network_layers_entries.append([output_layer, output_layer_label])

        # ================================================
        self.population_count_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2, 150), (75, 30)), self.ui_manager)
        self.population_count_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 200 // 2, 100), (200, 35)), "Individuals in Population", self.ui_manager)
        self.population_count_entry.set_text(str(GameSettings.POPULATION_COUNT))

        self.mutation_rate_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 75 // 2 + 250, 550), (75, 30)), self.ui_manager)
        self.mutation_rate_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 200 // 2 + 250, 500), (200, 35)), "Mutation Rate", self.ui_manager)
        self.mutation_rate_entry.set_text(str(GameSettings.MUTATION_CHANCE))

        self.crossover_operators_dropdown = UIDropDownMenu(GameSettings.AVAILABLE_CROSSOVER_OPERATORS, GameSettings.AVAILABLE_CROSSOVER_OPERATORS[0], pygame.Rect((ViewSettings.X_CENTER - 225 // 2, 350), (225, 30)), self.ui_manager)
        self.crossover_operators_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2, 300), (250, 35)), "Crossover Operators", self.ui_manager)

        self.selection_operators_dropdown = UIDropDownMenu(GameSettings.AVAILABLE_SELECTION_OPERATORS, GameSettings.AVAILABLE_SELECTION_OPERATORS[0], pygame.Rect((ViewSettings.X_CENTER - 225 // 2 - 250, 350), (225, 30)), self.ui_manager)
        self.selection_operators_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 - 250, 300), (250, 35)), "Selection Operators", self.ui_manager)

        self.mutation_operators_dropdown = UIDropDownMenu(GameSettings.AVAILABLE_MUTATION_OPERATORS, GameSettings.AVAILABLE_MUTATION_OPERATORS[0], pygame.Rect((ViewSettings.X_CENTER - 225 // 2 + 250, 350), (225, 30)), self.ui_manager)
        self.mutation_operators_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2 + 250, 300), (250, 35)), "Mutation Operators", self.ui_manager)

        self.genetic_options_list = [self.mutation_rate_entry, self.mutation_rate_entry_label, self.population_count_entry, self.population_count_entry_label, self.crossover_operators_dropdown, self.crossover_operators_label,
                                     self.selection_operators_dropdown, self.selection_operators_label, self.mutation_operators_dropdown, self.mutation_operators_label]

        self.snake_options_list = [self.starting_snake_size_entry, self.starting_snake_size_entry_label, self.board_size_entry, self.board_size_entry_label]

        self.neural_network_options_list = [self.dropdown_activation_function_output, self.dropdown_activation_function_output_label, self.dropdown_activation_function_hidden,
                                            self.dropdown_activation_function_hidden_label, self.dropdown_input_direction_count,
                                            self.dropdown_input_direction_count_label, self.dropdown_vision_line_return_type, self.dropdown_vision_line_return_type_label,
                                            self.hidden_layer_count_entry, self.hidden_layer_count_entry_label]

        # ================================================
        self.file_name_entry = UITextEntryLine(pygame.Rect((ViewSettings.X_CENTER - 175 // 2, 350), (175, 30)), self.ui_manager)
        self.file_name_entry_label = UILabel(pygame.Rect((ViewSettings.X_CENTER - 250 // 2, 300), (250, 35)), "Network name", self.ui_manager)
        self.file_name_entry.set_text("Default")
        self.file_name_entry.hide()
        self.file_name_entry_label.hide()

        self.button_next = UIButton(pygame.Rect((ViewSettings.X_CENTER - 75 // 2, 675), (75, 40)), "Next", self.ui_manager)

    def hide_layer_entries(self):
        for ui_element in self.neural_network_layers_entries:
            ui_element[0].hide()
            ui_element[1].hide()

    def show_layer_entries(self):
        for ui_element in self.neural_network_layers_entries:
            ui_element[0].show()
            ui_element[1].show()

    def end(self):
        self.ui_manager.clear_and_reset()

    def hide_all(self):
        for option in self.snake_options_list:
            option.hide()
        for option in self.neural_network_options_list:
            option.hide()
        for option in self.genetic_options_list:
            option.hide()
        self.hide_layer_entries()
        self.file_name_entry.hide()
        self.file_name_entry_label.hide()

    def draw_options(self):
        match self.options_state:
            case -1:
                if self.options_target == "genetic":
                    self.set_target_state_name(State.GENETIC_MENU)
                else:
                    self.set_target_state_name(State.BACKPROPAGATION_MENU)
                self.trigger_transition()

            case 0:
                self.hide_all()
                for option in self.snake_options_list:
                    option.show()
                self.title_label.set_text("Snake Game Options")

            case 1:
                for option in self.snake_options_list:
                    option.hide()

                self.show_layer_entries()
                for option in self.neural_network_options_list:
                    option.show()
                self.title_label.set_text("Neural Network Options")

            case 2:
                self.hide_layer_entries()
                for option in self.neural_network_options_list:
                    option.hide()

                for option in self.genetic_options_list:
                    option.show()
                self.title_label.set_text("Genetic Algorithm Options")

            case 3:
                for option in self.genetic_options_list:
                    option.hide()

                self.file_name_entry.show()
                self.file_name_entry_label.show()
                self.button_next.set_text("RUN")

            case 4:
                if self.options_target == "genetic":
                    self.set_target_state_name(State.GENETIC_TRAIN_NEW_NETWORK)
                    self.data_to_send = {
                        "input_direction_count": int(self.dropdown_input_direction_count.selected_option),
                        "vision_return_type": self.dropdown_vision_line_return_type.selected_option,
                        "file_name": self.file_name_entry.text,
                        "hidden_activation": self.dropdown_activation_function_hidden.selected_option,
                        "output_activation": self.dropdown_activation_function_output.selected_option,
                        "input_layer_neurons": int(self.neural_network_layers_entries[0][0].text),
                        "hidden_layer_neurons": int(self.neural_network_layers_entries[1][0].text),
                        "output_layer_neurons": int(self.neural_network_layers_entries[2][0].text),
                        "population_count": int(self.population_count_entry.text),
                        "selection_operator": self.selection_operators_dropdown.selected_option,
                        "crossover_operator": self.crossover_operators_dropdown.selected_option,
                        "mutation_operator": self.mutation_operators_dropdown.selected_option,
                        "mutation_rate": float(self.mutation_rate_entry.text),
                        "initial_snake_size": int(self.starting_snake_size_entry.text),
                        "board_size": int(self.board_size_entry.text)
                    }
                else:
                    self.set_target_state_name(State.BACKPROPAGATION_TRAIN_NEW_NETWORK)
                    self.data_to_send = {
                        "input_direction_count": int(self.dropdown_input_direction_count.selected_option),
                        "vision_return_type": self.dropdown_vision_line_return_type.selected_option,
                        "file_name": self.file_name_entry.text,
                        "hidden_activation": self.dropdown_activation_function_hidden.selected_option,
                        "output_activation": self.dropdown_activation_function_output.selected_option,
                        "input_layer_neurons": int(self.neural_network_layers_entries[0][0].text),
                        "hidden_layer_neurons": int(self.neural_network_layers_entries[1][0].text),
                        "output_layer_neurons": int(self.neural_network_layers_entries[2][0].text),
                        "initial_snake_size": int(self.starting_snake_size_entry.text),
                        "board_size": int(self.board_size_entry.text)
                    }

                self.trigger_transition()

    def run(self, surface, time_delta):
        surface.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

        self.neural_network_layers_entries[0][0].set_text(str(int(self.dropdown_input_direction_count.selected_option) * 3 + 4))
        self.draw_options()

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
                    if self.options_state == 3 and self.options_target == "backpropagation":
                        self.options_state -= 2
                    else:
                        self.options_state -= 1

                if event.ui_element == self.button_next:
                    if self.options_state == 1 and self.options_target == "backpropagation":
                        self.options_state += 2
                    else:
                        self.options_state += 1

        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(surface)
