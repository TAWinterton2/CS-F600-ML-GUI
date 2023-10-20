import numpy as np
import pandas as pd


def scaling(y, bool):
    """This function handles the process of scaling our machine learning model."""
    # Normalize the data - Convert to range [0, 1]
    if bool:
        Y = (y - np.min(y)) / (np.max(y) - np.min(y))
    # Standardize the data - Convert to a normal distribution with mean 0 and standard deviation of 1
    else:
        Y = (y - np.mean(y)) / np.std(y)
    return Y


def test_train_split():
    pass


def initialize():
    pass


def fit_model():
    pass


def predict_model():
    pass


def graph_prediction():
    pass


def mean_absolute_error():
    pass


def mean_square_error():
    pass


def root_mean_square_error():
    pass