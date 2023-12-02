import pandas as pd
import numpy as np
from operator import itemgetter

class DataSnapshot():
    """This class handles keeping track of the data snapshot that the user submits."""
    def __init__(self):
        self.og_data = None         # The original dataset as a dataframe
        self.data = None            # The current dataset as a dataframe
        self.filename = None        # The name of the file
        self.model = None           # The model object created in the initialization stage
        self.model_type = ""        # A string that denotes what type of model currently being used
        self.x = None               # Input columns as a numpy array
        self.y = None               # Target column as a numpy array
        self.x_train = None         
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.N = None               # Total number of columns selected

    def create_x_y_split(self, df):
        """Splits the dataframe into 2 numpy arrays. Assumes the final column of the dataframe is the target column."""
        self.x = df.iloc[:,:self.N-1].astype(float).to_numpy()
        self.y = df.iloc[:,-1:].astype(float).to_numpy()
        return self.x, self.y

    def merge_x_y(self, x, y):
        cols = self.data.columns.tolist()
        data = np.column_stack((x, y))
        df = pd.DataFrame(data, columns = cols)   
        return df
    
    def sort_x(self, x_test, y_test):
        """Sorts the test sets based on the first X input for better graphing visuals."""
        # TODO: Review this function to ensure it is properly sorting values.
        enumerate_x = enumerate(x_test)
        sorted_pairs = sorted(enumerate_x, key=lambda x: x[1][0])
        sorted_indices = [index for index, element in sorted_pairs]
        X_test = sorted(x_test, key=lambda x: x[0])
        Y_test = itemgetter(*sorted_indices)(y_test)
        return np.array(X_test), np.array(Y_test)

    def select_columns(self, x, y):
        """Retrieves the input and target columns from the original dataset."""
        self.N = len(x)+1
        x.append(y)
        df = self.og_data[x].copy()
        self.data = df

    def clean_data(self, df):
        """This function handles cleaning the dataset. This is done by removing all null values from the set."""
        df.dropna(inplace=True)

    def set_prediction_values(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

        # train = self.merge_x_y(x_train, y_train)
        # test = self.merge_x_y(x_test, y_test)
        # return train, test
    
    def reshape_data(self):
        self.x_train = self.x_train.reshape(-1, 1)
        self.x_test = self.x_test.reshape(-1, 1)