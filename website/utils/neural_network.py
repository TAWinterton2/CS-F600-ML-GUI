from sklearn.neural_network import MLPClassifier
from website.utils.model import Model


class NeuralNetwork(Model):
    def initialize(val):
        """This function initializes the neural network model based on the user provided inputs."""
        mlp = MLPClassifier(
            hidden_layer_sizes=(8, 8, 8), activation="relu", solver="adam", max_iter=500
        )
        return mlp

    def evaluate(y_test, y_pred):
        results = {
            "Accuracy Score": Model.accuracy(y_test, y_pred),
            "Recall": Model.recall(y_test, y_pred),
            "Precision": Model.precision(y_test, y_pred),
        }
        return results
