import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor


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


def test_train_split(df,test_split, train_split):
    
    x = df.iloc[:,0].to_numpy()
    y = df.iloc[:,1].to_numpy()
    columns = df.columns
    msg = ""

    if test_split + train_split != 100:
        return None, None, "Please ensure that the test/training split values total up to 100."

    if test_split < 0 or train_split < 0:
        return None, None, "Please ensure that the test/training are greater than 0 and total up to 100."
    
    if test_split > 1:
        test_split = test_split/100
    
    if train_split > 1:
        train_split = train_split/100

    if test_split > train_split:
        msg = "Please be aware that your training value should be greater than your testing value."
    print(msg)
    x_train, x_test, y_train, y_test = train_test_split(x,y , 
                                   random_state=104,  
                                   test_size=test_split,
                                   train_size=train_split,
                                   shuffle=True) 
    
    return pd.DataFrame({columns[0]: x_train, columns[1]: y_train}), pd.DataFrame({columns[0]: x_test, columns[1]: y_test}), msg


def initialize(val):
    for x in val:
        print(x)
    regr = SGDRegressor(loss=val[0], penalty=val[1], alpha=val[2], l1_ratio=val[3], fit_intercept=eval(val[4]), 
                 max_iter=val[5], tol=val[6], shuffle=eval(val[7]), verbose=val[8], epsilon=val[9], random_state=val[10], 
                 learning_rate=val[11], eta0=val[12], power_t=val[13], early_stopping=eval(val[14]), validation_fraction=val[15], 
                 n_iter_no_change=val[16], warm_start=eval(val[17]), average=eval(val[18]))
        
    print(regr)
    return regr


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