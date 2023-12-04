from sklearn.linear_model import LogisticRegression
from website.utils.model import Model

class LogRegr(Model):
    def initialize(val):
        """This function initializes the logistic regression model based on the user provided inputs."""
        regr = LogisticRegression(penalty=val[0], dual=eval(val[1]), tol=val[2], C=val[3], fit_intercept=eval(val[4]), 
        intercept_scaling=val[5], class_weight=val[6], random_state=val[7], solver=val[8], max_iter=val[9], multi_class=val[10], 
        verbose=val[11], warm_start=eval(val[12]), n_jobs=val[13], l1_ratio=val[14])
        return regr

    def evaluate(y_test, y_pred):
        results = {'Accuracy Score': Model.accuracy(y_test, y_pred),
                'Recall': Model.recall(y_test, y_pred),
                'Precision': Model.precision(y_test, y_pred)}
        return results