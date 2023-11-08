import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split

class Model:
    def __init__(self):
        self.model = None

    def scaling(x, y, bool):
        """This function handles the process of scaling our machine learning model."""
        # Normalize the data - Convert to range [0, 1]
        if bool == "Normalize":
            Y = (y - np.min(y)) / (np.max(y) - np.min(y))
        # Standardize the data - Convert to a normal distribution with mean 0 and standard deviation of 1
        else:
            Y = (y - np.mean(y)) / np.std(y)
        
        return Y

    def test_train_split(x, y, test_split, train_split):
        """This function handles the testing and training split of the data."""
        msg = ""

        # Simple error checking for the program to ensure proper user input.
        if test_split + train_split != 100:
            return None, None, None, None, "Please ensure that the test/training split values total up to 100."

        if test_split < 0 or train_split < 0:
            return None, None, None, None, "Please ensure that the test/training are greater than 0 and total up to 100."
        
        if test_split > train_split:
            msg = "Please be aware that your training value should be greater than your testing value."

        if test_split > 1:
            test_split = test_split/100
        
        if train_split > 1:
            train_split = train_split/100

        x_train, x_test, y_train, y_test = train_test_split(x, 
                                                            y, 
                                                            random_state=104,  
                                                            test_size=test_split,
                                                            train_size=train_split,
                                                            shuffle=True)
        
        return x_train, x_test, y_train, y_test, msg

    def fit_model(ml_model, x_train, y_train):
        try:
            model = ml_model.fit(x_train, y_train)
            return model
        except Exception as e:
            return 'An error has occured when trying to fit the model. \n Please review your hyperparameters settings'

    def predict_model(ml_model, x_test):
        y_pred = ml_model.predict(x_test)
        return y_pred
    
    def mean_absolute_error(y_test, y_pred):
        result = metrics.mean_absolute_error(y_test, y_pred)
        return result

    def mean_square_error(y_test, y_pred):
        result = metrics.mean_squared_error(y_test, y_pred)
        return result

    def root_mean_square_error(y_test, y_pred):
        result = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
        return result

    def r2_score(y_test, y_pred):
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score
        result = metrics.r2_score(y_test, y_pred)
        return result

    def max_error(y_test, y_pred):
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.max_error.html#sklearn.metrics.max_error
        result = metrics.max_error(y_test, y_pred)
        return result

    # While these 3 values were requested, the methods do not work with regression.
    def accuracy(y_test, y_pred):
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score
        result = metrics.accuracy_score(y_test, y_pred)
        return result

    def recall(y_test, y_pred):
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html
        result = metrics.recall_score(y_test, y_pred)
        return result

    def precision(y_test, y_pred):
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score
        result = metrics.precision_score(y_test, y_pred)
        return result