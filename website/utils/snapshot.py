import pandas as pd
import numpy as np

class snapshot():
    """This class handles keeping track of the data snapshot that the user submits."""
    def __init__(self):
        self.og_data = None
        self.data = None
        self.filename = None
        self.model = None
        self.x = None
        self.y = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.y_pred = None

    def select_columns(self, x, y):
        df = self.og_data[[x, y]].copy()
        self.data = df

    def clean_data(self, df):
        """This function handles cleaning the dataset. This is done by removing all null values from the set."""
        df.dropna(inplace=True)

    def set_prediction_values(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

        columns = self.data.columns
        train = pd.DataFrame({columns[0]: x_train, columns[1]: y_train})
        test = pd.DataFrame({columns[0]: x_test, columns[1]: y_test})
        return train, test
    
    def reshape_data(self):
        self.x_train = self.x_train.reshape(-1, 1)
        self.x_test = self.x_test.reshape(-1, 1)