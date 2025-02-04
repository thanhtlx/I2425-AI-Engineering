from autogluon.tabular import TabularDataset, TabularPredictor
from sklearn.svm import SVC


def get_model(type_model):
    if type_model == "auto":
        return TabularPredictor(label="label", path="output")
    return SVC()
