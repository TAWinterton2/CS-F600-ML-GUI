from sklearn.neural_network import MLPClassifier
from website.utils.model import Model


class NeuralNetwork(Model):
    def initialize(val):
        """This function initializes the neural network model based on the user provided inputs."""
        print(val)
        mlp = MLPClassifier(
            hidden_layer_sizes=(100,),
            activation=val[3],
            solver=val[4],
            alpha=val[5],
            batch_size=val[6],
            learning_rate=val[7],
            learning_rate_init=val[8],
            power_t=val[9],
            max_iter=val[10],
            shuffle=eval(str(val[11])),
            random_state=val[12],
            tol=val[13],
            verbose=eval(str(val[14])),
            warm_start=eval(str(val[15])),
            momentum=val[16],
            nesterovs_momentum=eval(str(val[17])),
            early_stopping=eval(str(val[18])),
            validation_fraction=val[19],
            beta_1=val[20],
            beta_2=val[21],
            epsilon=val[22],
            n_iter_no_change=val[23],
            max_fun=val[24],
        )
        return mlp

    def evaluate(y_test, y_pred):
        results = {
            "Accuracy Score": Model.accuracy(y_test, y_pred),
            "Recall": Model.recall(y_test, y_pred),
            "Precision": Model.precision(y_test, y_pred),
        }
        return results
