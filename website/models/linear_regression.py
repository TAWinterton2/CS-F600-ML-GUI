import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import sys


def scaling(df, bool):
    """This function handles the process of scaling our machine learning model."""
    # Normalize the data - Convert to range [0, 1]
    columns = df.columns
    x = df.iloc[:,0].to_numpy()
    y = df.iloc[:,1].to_numpy()
    if bool == "Normalize":
        Y = (y - np.min(y)) / (np.max(y) - np.min(y))
    # Standardize the data - Convert to a normal distribution with mean 0 and standard deviation of 1
    else:
        Y = (y - np.mean(y)) / np.std(y)
    
    return pd.DataFrame({columns[0]: x, columns[1]: Y})


def test_train_split(X, Y, test_size, train_size):
    """This function handles the process of splitting our dataset into testing and training sets."""
    X_train_split, X_test_split, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
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