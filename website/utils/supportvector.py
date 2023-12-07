from sklearn import svm
from website.utils.model import Model

class SupportVectorMachine(Model):
    def initalize(val):
        
        clf = svm.SVC(kernel='linear', C= 10)
        
        return clf

    def evaluate(y_test, y_pred):

        results = {'Accuracy Score': Model.accuracy(y_test, y_pred),
                'Recall': Model.recall(y_test, y_pred),
                'Precision': Model.precision(y_test, y_pred)}
        return results


    pass