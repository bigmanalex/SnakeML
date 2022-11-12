import numpy as np


def relu(x):
    return np.maximum(0.0, x)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    return np.exp(x) / sum(np.exp(x))


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x) ** 2


def mean_squared_root(y_real, y_predicted):
    return np.mean(np.power(y_real - y_predicted, 2))


def mean_squared_root_prime(y_real, y_predicted):
    return 2 * (y_predicted - y_real) / y_real.size