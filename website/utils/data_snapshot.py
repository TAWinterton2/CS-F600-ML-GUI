import pandas as pd

class DataSnapshot():
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

    def create_x_y_split(self, df):
        self.x = df.iloc[:,0].astype(float).to_numpy()
        self.y = df.iloc[:,1].astype(float).to_numpy()
        return self.x, self.y

    def merge_x_y(self, x, y):
        cols = self.data.columns.tolist()
        return pd.DataFrame({cols[0]: x, cols[1]: y})

    def select_columns(self, x, y):
        df = self.og_data[[x, y]].copy()
        self.data = df
        self.create_x_y_split(df)

    def clean_data(self, df):
        """This function handles cleaning the dataset. This is done by removing all null values from the set."""
        df.dropna(inplace=True)

    def set_prediction_values(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

        train = self.merge_x_y(x_train, y_train)
        test = self.merge_x_y(x_test, y_test)
        return train, test
    
    def reshape_data(self):
        self.x_train = self.x_train.reshape(-1, 1)
        self.x_test = self.x_test.reshape(-1, 1)