import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn import metrics

def scaling(snapshot, bool):
    """This function handles the process of scaling our machine learning model."""
    # Normalize the data - Convert to range [0, 1]
    columns = snapshot.data.columns
    snapshot.x = snapshot.data.iloc[:,0].to_numpy()
    y = snapshot.data.iloc[:,1].to_numpy()
    if bool == "Normalize":
        snapshot.y = (y - np.min(y)) / (np.max(y) - np.min(y))
    # Standardize the data - Convert to a normal distribution with mean 0 and standard deviation of 1
    else:
        snapshot.y = (y - np.mean(y)) / np.std(y)
    
    return pd.DataFrame({columns[0]: snapshot.x, columns[1]: snapshot.y})


def test_train_split(snapshot, test_split, train_split):
    """This function handles the testing and training split of the data."""
    msg = ""

    # Simple error checking for the program to ensure proper user input.
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

    x_train, x_test, y_train, y_test = train_test_split(snapshot.x, 
                                                        snapshot.y, 
                                                        random_state=104,  
                                                        test_size=test_split,
                                                        train_size=train_split,
                                                        shuffle=True)
    train, test = snapshot.set_prediction_values(x_train, x_test, y_train, y_test)
    
    return train, test, msg


def initialize(snapshot, val):
    """This function initializes the linear regression model based on the user provided inputs."""
    regr = SGDRegressor(loss=val[0], penalty=val[1], alpha=float(val[2]), l1_ratio=float(val[3]), fit_intercept=eval(val[4]), 
                 max_iter=int(val[5]), tol=float(val[6]), shuffle=eval(val[7]), verbose=int(val[8]), epsilon=float(val[9]), random_state=int(val[10]), 
                 learning_rate=val[11], eta0=float(val[12]), power_t=float(val[13]), early_stopping=eval(val[14]), validation_fraction=float(val[15]), 
                 n_iter_no_change=int(val[16]), warm_start=eval(val[17]), average=eval(val[18]))
    snapshot.model = regr

def fit_model(snapshot):
    snapshot.reshape_data()
    snapshot.model.fit(snapshot.x_train, snapshot.y_train)

def predict_model(snapshot):
    snapshot.y_pred = snapshot.model.predict(snapshot.x_test)

def graph_prediction():
    pass

def evaluate(snapshot):
    results = {'Mean Absolute Error': mean_absolute_error(snapshot),
               'Mean Square Error': mean_square_error(snapshot),
               'Root Mean Square Error': root_mean_square_error(snapshot)}
    print(results)
    return results

def mean_absolute_error(snapshot):
    result = metrics.mean_absolute_error(snapshot.y_test, snapshot.y_pred)
    return result

def mean_square_error(snapshot):
    result = metrics.mean_squared_error(snapshot.y_test, snapshot.y_pred)
    return result

def root_mean_square_error(snapshot):
    result = np.sqrt(metrics.mean_squared_error(snapshot.y_test, snapshot.y_pred))
    return result