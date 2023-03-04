from enum import Enum


class State(Enum):
    QUIT = 0
    MAIN_MENU = 1
    BACKPROPAGATION_MENU = 2
    GENETIC_MENU = 3
    GENETIC_RUN_TRAINED_NETWORK = 4
    GENETIC_TRAIN_NETWORK_OPTIONS = 5
    GENETIC_TRAIN_NEW_NETWORK = 6
    BACKPROPAGATION_TRAINED_NETWORK = 7
    BACKPROPAGATION_TRAIN_NEW_NETWORK_OPTIONS = 8
    BACKPROPAGATION_TRAIN_NEW_NETWORK = 9


class ViewConsts:
    DRAW = True
    # TODO option for draw in train new genetic
    MAX_FPS = 40
    # OFFSET_BOARD_X = 500
    # OFFSET_BOARD_Y = 100
    WIDTH, HEIGHT = 1366, 768
    SQUARE_SIZE = 25
    # WINDOW_START_X, WINDOW_START_Y = 50, 50

    # NN_DISPLAY_OFFSET_X = 50
    # NN_DISPLAY_OFFSET_Y = 150
    NN_DISPLAY_LABEL_HEIGHT_BETWEEN = 8
    # NN_DISPLAY_lABEL_OFFSET_X = NN_DISPLAY_OFFSET_X - 40
    NN_DISPLAY_NEURON_WIDTH_BETWEEN = 100
    NN_DISPLAY_NEURON_HEIGHT_BETWEEN = NN_DISPLAY_LABEL_HEIGHT_BETWEEN
    # NN_DISPLAY_NEURON_OFFSET_X = NN_DISPLAY_OFFSET_X + 100
    # NN_DISPLAY_NEURON_OFFSET_Y = NN_DISPLAY_OFFSET_Y
    NN_DISPLAY_NEURON_RADIUS = 8

    X_MIDDLE = WIDTH // 2
    Y_MIDDLE = HEIGHT // 2

    TITLE_LABEL_DIMENSION = (300, 50)
    TITLE_LABEL_POSITION = (X_MIDDLE - TITLE_LABEL_DIMENSION[0] // 2, 50)

    BUTTON_BACK_DIMENSION = (125, 35)
    BUTTON_BACK_POSITION = (50, HEIGHT - 100)

    PRETRAINED_BUTTON_DIMENSIONS = (250, 35)
    PRETRAINED_BUTTON_POSITION = (X_MIDDLE - PRETRAINED_BUTTON_DIMENSIONS[0] // 2 - 200, Y_MIDDLE - PRETRAINED_BUTTON_DIMENSIONS[1] // 2 - 100)

    OPTIONS_BUTTON_DIMENSIONS = (250, 35)
    OPTIONS_BUTTON_POSITION = (X_MIDDLE - OPTIONS_BUTTON_DIMENSIONS[0] // 2 + 200, Y_MIDDLE - OPTIONS_BUTTON_DIMENSIONS[1] // 2 - 100)

    NN_POSITION = (350, 150)
    BOARD_POSITION = (800, 150)

    COLOR_BLACK = (0, 0, 0)
    COLOR_BACKGROUND = (47, 47, 47)
    COLOR_WHITE = (255, 255, 255)
    COLOR_SNAKE_SEGMENT = (30, 144, 255)
    COLOR_SNAKE_HEAD = (128, 0, 128)
    COLOR_APPLE = (199, 55, 47)
    COLOR_SQUARE_DELIMITER = (64, 64, 64)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_NEXT_MOVE = (22, 255, 0)


class BoardConsts:
    APPLE = "A"
    WALL = "W"
    EMPTY = "."
    SNAKE_BODY = "S"
    SNAKE_HEAD = "H"


class Direction(Enum):
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]
    Q1 = [-1, 1]
    Q2 = [1, 1]
    Q3 = [1, -1]
    Q4 = [-1, -1]


DYNAMIC_DIRECTIONS = ["STRAIGHT", "LEFT", "RIGHT"]
MAIN_DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
ALL_DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.Q1, Direction.Q2, Direction.Q3, Direction.Q4]
