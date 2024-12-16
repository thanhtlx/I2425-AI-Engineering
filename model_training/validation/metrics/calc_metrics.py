from sklearn.metrics import accuracy_score


def calc_metrics(predicts, refs):
    # TODO: f1, recall, precision, auc
    return accuracy_score(refs, predicts)
