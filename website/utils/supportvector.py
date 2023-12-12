from sklearn import svm
from website.utils.model import Model

class SupportVectorMachine(Model):
    def initalize(val):
    
        svm_model = svm.SVC( C=val[0], kernel=val[1], degree=val[2], gamma=val[3], coef0=val[4], shrinking=val[5],
                             probability=val[6], tol=val[7], cache_size=val[8], class_weight=val[9],
                             verbose=val[10], max_iter=val[11], decision_function_shape=val[12], break_ties=val[13], random_state=val[14])
        
        return svm_model()

    def evaluate(y_test, y_pred):

        results = {'Accuracy Score': Model.accuracy(y_test, y_pred),
                'Recall': Model.recall(y_test, y_pred),
                'Precision': Model.precision(y_test, y_pred)}
        return results


    pass