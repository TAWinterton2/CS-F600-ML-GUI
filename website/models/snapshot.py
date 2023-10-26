import pandas as pd
import numpy as np

class snapshot():
    """This class handles keeping track of the data snapshot that the user submits."""
    def __init__(self):
        self.og_data = None
        self.data = None
        self.filename = None
        self.x = None
        self.y = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None

    def select_columns(self, x, y):
        df = self.og_data[[x, y]].copy()
        self.data = df

    def clean_data(self, df):
        """This function handles cleaning the dataset. This is done by removing all null values from the set."""
        df.dropna(inplace=True)