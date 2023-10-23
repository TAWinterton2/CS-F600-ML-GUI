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


def test_train_split(df,testsplit, trainsplit):
    
    x = df.iloc[:,0].to_numpy()
    y = df.iloc[:,1].to_numpy()
    columns = df.columns


    x_train, x_test, y_train, y_test = train_test_split(x,y , 
                                   random_state=104,  
                                   test_size=testsplit / 100,
                                   train_size=trainsplit / 100,
                                   shuffle=True) 
    
    print("Test / Train Split")
    print(x_train)
    print(x_test)
    print(y_test)
    print(y_train)


  
    return pd.DataFrame({columns[0]: x_train, columns[1]: y_train}), pd.DataFrame({columns[0]: x_test, columns[1]: y_test})




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