from sklearn.metrics import classification_report, recall_score, precision_score, f1_score, accuracy_score


def calc_metrics(ps, refs):
    tmp_r = recall_score(refs, ps)
    tmp_p = precision_score(refs, ps)
    tmp_f = f1_score(refs, ps)
    tmp_a = accuracy_score(refs, ps)
    return [tmp_a, tmp_p, tmp_r, tmp_f]
