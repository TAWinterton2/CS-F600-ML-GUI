from sklearn.linear_model import SGDRegressor
from website.utils.model import Model

class LinearRegression(Model):
    def initialize(val):
        """This function initializes the linear regression model based on the user provided inputs."""
        regr = SGDRegressor(loss=val[0], penalty=val[1], alpha=val[2], l1_ratio=val[3], fit_intercept=eval(val[4]), 
                    max_iter=val[5], tol=val[6], shuffle=eval(val[7]), verbose=val[8], epsilon=val[9], random_state=val[10], 
                    learning_rate=val[11], eta0=val[12], power_t=val[13], early_stopping=eval(val[14]), validation_fraction=val[15], 
                    n_iter_no_change=val[16], warm_start=eval(val[17]), average=eval(val[18]))
        return regr

    def evaluate(y_test, y_pred):
        results = {'Mean Absolute Error': Model.mean_absolute_error(y_test, y_pred),
                'Mean Square Error': Model.mean_square_error(y_test, y_pred),
                'Root Mean Square Error': Model.root_mean_square_error(y_test, y_pred),
                'R2 Score': Model.r2_score(y_test, y_pred),
                'Max Error': Model.max_error(y_test, y_pred)}
        return results