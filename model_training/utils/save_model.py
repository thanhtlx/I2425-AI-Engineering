from joblib import dump


def save_model(model):
    out_dir = "output/model.pkl"
    dump(model, out_dir)
    return out_dir
